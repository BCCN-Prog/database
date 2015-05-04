#Doesn't work properly, need TimeSeries!

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

def get_data(data, station_id, category = 3):
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
    
    return selected
    
def calculating_means(time_series): #for now: mean for each month in different years
    #returns dataframe with years-columns, months-rows, elements - mean values for months
    
    years = range(time_series.index.year[0], time_series.index.year[-1]) #period 
    yearly_month_stats = [time_series.xs(str(year)).groupby(lambda x : x.month).mean() for year in years]
    df2 = pd.concat(yearly_month_stats, axis=1, keys = years)
    
    return df2

def plot_one_month_means(time_series, month_number=3): 
    #takes timeseries as an imput, makes month-years dataframe, plots one row of it
    
    months_years_means=calculating_means(time_series)
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

#Error
#years = range(time_series.index.year[0], time_series.index.year[-1]) #period 
#AttributeError: 'Index' object has no attribute 'year'

##different kinds of plots...