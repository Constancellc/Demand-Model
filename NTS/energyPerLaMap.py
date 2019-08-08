import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import csv
import copy
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

greens = cm.get_cmap('Greens', 1000)
new = greens(np.linspace(0, 1, 1000))
new[:1,:] =  np.array([1,1,1,1])
green2 = ListedColormap(new)

file = '../../Documents/UKDA-7553-tab/constance/hh-loc.csv'
file2 = '../../Documents/census/dwellingType-MSOA.csv'
file4 = '../../Documents/census/scotland_dwellings.csv'
trips = '../../Documents/UKDA-5340-tab/tab/tripeul2016.tab'

m2l = {}
file3 = '../../Documents/census/Output_Area_to_Lower_Layer_Super_Output_Area_to_Middle_Layer_Super_Output_Area_to_Local_Authority_District_December_2017_Lookup_in_Great_Britain__Classification_Version_2.csv'
with open(file3,'rU',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        msoa = row[7]
        la = row[9]
        m2l[msoa] = la

LAs = {}
hh2LA = {}
with open(file,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        la = row[2]
        hh2LA[row[0]] = la
        if la not in LAs:
            LAs[la] = 1
        else:
            LAs[la] += 1

LAs2 = {}
with open(file2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for i in range(10):
        next(reader)
    for row in reader:
        if len(row) < 2:
            continue
        m = row[0][:9]
        try:
            la = m2l[m]
        except:
            continue
        if la not in LAs:
            continue
        if la not in LAs2:
            LAs2[la] = 0
        LAs2[la] += float(row[1])
        
with open(file4,'rU',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        LAs2[row[1]] = int(row[2])

sf = {}
distance = {}
toskip = []
for la in LAs2:
    distance[la] = 0
    try:
        sf[la] = LAs2[la]/LAs[la]
    except:
        toskip.append(la)

# get distances
with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    for row in reader:
        if row[20] != '5': # if trip by car
            continue
        la = hh2LA[row[4]]
        d = float(row[26])
        if d > 100:
            d = 100
        try:
            distance[la] += d
        except:
            continue
        
# now make map
 
# get locations
locs = {}
with open('LA-lat-lon.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[1]] = [float(row[3]),float(row[2])]


pList = []
z = []
z2 = []

_2030 = {}
with open('2030.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        _2030[row[0]] = float(row[1])/100

for la in LAs2:
    if la in toskip:
        continue
    z.append(0.3e-6*distance[la]*sf[la]/7)
    try:
        z2.append(z[-1]*_2030[la])
    except:
        z2.append(z[-1]*0.48)
    pList.append(locs[la])

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

x = np.arange(-7.1,1.9,0.02)
y = np.arange(49.8,59,0.02)

Z = np.zeros((len(x),len(y)))
Z2 = np.zeros((len(x),len(y)))
X = np.zeros((len(x),len(y)))
Y = np.zeros((len(x),len(y)))

fig=plt.figure()#figsize=(4.5,4) )
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 10
plt.subplot(1,2,1)
plt.title('100%',fontweight='bold')
ax = plt.gca()
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=1.9,urcrnrlat=58.9,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)

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
            if xpt < 150000 and ypt < 800000 and ypt > 650000:
                continue
            if xpt > 685000 and ypt < 175000:
                continue
            if xpt > 766000 and ypt < 104000:
                continue
            Z[i,j] = z[best]
            Z2[i,j] = z2[best]
        else:
            continue

im = m.pcolor(X,Y,Z,cmap=green2)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)

plt.subplot(1,2,2)
plt.title('2030',fontweight='bold')
ax = plt.gca()
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=1.9,urcrnrlat=58.9,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)

m.drawcoastlines()
im = m.pcolor(X,Y,Z2,cmap=green2)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/Nature/img/energy.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()
        
            
       
            
