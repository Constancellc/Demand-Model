from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv

plt.figure()
plt.bar(range(1,26),[350,406,432,551,358,292,223,508,341,664,292,424,300,394,
                      440,431,317,427,540,104,398,924,344,297,429])
plt.xlabel('Network')
plt.ylabel('m2 per household')
plt.grid()
plt.show()
stem = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'
stem2 = '../../../Documents/census/'
# get locations
fig=plt.figure(figsize=(4,6))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.,urcrnrlat=58.7,\
            resolution='l',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
locs = {}
with open(stem+'LA-lat-lon.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[1]] = [float(row[3]),float(row[2])]

pd = {}
x = []
y = []
with open(stem2+'population_density.csv','rU',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            pd[row[0]] = float(row[5])
            x.append(locs[row[0]][1])
            y.append(locs[row[0]][0])
        except:
            continue

z = []
pList = []
lList = []
for l in locs:
    try:
        p = pd[l]
    except:
        continue
    if p < 6:
        z.append(1)
    elif p < 27:
        z.append(2)
    else:
        z.append(3)
    lList.append(l)
    pList.append(locs[l])

with open(stem2+'LA_rural_urban.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LA Code','Classification (1-3)'])
    for i in range(len(z)):
        writer.writerow([lList[i],z[i]])
print(len(z))
        
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
    closest = 10000000
    best = None

    for ii in range(len(pList)):
        p = pList[ii]
        d = np.sqrt(np.power(p[0]-p1[1],2)+np.power(p[1]-p1[0],2))
        if d < closest:
            closest = d
            best = ii

    return best

# make these smaller to increase the resolution
x = np.arange(-7,3,0.5)
y = np.arange(49,59,0.5)

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

'''
dx, dy = 0.1, 0.1
y, x = np.mgrid[slice(49, 59 + dy, dy),
                slice(-7, 3 + dx, dx)]
'''

m.pcolor(X,Y,Z,cmap='Blues',vmin=0)
#m.pcolormesh(x,y,Z,latlon=True)
#m.drawmapboundary(fill_color='#99ffff')
#m.drawlsmask(land_color='coral',ocean_color='aqua')
# draw parallels
#m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# draw meridians
#m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
#plt.colorbar()
plt.show()
