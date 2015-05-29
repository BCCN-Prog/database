import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator

from pylab import rcParams
rcParams['figure.figsize'] = 20, 3 #setting plots size

#creating test time series
#rng = pd.date_range('1/1/2011', periods=5000, freq='D')
#ts = pd.Series(np.random.randn(np.size(rng)), index=rng)

def load_data(path):
    '''
    (str) -> (pandas.DataFrame)
    Loads the database and cleans the whitespace in STATIONS_ID.
    
    IMPORTANT: This function assumes you have the database stored in a text file in the directory.
    '''
    data = pd.read_csv(path, index_col = 2)
    
    date_form =  data.index.values.astype(str)
    for i in range(0, len(date_form)):
        date_form[i] = date_form[i][:-2]
        date_form[i] = pd.to_datetime(date_form[i])
    data.index = date_form
    
    #data = data.astype(str)
    #pd.to_datetime(df.day + df.month + df.year, format="%d%m%Y")
    
    data["STATIONS_ID"] = data["STATIONS_ID"].str.replace(' ', '')
    data["STATIONS_ID"] = data["STATIONS_ID"].convert_objects(convert_numeric=True)
    
    return data

def get_data(data, station_id, category = 3, start=None, end=None):
    """
    (pandas.Dataframe, int, list) -> (pandas.DataFrame)
    Returns desired information from the database about requested city and categories.
    
    station_id: The code for the requested city/station
    
    category: Can be an int or a list of desired variable(s). By default gets the air temperature.
    
        The codes for variables:
        0: Numerical Index
        1: STATIONS_ID
        2: QUALITAETS_NIVEAU
        3: Air Temperature / LUFTTEMPERATUR
        4: DAMPFDRUCK
        5: BEDECKUNGSGRAD
        6: LUFTDRUCK_STATIONSHOEHE
        7: REL_FEUCHTE
        8: WINDGESCHWINDIGKEIT
        9: Max Air Temperature
        10: Min Air Temperature
        11: LUFTTEMP_AM_ERDB_MINIMUM (?)
        12: Max Wind Speed / WINDSPITZE_MAXIMUM
        13: Precipitation Height / NIEDERSCHLAGSHOEHE (?)
        14: NIEDERSCHLAGSHOEHE_IND (?)
        15: Sunshine Duration
        16: Snow Height
    """
    
    rlv_station = data[data.iloc[:, 1] == station_id]
    selected = rlv_station.iloc[:, category]
    selected.index = pd.DatetimeIndex(selected.index) 
                
    return selected[start:end]
 
def calculating_means(time_series,resolution='month'): 
    #creates a DataFrame out of time series, rows-resolution, columns - years
    #for resolution='year' returns Series, indices - years
    #possible resolutions: 'dayofyear', 'month', 'year'
    years = range(time_series.index.year[0], time_series.index.year[-1]) 
    #years in period 
    yearly_resolution_stats = [time_series.xs(str(year)).groupby\
    (lambda x : operator.attrgetter(resolution)(x)).mean() for year in years]    
    df2 = pd.concat(yearly_resolution_stats, axis=1, keys = years)
#to do something here!    
    if resolution=='year': 
        df2=df2.mean().transpose()
        #flattening data if there is only one dimension
    return df2    

def finding_max(data_frame):
#same as finding_min
    if type(data_frame)==pd.core.frame.DataFrame:
         maximums, maximum_idces=data_frame.max(), data_frame.idxmax()
         maximum,maximum_idx_1=maximums.max(),maximums.idxmax()
         maximum_idx_2=maximum_idces.loc[maximum_idx_1]
         return maximum, maximum_idx_1,maximum_idx_2    
    else:
        return data_frame.max(),data_frame.idxmax()
    
def finding_min(data_frame):
#we pass to this function TimeSeries after preprocessing
    if type(data_frame)==pd.core.frame.DataFrame:
        #if not averaging, the input is data frame
        #makes things more complicated
        minimums, minimum_idces=data_frame.min(), data_frame.idxmin()
        #finding minimums in rows
        minimum,minimum_idx_1=minimums.min(),minimums.idxmin()
        #finding absolute minimum, it's first index
        minimum_idx_2=minimum_idces.loc[minimum_idx_1]
        #finding it's second index
        return minimum, minimum_idx_1,minimum_idx_2 
    else: #if after averaging, the input is series
        return data_frame.min(),data_frame.idxmin()
                                                
    
def get_statistics(time_series,resolution='month',function=finding_min,average=True):
    #function to find max/min averages/in total
    new_frame=calculating_means(time_series,resolution)  
    #data preprocessing
    if average and resolution!='year':
        new_frame=new_frame.mean(axis=1) #calculating averages
    return function(new_frame) 
    

def plot_means(time_series, resolution='month', number=1):     
    #takes timeseries as an input, makes resolution-years dataframe
    #returns list of years, list of mean values for one row
    new_frame=calculating_means(time_series,resolution)
    if type(new_frame) == pd.core.frame.DataFrame:
        ToPlot=new_frame.iloc[number] # to acess one row, 
    else:
        ToPlot=new_frame #if we are dealing with years 
    plotting_indices=ToPlot.index.tolist() 
    #get years
    return plotting_indices,ToPlot

#loading dara
Data=load_data('db.txt')
timeSeries=get_data(Data,1)

#Finding means to plot
Indices,Values=plot_means(timeSeries,resolution='year',number=10)

#just plotting
plt.figure()
plt.plot(Indices,Values,'o')
plt.xlim(Indices[0]-0.5,Indices[-1]+0.5)
plt.show()

#Finding min/max
print(get_statistics(timeSeries,resolution='dayofyear',function=finding_max,average=True))

#dayofyear attribute returns 1...365, not day-month
#also decided not to do statistics on 29-02, so preprocessing has to delete it