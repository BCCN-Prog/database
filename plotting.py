import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
import click
import datetime
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
        return minimum, minimum_idx_1,minimum_idx_2
    else: #if after averaging, the input is series
        return data_frame.min(),data_frame.idxmin()


def get_statistics(time_series,resolution='month',function=finding_min,average=True):
    #function to find max/min averages/in total
    if average:
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
        ToPlot=new_frame.iloc[number] # to acess one row,
    else:
        ToPlot=new_frame #if we are dealing with years
    plotting_indices=ToPlot.index.tolist()
    #get years
    return plotting_indices,ToPlot

def compare_statistics(time_series,resolution='dayofweek',slice1=[0,5],slice2=[5,7]):
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
@click.option('--id', type=click.STRING, help="Enter the ID of the station whose data you would like to receive")
@click.option('--startyear', type=click.INT, default=1980, \
    help="Enter year that you want to begin your query as INT")
@click.option("--endyear", type=click.INT, default=1981, \
    help="Enter year that you want to begin your query as INT")
@click.option("--measure", type=click.INT, default=3, help=helpstring)
@click.option("--resolution", type=click.STRING, default="month", \
    help="Enter the time measure that you want. \n 'dayofyear', 'month' or 'year'")
@click.option("--function", type=click.STRING, default="min", \
    help="Enter the function you want to use. 'min' or 'max'")
@click.option("--average", type=click.BOOL, default=True, \
    help="Enter if you want the average of the given data")

def main(id, startyear, endyear, measure, resolution, function, average):

    start = str(startyear) + '0101'
    end = str(endyear) + '3112'
    if len(id[0]) == 1:
        id = [id]

    func_dict = {'min':finding_min, 'max':finding_max}

    data_slice = get_data(id, measure, start, end)

    final_stats = get_statistics(data_slice, resolution, func_dict[function], average)

    if resolution == 'dayofyear':
        print(final_stats[0])
        print((datetime.datetime(final_stats[1], 1, 1) + datetime.timedelta(int(final_stats[2]) - 1)).date())
    else:
        print(final_stats)
    return final_stats

if __name__ == "__main__":
    main()