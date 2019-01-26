from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv

stem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'
# create new figure, axes instances.
fig=plt.figure(figsize=(6,8) )
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=58.7,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)


locs = {}
with open(stem+'LA-lat-lon.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[1]] = [float(row[3]),float(row[2])]

pList = []
z = []

limZ = 0
with open(stem+'peaks.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        pList.append(locs[row[0]])
        #z.append(float(row[2])) # kW 1- before 2- after
        z.append(100*(float(row[2])-float(row[1]))/float(row[1])) # % incr
        if z[-1] > limZ:
            limZ = z[-1]
        

def find_nearest(p1):
    closest = 100000
    best = None

    for ii in range(len(pList)):
        p = pList[ii]
        d = np.power(p[0]-p1[1],2)+np.power(p[1]-p1[0],2)
        if d < closest:
            closest = d
            best = ii

    return best

# make these smaller to increase the resolution
x = np.arange(-1.87,-0.8,0.01)
y = np.arange(51.46,52.18,0.01)

Z = np.zeros((len(x),len(y)))
X = np.zeros((len(x),len(y)))
Y = np.zeros((len(x),len(y)))

x_l,y_h = m(-1.8785,52.1767)
x_h,y_l = m(-0.7950,51.4568)

for i in range(len(x)):
    for j in range(len(y)):
        p = [x[i],y[j]]
        best = find_nearest(p)
        xpt,ypt = m(x[i],y[j])
        X[i,j] = xpt
        Y[i,j] = ypt
        Z[i,j] = z[best]
plt.imshow('oxfordshire.png',extent=[x_l,x_h,y_l,y+h])
m.pcolor(X,Y,Z,vmax=limZ,alpha=0.2)
plt.xlim(x_l,x_h)
plt.ylim(y_l,y_h)
plt.colorbar()
plt.show()
