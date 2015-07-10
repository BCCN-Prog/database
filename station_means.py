import datetime
import os.path
from weather_loading import load_dataframe
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import click
import datetime


###For plotting the Germany mask
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
from shapely.prepared import prep
from shapely.ops import cascaded_union
import shapely.geometry as sgeom


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
	
	df = df.dropna()
	geo_df = read_dwd_city_list()

	X = df['geoBreite'].as_matrix().flatten()
	Y = df['geoLaenge'].as_matrix().flatten()
	
	geoX = geo_df['geoBreite'].as_matrix().flatten()
	geoY = geo_df['geoLaenge'].as_matrix().flatten()
	
	coordinates = np.array([X, Y]).T

	###Creating meshgrid to plot
	xmax = max(geoX); xmin = min(geoX)
	ymax = max(geoY); ymin = min(geoY)
	dt = 0.01
	dx = dy = dt

	OX = np.arange(xmin-dx,xmax+2*dx,dx)
	OY = np.linspace(ymin-dy,ymax+2*dy,len(OX))
	XX,YY = np.meshgrid(OX,OY)
	
	###Creating a mask
	
	shpfilename = shpreader.natural_earth(resolution='110m',
										  category='cultural',
										  name='admin_0_countries')

	reader = shpreader.Reader(shpfilename)
	countries = reader.records()
	de, = [country.geometry for country in countries
					 if country.attributes['name'] == 'Germany']
	MAF_region = cascaded_union([de])

	y, x = grid_points = np.mgrid[47.398:55.011:765j, 6.024:14.95:765j]
	mask = np.empty(x.shape, dtype=np.bool)

	MAF_prep = prep(MAF_region)
	
	for index in np.ndindex(x.shape):
		contains = MAF_prep.contains(sgeom.Point(x[index], y[index]))
		mask[index] = contains


	###Interpolation
	grid_z0 = griddata(coordinates, df['Time avg.'].as_matrix().flatten(),
					   (XX, YY), method='nearest')
	
	Z = np.ma.masked_array(grid_z0,
					   mask = ~mask) 
					   
	###Plotting
	plt.figure(figsize=(10,10))
	plt.pcolormesh(XX,YY,Z.T)
	plt.plot(X,Y,'ko')
	plt.colorbar()

	plt.show()


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
@click.option('--station', type=click.INT, multiple=True,
			  help="Enter the ID of the station whose data you would like to receive")
@click.option('--start_date', type=click.STRING, default='20150101',
			  help="Enter the start date of the average.")
@click.option('--end_date', type=click.STRING, default='20150606',
			  help="Enter the end date of the average.")
@click.option("--measure", type=click.INT, default=2, help=helpstring)
@click.option('--station_list', type=click.STRING, default='downloaded_data/DWD_city_list.txt',
			  help='Enter the path to the DWD stations list file')

def main(station, start_date, end_date, measure, station_list):

	# empty tuple != None
	if not station:
		station = None

	heatmap_germany(station, measure=measure,
					start_date=datetime.datetime.strptime(start_date, '%Y%m%d'),
					end_date=datetime.datetime.strptime(end_date, '%Y%m%d'), fname=station_list)

if __name__ == "__main__":
	main()
