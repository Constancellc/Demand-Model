from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv

stem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'
stem2 = '../../Documents/elec_demand/'
# create new figure, axes instances.
fig=plt.figure(figsize=(6,8) )
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=58.7,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)


#            rsphere=(6378137.00,6356752.3142),\
# get locations
locs = {}
with open(stem+'LA-lat-lon.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[1]] = [float(row[3]),float(row[2])]

ind = {}
dom = {}

with open(stem2+'MSOA_non-domestic_electricity_2017.csv','r',
          encoding="ISO-8859-1") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        l = row[1].replace(' ','')
        if l not in ind:
            ind[l] = 0
            dom[l] = 0
        try:
            ind[l] += float(row[4].replace(',',''))
        except:
            continuw

with open(stem2+'MSOA_domestic_electricity_2017.csv','r',
          encoding="ISO-8859-1") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        l = row[1].replace(' ','')
        if l not in dom:
            dom[l] = 0
            ind[l] = 0
        try:
            dom[l] += float(row[4].replace(',',''))
        except:
            continue

e7 = 0
std = 0
with open(stem2+'MSOA_domestic_electricity_2016.csv','r',
          encoding="ISO-8859-1") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        try:
            e7 += float(row[5])
            std += float(row[4])
        except:
            continue

print(e7/(e7+std))
        
pList = []
z = []

totalI = 0
totalD = 0
limZ = 0
for l in dom:
    totalI += ind[l]
    totalD += dom[l]
    try:
        pList.append(locs[l])
    except:
        print(l)
        continue
    z.append(100*ind[l]/(ind[l]+dom[l]))
    if z[-1] > limZ:
        limZ = z[-1]

print(totalI)
print(totalD)
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
x = np.arange(-7,3,0.025)
y = np.arange(49,59,0.025)

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
            if xpt < 200000 and ypt < 970000 and ypt > 300000:
                continue
            if xpt > 885000 and ypt < 175000:
                continue
            if xpt > 766000 and ypt < 104000:
                continue
            Z[i,j] = z[best]
        else:
            continue

m.pcolor(X,Y,Z,vmin=30,vmax=80)#,cmap='inferno')
#m.pcolormesh(x,y,Z,latlon=True)
#m.drawmapboundary(fill_color='#99ffff')
#m.drawlsmask(land_color='coral',ocean_color='aqua')
# draw parallels
#m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# draw meridians
#m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
plt.colorbar()
#plt.savefig('../../Dropbox/papers/d.eps', format='eps',
#            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
