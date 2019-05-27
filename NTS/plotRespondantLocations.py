from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv
import copy

file = '../../Documents/UKDA-7553-tab/constance/hh-loc.csv'
file2 = '../../Documents/census/dwellingType-MSOA.csv'

m2l = {}
file3 = '../../Documents/census/Output_Area_to_Lower_Layer_Super_Output_Area_to_Middle_Layer_Super_Output_Area_to_Local_Authority_District_December_2017_Lookup_in_Great_Britain__Classification_Version_2.csv'
with open(file3,'rU',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        msoa = row[7]
        la = row[9]
        m2l[msoa] = la

LAs = {}
with open(file,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        la = row[2]
        if la not in LAs:
            LAs[la] = 1
        else:
            LAs[la] += 1

LAs2 = {}
with open(file2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
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

# get locations
locs = {}
with open('LA-lat-lon.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[1]] = [float(row[3]),float(row[2])]


pList = []
z = []

for la in LAs2:
    z.append(100*LAs[la]/LAs2[la])
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

x = np.arange(-5.5,1.9,0.02)
y = np.arange(49.8,55.4,0.02)

Z = np.zeros((len(x),len(y)))
X = np.zeros((len(x),len(y)))
Y = np.zeros((len(x),len(y)))

fig=plt.figure(figsize=(4.5,4) )
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 10
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-5.55,llcrnrlat=49.9,urcrnrlon=1.9,urcrnrlat=55.2,\
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
            '''if xpt < 200000 and ypt < 970000 and ypt > 300000:
                continue
            '''
            if xpt < 150000 and ypt < 800000 and ypt > 650000:
                continue
            if xpt > 685000 and ypt < 175000:
                continue
            if xpt > 766000 and ypt < 104000:
                continue
            Z[i,j] = z[best]
        else:
            continue

m.pcolor(X,Y,Z,cmap='Blues')
plt.colorbar()
plt.savefig('../../Dropbox/thesis/chapter3/img/respondants_loc.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0.1)

plt.show()
        
            
