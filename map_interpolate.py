import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


###Reading the city list
fname = 'downloaded_data/DWD_city_list.txt'
colspecs = [(0, 11),(12, 21),(21, 31),(32, 45),(46,55),(56,65),(66,107),(108,128)]
df = pd.read_fwf(fname, colspecs=colspecs, header=0)#, index_col=0)
df = df.drop(df.index[0])
df = df.drop(df.index[-1])

###Test fragment of code for plotting only for stations from s:
s = [1,3,44,161,184,202,211,217,129,132,2,45,56,77,432,66,435,75,87,778]
stations = [str(i) for i in s]
df2 = df[df.Stations_id.isin(stations)]


###Here the subset of stations can be selected to be plotted
#df = df2


###Getting gps positions
y = df.as_matrix(columns=['geoBreite']).flatten()
x = df.as_matrix(columns=['geoLaenge']).flatten()

X = np.array([float(i) for i in x])
Y = np.array([float(i) for i in y])

Nstations = len(X)
coordinates = np.array([X,Y]).T


###Getting values to plot
Temp = np.random.randint(0, 30, len(X))


###Creating meshgrid to plot
xmax = max(X); xmin = min(X); xl = xmax-xmin
ymax = max(Y); ymin = min(Y); yl = xmax-xmin
dt = 0.01
dx = dy = dt

OX = np.arange(xmin-dx,xmax+2*dx,dx)
OY = np.linspace(ymin-dy,ymax+2*dy,len(OX))
XX,YY = np.meshgrid(OX,OY)

###Interpolation
grid_z0 = griddata(coordinates, Temp, (XX, YY), method='nearest')


###Plotting
plt.figure(figsize=(10,10))
plt.pcolormesh(XX,YY,grid_z0.T)
plt.plot(X,Y,'ko')
plt.colorbar()

plt.show()

