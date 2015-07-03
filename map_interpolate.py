import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

from scipy import interpolate

#def plot_map(stations, data)

###Reading the city list
fname = 'downloaded_data/DWD_city_list.txt'
colspecs = [(0, 11),(12, 21),(21, 31),(32, 45),(46,55),(56,65),(66,107),(108,128)]
df = pd.read_fwf(fname, colspecs=colspecs, header=0)
df = df.drop(df.index[0])
df = df.drop(df.index[-1])
df[['Stations_id', 'geoBreite', 'geoLaenge']] = df[['Stations_id', 'geoBreite', 'geoLaenge']].astype(float)

###Test fragment of code for plotting only for stations from s:
stations = [1,3,44,161,184,202,211,217,129,132,2,45,56,77,432,66,435,75,87,778]
df2 = df[df.Stations_id.isin(stations)]

###Here the subset of stations can be selected to be plotted
#df = df2


###Getting gps positions
Y = df.as_matrix(columns=['geoBreite']).flatten()
X = df.as_matrix(columns=['geoLaenge']).flatten()

Nstations = len(X)
coordinates = np.array([X,Y]).T


###Getting values to plot
Temp = np.random.randint(0, 30, len(X))


###Creating meshgrid to plot
xmax = max(X); xmin = min(X); xl = xmax-xmin
ymax = max(Y); ymin = min(Y); yl = ymax-ymin
dt = 0.01
dx = dy = dt

OX = np.arange(xmin-2*dx,xmax+2*dx,dx)
OY = np.linspace(ymin-2*dy,ymax+2*dy,len(OX))
XX,YY = np.meshgrid(OX,OY)

###Interpolation
grid_z0 = griddata(coordinates, Temp, (XX, YY), method='nearest')

###Interpolation method 2


###Plotting
plt.figure(figsize=(10,10))
plt.pcolormesh(XX,YY,grid_z0.T)
#plt.imshow(grid_z0)
plt.plot(X,Y,'ko')
plt.colorbar()

plt.show()

