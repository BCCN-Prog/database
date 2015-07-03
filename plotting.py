import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import operator
import click
import datetime
import calendar
from weather_loading import load_dataframe
from scipy.stats import linregress

from pylab import rcParams
rcParams['figure.figsize'] = 20, 3 #setting plots size
 
def calculating_yearly_means(time_series,resolution='month'):
    '''

    :param time_series: pandas time series indexed with days
    :param resolution: 'month' or 'dayofyear' or 'year'
    :return DataFrame df[i,j] = mean of measure over resolution i of year j.
            if resolution is 'year' returns and years as rows.
    '''

    years = range(time_series.index.year[0], time_series.index.year[-1]+1)
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
        ToPlot = new_frame.iloc[number] # to acess one row,
    else:
        ToPlot = new_frame #if we are dealing with years
    plotting_indices = ToPlot.index.tolist()
    #get years
    return plotting_indices,ToPlot

def plot_res(data_slice, resolution, startyear, endyear, measure = "Requested Measure"):
    
    
    if resolution == 'month':
        months = ["January", "February", "March", "April", "May", "June", "July"\
                        , "August", "September", "October", "November", "December"]
        month = input("Which month would you like to plot? Give a number 1-12: ")
        month = int(month) - 1
        plt.xlabel("Measures for each " + months[month])
        #plt.xticks(np.arange(startyear, endyear), np.arange(startyear, endyear).astype(str))
        x, y = plot_means(data_slice, resolution, month)

    elif resolution == 'dayofyear':
        day = input("Which day of the year would you like to plot? Give a number 1-366: ")
        day = int(day) - 1

        plt.xlabel("Day #" + str(day) + " for each year")
        #plt.xticks(np.arange(startyear, endyear), np.arange(startyear, endyear).astype(str))

        x, y = plot_means(data_slice, resolution, day)

    elif resolution == 'year':
        x, y = plot_means(data_slice, resolution, 0) #number doesn't matter

    cols = plt.rcParams['axes.color_cycle']
    
    cred = '#E24A33'
    cblue = '#83A1F2'#'#348ABD'
    cpurple = '#988ED5'
    cgray = '#A8A8A9'#'#777777'
    cyellow = '#FBC15E'
    cgreen = '#53C955'#'#8EBA42'
    cpink = 'Salmon' #'#FFB5B8'
    
    if measure.endswith('temperature'):
        if np.nanmean(y) > 10:
            use_color = cpink
        else:
            use_color = cblue
        
    
    plt.axhline(np.nanmean(y),color = cgray, label = 'mean')    

    plt.plot(x,y, 'o', color = use_color)
    plt.plot(x,y, color = use_color)


    y_isfinite = np.isfinite(np.array(y))
    y_regress  = np.array(y)[y_isfinite]
    x_regress  = np.array(x)[y_isfinite]
    # regression line
    if (len(x_regress) >= 10) and (len(y_regress)/len(x) >= 0.8):
        slope, intercept, r_value, p_value, std_err = linregress(x_regress,y_regress)
        plt.plot(np.array(x_regress), intercept+slope*np.array(x_regress), '--',color = cgreen, label = 'regression line, slope = %.4f, p-value = %.4f' %(slope,p_value) )
        plt.legend(loc = 'best')


    plt.xlabel("Year")
    #yrs = np.linspace(startyear, endyear, 5, dtype=int)
   

    yeardif = np.max(x) - np.min(x)
    
    if yeardif < 10:
        yrs = np.arange(np.min(x), np.max(x))
        plt.xticks(yrs, yrs.astype(str))
    elif yeardif < 50:          
        yrs = np.arange(np.min(x), np.max(x)+5, 5, dtype=int)    
        yrs[-1] = min(yrs[-1], np.max(x))
        plt.xticks(yrs, yrs.astype(str))
    else:
        #yrs = np.arange(startyear, endyear+10, 10, dtype=int)    
        yrs = np.linspace(np.min(x), np.max(x), 10, dtype=int)        
        yrs[-1] = min(yrs[-1], np.max(x))
        plt.xticks(yrs, yrs.astype(str))
    

    plt.ylabel(measure)
    plt.xlim(np.min(x), np.max(x))

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
0: station ID
1: quality level
2: air temperature
3: vapor pressure
4: degree of coverage
5: air pressure
6: relative humidity
7: wind speed
8: maximum air temperature
9: minimum air temperature
10: minimum groundlevel temperature
11: maximum wind speed
12: precipitation height
13: precipitation ind (we don't really know what this is..)
14: hours of sun
15: depth of snow"""

@click.command()
@click.option('--id_stat', type=click.STRING, default = ['06337','00070'], \
              help="Enter the ID of the station whose data you would like to receive")
@click.option('--startyear', type=click.INT, default=1950, \
    help="Enter year that you want to begin your query as INT")
@click.option("--endyear", type=click.INT, default=2014, \
    help="Enter year that you want to begin your query as INT")
@click.option("--measure", type=click.INT, default=2, help=helpstring)
@click.option("--resolution", type=click.STRING, default="month", \
    help="Enter the time measure that you want. \n 'dayofyear', 'dayofweek', 'month' or 'year'")
@click.option("--function", type=click.STRING, default="min", \
    help="Enter the function you want to use. 'min' or 'max'")
@click.option("--average", type=click.BOOL, default=True, \
    help="Enter if you want the average of the given data")
@click.option("--plotting", type=click.BOOL, default=True, \
    help="Enter 'True' if you want to plot")
@click.option("--weekend_comparison", type=click.BOOL, default=False, \
    help="Enter 'True' if you want to compare between weekdays and weekend")

def main(id_stat, startyear, endyear, measure, resolution, function, average, plotting, weekend_comparison):
    start = str(startyear) + '0101'
    end = str(endyear+1) + '0101'
    #if len(id[0]) == 1:
    #    id = [id]

    func_dict = {'min':finding_min, 'max':finding_max}
    measures_dict = {3: 'vapor pressure', 2: 'air temperature', 4: 'degree of coverage', 5: 'air pressure',\
                     6: 'relative humidity', 7:'wind speed', 8: 'maximum air temperature', 9: 'minimum air temperature', \
                    10: 'minimum groundlevel temperature', 11: 'maximum wind speed', 12: 'precipitation height', \
                     13: 'precipitation ind', 14: 'hours of sun', 15: 'depth of snow'}

    data = load_dataframe(id_stat, start, end, matching_stations=True)
       
    data_slice=pd.concat([data[station].iloc[:, measure] for station in data],axis=1)
    print(data_slice)
    
    data_slice=data_slice.mean(axis=1)
    data_slice = pd.TimeSeries(data_slice)
    
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
        plot_res(data_slice, resolution, startyear, endyear, measures_dict[measure])
if __name__ == "__main__":
    main()
