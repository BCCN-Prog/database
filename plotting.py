#Doesn't work properly, need TimeSeries!

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator


#creating test time series
rng = pd.date_range('1/1/2011', periods=5000, freq='D')
ts = pd.Series(np.random.randn(np.size(rng)), index=rng)

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
    #creates a DataFrame out of time series, indices-resolution, columns - years
    years = range(time_series.index.year[0], time_series.index.year[-1]) #period 
    yearly_resolution_stats = [time_series.xs(str(year)).groupby(lambda x : operator.attrgetter(resolution)(x)).mean() for year in years]    
    df2 = pd.concat(yearly_resolution_stats, axis=1, keys = years)
    
    return df2    

def finding_max(data_frame):#we pass to this function DataFrame either after preprocessing
                           
    return data_frame.max(),data_frame.idxmax()
    
def finding_min(data_frame):#same as finding_max

    return data_frame.min(),data_frame.idxmin()
                                                #data_frame.values.min() returns nan
    
def get_statistics(time_series,resolution='month',function=finding_min,average=True):
    #function to find max/min averages/in total
    transformed_frame=calculating_means(time_series,resolution)   
    if average:
        transformed_frame=transformed_frame.mean(axis=1) 
    return function(transformed_frame) 
    #doesn-t work when not averaging

def plot_one_month_means(time_series, resolution='month', month_number=11):     
    #takes timeseries as an imput, makes month-years dataframe, plots one row of it
    #now only works with mobths
    months_years_means=calculating_means(time_series,resolution)
    ToPlot=months_years_means.iloc[month_number,:] # to acess one row
    
    #plotting
    plt.figure()
    x =np.arange(len(ToPlot))
    plt.plot(x,ToPlot,'o')
    plt.xticks(list(np.arange(len(ToPlot))),months_years_means.columns.values.tolist())
    plt.xlim(x[0]-0.5,x[-1]+0.5)
    plt.show()    

Data=load_data('db.txt')
timeSeries=get_data(Data,1)
timeSeries=pd.TimeSeries(timeSeries)
plot_one_month_means(timeSeries)
print(get_statistics(timeSeries,resolution='month',function=finding_min,average=True))

#For now:

#Problem! whene averaging we obtain Series, max,idxmax work
#Without we have DataFrame, max,idmax doesn-t work

#average=False returns 
#1937    17.693548
#1938    16.806452
#1939    17.393548 ...

#1938     8
#1939     8
#1940     7

#average=True returns right thing

#dayofyear attribute returns 1...365? not day-month

#Plotting
#we can only plot months, also want years and days

##different kinds of plots...