import datetime
from weather_loading import load_dataframe

def station_mean_measure(cities, measure=2,
                         start_date=(datetime.datetime.now()-datetime.timedelta(datetime.datetime.now().weekday(), weeks=1)),
                         end_date=datetime.datetime.now(),
                         fname='downloaded_data/DWD_city_list.txt'):

    # Calculate means over the time range for the given stations
    data = load_dataframe(cities, datetime.datetime.strftime(start_date, '%Y%m%d'),
                          datetime.datetime.strftime(end_date, '%Y%m%d'))
    station_means = {}
    for key in data:
        station_means[key] = data[key].iloc[:, measure].mean()

    # Read coordinates for the stations
    #df = pd.read_fwf(fname, colspecs=colspecs, header=0)


stations = ['00071', '00161']
station_mean_measure(stations)