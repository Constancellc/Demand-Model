from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv

stem = '../../Documents/simulation_results/NTS/clustering/power/locations/'
# create new figure, axes instances.
fig=plt.figure(figsize=(12, 8) )
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7.5,llcrnrlat=49.7,urcrnrlon=2.8,urcrnrlat=59.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)


# get locations
locs = {}
with open(stem+'county-centroids.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[0]] = [float(row[1]),float(row[2])]

pList = []
z = []
for l in locs:
    with open(stem+l+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        s = []
        for row in reader:
            s.append(float(row[1])/50)
        z.append(max(s))
        pList.append(locs[l])
        
'''
        if s > 1.5:
            x1.append(locs[l][1])
            y1.append(locs[l][0])

        elif s > 1.2:
            x2.append(locs[l][1])
            y2.append(locs[l][0])

        elif s > 1:
            x3.append(locs[l][1])
            y3.append(locs[l][0])

        else:
            x4.append(locs[l][1])
            y4.append(locs[l][0])


    
m.scatter(x1,y1,latlon=True,c='r')
m.scatter(x2,y2,latlon=True,c='y')
m.scatter(x3,y3,latlon=True,c='g')
m.scatter(x4,y4,latlon=True,c='b')
'''

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
x = np.arange(-7,3,0.1)
y = np.arange(49,59,0.1)

Z = np.zeros((len(x),len(y)))

for i in range(len(x)):
    for j in range(len(y)):
        p = [x[0],y[j]]
        best = find_nearest(p)
        Z[i,j] = z[best]

'''
dx, dy = 0.1, 0.1
y, x = np.mgrid[slice(49, 59 + dy, dy),
                slice(-7, 3 + dx, dx)]
'''
m.pcolormesh(x,y,Z,latlon=True)
m.drawcoastlines()
# draw parallels
#m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# draw meridians
#m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
plt.show()
