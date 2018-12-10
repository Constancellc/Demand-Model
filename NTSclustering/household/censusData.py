from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv
import utm

'''
plt.figure()
plt.scatter(x,y)
plt.show()
'''
# create new figure, axes instances.
fig=plt.figure(figsize=(12, 8))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7.5,llcrnrlat=49.7,urcrnrlon=2.8,urcrnrlat=59.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)

stem = '../../../Documents/census/'
# get locations
x = []
y = []
locs = {}
with open(stem+'centroids-MSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        
        try:
            ll = utm.to_latlon(float(row[1]),float(row[0]),29,'N')
            print(ll)
            p = m(ll[0],ll[1])
        except:
            continue
        x.append(p[0])
        y.append(p[1])
        locs[row[3]] = [float(row[1]),float(row[2])]


m.drawcoastlines()
plt.scatter(x,y)
plt.show()
plt.show()

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
x = np.arange(-7,3,0.05)
y = np.arange(49,59,0.05)

Z = np.zeros((len(x),len(y)))
X = np.zeros((len(x),len(y)))
Y = np.zeros((len(x),len(y)))
m.drawcoastlines()
for i in range(len(x)):
    for j in range(len(y)):
        p = [x[i],y[j]]
        best = find_nearest(p)
        xpt,ypt = m(x[i],y[j])
        X[i,j] = xpt
        Y[i,j] = ypt
        if m.is_land(xpt,ypt) == True:
            if xpt < 200000 and ypt < 970000:
                continue
            if xpt > 950000 and ypt < 235000:
                continue
            if xpt > 766000 and ypt < 104000:
                continue
            Z[i,j] = z[best]
        else:
            continue



m.pcolor(X,Y,Z)
#m.pcolormesh(x,y,Z,latlon=True)
#m.drawmapboundary(fill_color='#99ffff')
#m.drawlsmask(land_color='coral',ocean_color='aqua')
# draw parallels
#m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# draw meridians
#m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
plt.colorbar()
plt.show()

