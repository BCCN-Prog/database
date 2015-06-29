import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
import click
import datetime
import calendar
from weather_loading import load_dataframe

from pylab import rcParams
rcParams['figure.figsize'] = 20, 3 #setting plots size
 
def calculating_yearly_means(time_series,resolution='month'):
    '''

    :param time_series: pandas time series indexed with days
    :param resolution: 'month' or 'dayofyear' or 'year'
    :return DataFrame df[i,j] = mean of measure over resolution i of year j.
            if resolution is 'year' returns and years as rows.
    '''

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

def calculating_total_means(time_series,resolution='month'):
    '''
    :param time_series: pandas time series indexed with days
    :param resolution: 'month' or 'dayofyear' or 'year'
    :return: averaging over the years over calculating_yearly_means(time_series,resolution)
    '''
    new_frame=calculating_yearly_means(time_series,resolution)
    if resolution !='year':
        new_frame=new_frame.mean(axis=1) #calculating averages
    return new_frame

def finding_max(data_frame):
    '''
    :param data_frame: pandas dataFrame
    :return: the maximum and the index of the maximum for the data_frame
    '''

    if type(data_frame)==pd.core.frame.DataFrame:
        maximums, maximum_idces=data_frame.max(), data_frame.idxmax()
        maximum,maximum_idx_1=maximums.max(),maximums.idxmax()
        maximum_idx_2=maximum_idces.loc[maximum_idx_1]
        return maximum, maximum_idx_1,maximum_idx_2
    else:
        return data_frame.max(),data_frame.idxmax()


def finding_min(data_frame):
    '''
    :param data_frame: pandas dataFrame
    :return: the minimum and the index of the minimum for the data_frame
    '''

    if type(data_frame) == pd.core.frame.DataFrame:
        #if not averaging, the input is data frame
        #makes things more complicated
        minimums, minimum_idces=data_frame.min(), data_frame.idxmin()
        #finding minimums in rows
        minimum,minimum_idx_1=minimums.min(),minimums.idxmin()
        #finding absolute minimum, it's first index
        minimum_idx_2=minimum_idces.loc[minimum_idx_1]
        #finding it's second index
        return minimum, minimum_idx_1, minimum_idx_2
    else: #if after averaging, the input is series
        return data_frame.min(),data_frame.idxmin()


def get_statistics(time_series,resolution='month',function=finding_min, average=True):
    '''
    :param time_series: pandas time series indexed with days
    :param resolution: 'month' or 'dayofyear' or 'year'
    :param function: finding_min or finding_ax
    :param average: Boolean
    :return: function(time_series) according to resolution.
    '''
<<<<<<< Updated upstream
=======
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

def finding_maximum(data_frame):
    index = data_frame.unstack()[data_frame.unstack().argsort()].index[-1:]
    return index
    
def get_statistics(time_series,resolution='month',function=finding_min,average=True):
>>>>>>> Stashed changes
    #function to find max/min averages/in total
    if average:
<<<<<<< Updated upstream
        new_frame=calculating_total_means(time_series,resolution)
    #calculating averages
    else:
        new_frame=calculating_yearly_means(time_series,resolution)
    return function(new_frame)

def plot_means(time_series, resolution='month', number=1):
    #takes timeseries as an input, makes resolution-years dataframe
    #returns list of years, list of mean values for one row
    new_frame=calculating_yearly_means(time_series,resolution)
    if type(new_frame) == pd.core.frame.DataFrame:
        ToPlot = new_frame.iloc[number] # to acess one row,
    else:
        ToPlot = new_frame #if we are dealing with years
    plotting_indices = ToPlot.index.tolist()
    #get years
    return plotting_indices,ToPlot

def plot_res(data_slice, resolution, startyear, endyear):
    if resolution == 'month':
        months = ["January", "February", "March", "April", "May", "June", "July"\
                        , "August", "September", "October", "November", "December"]
        month = input("Which month would you like to plot? Give a number 1-12: ")
        month = int(month) - 1
        plt.xlabel("Measures for each " + months[month])
        plt.xticks(np.arange(startyear, endyear), np.arange(startyear, endyear).astype(str))
        x, y = plot_means(data_slice, resolution, month)

    elif resolution == 'dayofyear':
        day = input("Which day of the year would you like to plot? Give a number 1-366: ")
        day = int(day) - 1

        plt.xlabel("Day #" + str(day) + " for each year")
        plt.xticks(np.arange(startyear, endyear), np.arange(startyear, endyear).astype(str))

        x, y = plot_means(data_slice, resolution, day)

    elif resolution == 'year':
        x, y = plot_means(data_slice, resolution, 0) #number doesn't matter

    plt.plot(x,y, 'o')
    plt.plot(x,y)
    plt.ylabel("Requested Measure")

    plt.show()

def compare_statistics(time_series,resolution='dayofweek',slice1=[0,5],slice2=[5,7]):
    '''
    :param time_series: pandas time series indexed with days
    :param resolution: 'month' or 'dayofyear' or 'year' (makes sence only with 'dayofyear')
    :param slice1: list of dayofweek as int to compare
    :param slice2: another list of dayofweek as int to compare
    :return: the mean of the data frame for each slice
    '''
    #comparing mean values in slice1 and slice2 with given resolution
    new_frame=calculating_total_means(time_series,resolution)
    #calculating total means
    statistics1=new_frame.iloc[slice1[0]:slice1[1]].mean()
    statistics2=new_frame.iloc[slice2[0]:slice2[1]].mean()
    return statistics1, statistics2

def compare_weather(time_series,resolution='dayofweek',slice1=[0,5],slice2=[5,7]):
    '''

    :param time_series: pandas time series indexed with days
    :param resolution: 'month' or 'dayofyear' or 'year' (makes sence only with 'dayofyear')
    :param slice1: list of dayofweek as int to compare
    :param slice2: another list of dayofweek as int to compare
    :return: statistics for each slice ver the measures - temperature, wind_speed, percipitaion and sun hours.
    '''
    temperature=compare_statistics(pd.TimeSeries(time_series.iloc[:,3]),resolution,slice1,slice2)
    wind_speed=compare_statistics(pd.TimeSeries(time_series.iloc[:,12]),resolution,slice1,slice2)
    precipitation=compare_statistics(pd.TimeSeries(time_series.iloc[:,13]),resolution,slice1,slice2)
    sunshine=compare_statistics(pd.TimeSeries(time_series.iloc[:,15]),resolution,slice1,slice2)
    return temperature,wind_speed,precipitation,sunshine

helpstring = """Enter the code of measure(s) you want to obtain.
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
16: Snow Height"""

@click.command()
@click.option('--id', type=click.STRING, default = '00131', \
              help="Enter the ID of the station whose data you would like to receive")
@click.option('--startyear', type=click.INT, default=2005, \
    help="Enter year that you want to begin your query as INT")
@click.option("--endyear", type=click.INT, default=2014, \
    help="Enter year that you want to begin your query as INT")
@click.option("--measure", type=click.INT, default=3, help=helpstring)
@click.option("--resolution", type=click.STRING, default="month", \
    help="Enter the time measure that you want. \n 'dayofyear', 'dayofweek', 'month' or 'year'")
@click.option("--function", type=click.STRING, default="min", \
    help="Enter the function you want to use. 'min' or 'max'")
@click.option("--average", type=click.BOOL, default=True, \
    help="Enter if you want the average of the given data")
@click.option("--plotting", type=click.BOOL, default=False, \
    help="Enter 'True' if you want to plot")
@click.option("--weekend_comparison", type=click.BOOL, default=False, \
    help="Enter 'True' if you want to compare between weekdays and weekend")

def main(id, startyear, endyear, measure, resolution, function, average, plotting, weekend_comparison):
    start = str(startyear) + '0101'
    end = str(endyear) + '3112'
    if len(id[0]) == 1:
        id = [id]

    func_dict = {'min':finding_min, 'max':finding_max}
    measures_dict = {4: 'DAMPFDRUCK', 3: 'Air Temperature', 5: 'BEDECKUNGSGRAD', 6: 'LUFTDRUCK_STATIONSHOEHE',\
                     7: 'REL_FEUCHTE', 8:'WINDGESCHWINDIGKEIT', 9: 'Max Air Temperature', 10: 'Min Air Temperature', \
                    11: 'LUFTTEMP_AM_ERDB_MINIMUM', 12: 'Max Wind Speed', 13: 'Precipitation Height', \
                     14: 'IEDERSCHLAGSHOEHE_IND', 15: 'Sunshine Duration', 16: 'now Height'}

    data = load_dataframe(id, start, end)
    for station in data:
        selected = data[station].iloc[:, measure]
    data_slice = pd.TimeSeries(selected)

    final_stats = get_statistics(data_slice, resolution, func_dict[function], average)

    average_message = ' on average' if average else ''
    value_message = 'the ' + function + ' for ' + measures_dict[measure] + ' is: ' + str(final_stats[0]) + average_message

    print()
    print(value_message)

    index_message = 'for '

    if resolution == 'dayofyear':
        if not average:
            print(index_message + str((datetime.datetime(final_stats[1], 1, 1) + \
                                   datetime.timedelta(int(final_stats[2]) - 1)).date()))
        else:
            print(index_message + 'the ' + str(final_stats[1]) + 'th day of the year')
    elif resolution == 'dayofweek':
        if not average:
            print(index_message + calendar.day_name[final_stats[2]] + 's during ' + str(final_stats[1]))
        else:
            print(index_message + calendar.day_name[final_stats[1]])
    else:
        if resolution == 'month':
            if average:
                month_name = datetime.date(1900, final_stats[1], 1).strftime('%B')
                index_message += month_name + ' '
                print(index_message)
            else:
                print(index_message + calendar.month_name[final_stats[2]] + ' ' + str(final_stats[1]))
        else:
            index_message += str(final_stats)
            print(index_message)

    if weekend_comparison:
        comparison = compare_weather(data[id[0]])
        print()
        for i, measure in enumerate(['Air Temperature', 'Max Wind Speed',  'Precipitation Height', 'Sunshine Duration']):
            message = 'on average the ' + measure + ' during the week is: ' + str(comparison[i][0]) \
                + ' and during the weekend is: ' + str(comparison[i][1])
            print(message)

    print()
    print('calculated from: ' + str(startyear) + ' to: ' + str(endyear))

    if plotting:
        print()
        plot_res(data_slice, resolution, startyear, endyear)
if __name__ == "__main__":
    main()
=======
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
print(timeSeries)

plot_one_month_means(timeSeries)
print(get_statistics(timeSeries,resolution='month',function=finding_min,average=True))
'''
print(Data)

print(finding_maximum(Data))
'''
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
>>>>>>> Stashed changes
