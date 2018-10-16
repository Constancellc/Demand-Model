from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv

data = '../../Documents/national-charge-point-registry.csv'
# create new figure, axes instances.
fig=plt.figure(figsize=(6,8))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=58.7,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
locs = []
with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        try:
            locs.append([float(row[0]),float(row[1])])
        except:
            continue
m.drawcoastlines()
x = []
y = []
for loc in locs:
    xpt,ypt = m(loc[1],loc[0])
    x.append(xpt)
    y.append(ypt)

plt.scatter(x,y,c='b',s=4,marker='x')
plt.show()
