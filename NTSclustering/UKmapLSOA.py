from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv
from pyproj import Proj, transform

inProj = Proj(init='epsg:27700')
outProj = Proj(init='epsg:4326')


stem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'
locXY = '../../Documents/census/centroids-LSOA.csv'
locLatLon = '../../Documents/census/centroids-LSOA-LatLon.csv'
# create new figure, axes instances.
fig=plt.figure(figsize=(6,8))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=55.5,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)


#m.drawcoastlines()
x = []
y = []
#            rsphere=(6378137.00,6356752.3142),\
# get locations
locs = {}
with open(locXY,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        lat,lon = transform(inProj,outProj,float(row[0]),float(row[1]))
        x_,y_ = m(lat,lon)
        x.append(x_)
        y.append(y_)
        locs[row[3]] = [lat,lon]

with open(locLatLon,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LSOA','Lat','Lon'])
    for l in locs:
        writer.writerow([l]+locs[l])

print('DONE')

#plt.scatter(x,y)
#plt.show()
pList = []
z = []

limZ = 0
with open(stem+'lsoaPred.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        pList.append(locs[row[0]])
        z.append(float(row[1])) # % increase
        if z[-1] > limZ:
            limZ = z[-1]
        
'''    
for l in locs:
    try:
    with open(stem+l+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            pList.append(locs[row[0]])
            z.append(100*(float(row[2])-float(row[1]))/float(row[1]))
'''
def find_nearest(p1):
    closest = 0.2
    best = None

    for ii in range(len(pList)):
        p = pList[ii]
        d = np.sqrt(np.power(p[0]-p1[0],2)+np.power(p[1]-p1[1],2))
        if d < closest:
            closest = d
            best = ii

    return best

# make these smaller to increase the resolution
x = np.arange(-7,3,0.02)
y = np.arange(49,56.5,0.02)

Z = np.zeros((len(x),len(y)))
X = np.zeros((len(x),len(y)))
Y = np.zeros((len(x),len(y)))
m.drawcoastlines()
for i in range(len(x)):
    for j in range(len(y)):
        p = [x[i],y[j]]
        
        #xpt = x[i]
        #ypt = y[j]
        xpt,ypt = m(x[i],y[j])
        X[i,j] = xpt
        Y[i,j] = ypt
        if m.is_land(xpt,ypt) == True:
            if xpt < 200000 and ypt < 970000 and ypt > 300000:
                continue
            if xpt > 885000 and ypt < 175000:
                continue
            if xpt > 766000 and ypt < 104000:
                continue
            best = find_nearest(p)
            if best != None:
                Z[i,j] = z[best]
        else:
            continue

m.pcolor(X,Y,Z,vmax=90)

plt.colorbar()
#plt.savefig('../../Dropbox/papers/uncontrolled/img/UK_.eps', format='eps',
#            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
