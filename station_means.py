import datetime
from weather_loading import load_dataframe
import pandas as pd

def read_dwd_city_list(fname='downloaded_data/DWD_city_list.txt'):
    colspecs = [(0, 11),(12, 21),(21, 31),(32, 45),(46,55),(56,65),(66,107),(108,128)]
    df = pd.read_fwf(fname, colspecs=colspecs, header=0, encoding='Latin-1')

    # Remove the line with lines
    df = df.drop(df.index[0])

    # Remove the last line; it is EOF.
    df = df.drop(df.index[-1])

    # Use correct data types
    df[['Stationshoehe', 'geoBreite', 'geoLaenge']] = df[['Stationshoehe', 'geoBreite', 'geoLaenge']].astype(float)
    df[['Stations_id']] = df[['Stations_id']].astype(int)

    # Use Stations_ID as index
    df = df.set_index(['Stations_id'])

    return df


def station_mean_measure(cities, measure=2,
                         start_date=(datetime.datetime.now()-datetime.timedelta(datetime.datetime.now().weekday(), weeks=1)),
                         end_date=datetime.datetime.now()):

    # Calculate means over the time range for the given stations
    data = load_dataframe(cities, datetime.datetime.strftime(start_date, '%Y%m%d'),
                          datetime.datetime.strftime(end_date, '%Y%m%d'))
    df = pd.DataFrame(columns=('Stations_id', 'Time avg.'))
    for i, key in enumerate(data):
        df.loc[i] = [key, data[key].iloc[:, measure].mean()]

    df = df.set_index(['Stations_id'])

    return df


stations = ['00071', '00161']
df = read_dwd_city_list()
df2 = station_mean_measure(stations)
print(df2)