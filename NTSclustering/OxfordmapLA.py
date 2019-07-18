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
fig=plt.figure()#figsize=(8,6))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=58.7,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)

locs = {}
x = []
y = []


with open(locXY,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        lat,lon = transform(inProj,outProj,float(row[0]),float(row[1]))
        if lat < -1.9 or lat > -0.7:
            continue
        if lon < 51.4 or lon > 52.3:
            continue
        x_,y_ = m(lat,lon)
        x.append(x_)
        y.append(y_)
        locs[row[3]] = [lat,lon]
'''
with open(locLatLon,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LSOA','Lat','Lon'])
    for l in locs:
        writer.writerow([l]+locs[l])
'''
pList = []
z = []

limZ = 0
with open(stem+'lsoaPred.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] not in locs:
            continue
        pList.append(locs[row[0]])
        z.append(float(row[1])) # % increase
        if z[-1] > limZ:
            limZ = z[-1]
 
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
#x = np.arange(-1.7,-0.8,0.1)
#y = np.arange(51.4,52.2,0.1)
x = np.arange(-1.74,-0.8,0.005)
y = np.arange(51.45,52.19,0.005)

Z = np.zeros((len(x),len(y)))
X = np.zeros((len(x),len(y)))
Y = np.zeros((len(x),len(y)))

#x_l,y_h = m(-1.8785,52.1767)
#x_h,y_l = m(-0.7950,51.4568)
x_l,y_h = m(-1.7270,52.1761)
x_h,y_l = m(-0.8598,51.4579)

for i in range(len(x)):
    for j in range(len(y)):
        p = [x[i],y[j]]
        best = find_nearest(p)
        xpt,ypt = m(x[i],y[j])
        X[i,j] = xpt
        Y[i,j] = ypt
        Z[i,j] = z[best]


im = plt.imread('../../Downloads/oxfordshire.png')
plt.imshow(im,extent=[int(x_l),int(x_h),int(y_l),int(y_h)],alpha=0.3,zorder=3,
           cmap='Greys_r')
m.pcolor(X,Y,Z,vmin=0,vmax=40,cmap='Blues',zorder=2)
#ax2=fig.add_axes([x_h*1.05,y_l*1.05,0.025,0.08])
plt.colorbar()#cax=ax2)
plt.xlim(x_l+1,x_h-1)
plt.ylim(y_l+1,y_h-1)
plt.savefig('../../Dropbox/thesis/chapter6/img/Oxfordshire.pdf', format='pdf',
            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
