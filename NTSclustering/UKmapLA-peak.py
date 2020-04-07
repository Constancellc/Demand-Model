from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import matplotlib.cbook
import csv

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

blues = cm.get_cmap('Blues', 1000)
new = blues(np.linspace(0, 1, 1000))
new[:1,:] =  np.array([1,1,1,1])
blue2 = ListedColormap(new)

stem = '../../Documents/simulation_results/'
# create new figure, axes instances.



#            rsphere=(6378137.00,6356752.3142),\
# get locations
locs = {}
with open(stem+'LA-lat-lon.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[1]] = [float(row[3]),float(row[2])]

pList = []
z = [[],[],[]]
z2 = []
z3 = []

with open(stem+'peaks.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        pList.append(locs[row[0]])
        z[0].append(50*(float(row[2])-float(row[1]))) # kW 1- before 2- after
        z[1].append(float(row[2]))
        z[2].append(float(row[3]))
        #z.append(100*(float(row[2])-float(row[1]))/float(row[1])) # % incr
        
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

fig=plt.figure(figsize=(4.5,5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
largest = 0
titles = ['No Charging','Uncontrolled','Controlled']
for pn in range(1):
    #plt.subplot(1,3,pn+1)
    #plt.title(titles[pn])
    ax = plt.gca()
    #ax=fig.add_axes([0.1,0.1,0.8,0.8])
    # setup mercator map projection.
    m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=58.7,\
                resolution='h',projection='merc',\
                lat_0=40.,lon_0=-20.,lat_ts=20.)
    # make these smaller to increase the resolution
    x = np.arange(-7,3,0.02)
    y = np.arange(49,59,0.02)

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
                Z[i,j] = z[pn][best]
                if z[pn][best] > largest:
                    largest = z[pn][best]
            else:
                continue

    im = m.pcolor(X,Y,Z,vmin=0,vmax=70,cmap=blue2)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
print(largest)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/peak.eps', format='eps', dpi=1000,
            bbox_inches='tight', pad_inches=0)
plt.show()
