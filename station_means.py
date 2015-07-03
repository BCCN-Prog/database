import datetime
import os.path
from weather_loading import load_dataframe
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


def read_dwd_city_list(fname=os.path.join('downloaded_data', 'DWD_city_list.txt')):
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
    df.sort_index(inplace=True)

    return df


def station_mean_measure(stations=None, measure=2,
                         start_date=(datetime.datetime.now()-datetime.timedelta(datetime.datetime.now().weekday(), weeks=1)),
                         end_date=datetime.datetime.now(),
                         fname=os.path.join('downloaded_data', 'DWD_city_list.txt')):

    df_city_list = read_dwd_city_list(fname)

    if stations is None:
        df = read_dwd_city_list(fname)
        stations = [int(i) for i in df.index]

    # load_dataframe expects a string
    if type(stations[0]) == int:
        stations = ["%05d" % i for i in stations]

    # Calculate means over the time range for the given stations
    data = load_dataframe(stations, datetime.datetime.strftime(start_date, '%Y%m%d'),
                          datetime.datetime.strftime(end_date, '%Y%m%d'))
    df = pd.DataFrame(columns=('Stations_id', 'Time avg.'))
    for i, key in enumerate(data):
        df.loc[i] = [int(key), data[key].iloc[:, measure].mean()]

    df[['Stations_id']] = df[['Stations_id']].astype(int)
    df = df.set_index(['Stations_id'])
    df[['geoBreite', 'geoLaenge']] = df_city_list.loc[df.index, ['geoBreite', 'geoLaenge']]
    df.sort_index(inplace=True)

    return df


def heatmap_germany(stations=None,
                    measure=2,
                    start_date=(datetime.datetime.now()-datetime.timedelta(datetime.datetime.now().weekday(), weeks=1)),
                    end_date=datetime.datetime.now(),
                    fname=os.path.join('downloaded_data', 'DWD_city_list.txt')):

    df = station_mean_measure(stations, measure=measure,
                              start_date=start_date,
                              end_date=end_date,
                              fname=fname)
    df.dropna()

    X = df['geoBreite'].as_matrix().flatten()
    Y = df['geoLaenge'].as_matrix().flatten()
    coordinates = np.array([X, Y]).T

    ###Creating meshgrid to plot
    xmax = max(X); xmin = min(X)
    ymax = max(Y); ymin = min(Y)
    dt = 0.01
    dx = dy = dt

    OX = np.arange(xmin-dx,xmax+2*dx,dx)
    OY = np.linspace(ymin-dy,ymax+2*dy,len(OX))
    XX,YY = np.meshgrid(OX,OY)

    ###Interpolation
    grid_z0 = griddata(coordinates, df['Time avg.'].as_matrix().flatten(),
                       (XX, YY), method='nearest')


    ###Plotting
    plt.figure(figsize=(10,10))
    plt.pcolormesh(XX,YY,grid_z0.T)
    plt.plot(X,Y,'ko')
    plt.colorbar()

    plt.show()


stations = [71, 161]
heatmap_germany(stations)