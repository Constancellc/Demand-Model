import matplotlib.pyplot as plt
import numpy as np
import csv
import utm


stem = '../../../Documents/census/'
# get locations
locs = {}
with open(stem+'centroids-MSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        #x.append(float(row[0]))
        #y.append(float(row[1]))
        locs[row[3]] = [float(row[0]),float(row[1])]

x = {}
y = {}

c_ = {0:'#9400D3',0.5:'#4B0082',0.75:'#0000FF',1:'#00FF00',1.25:'#FFFF00',
      1.5:'#FF7F00',1.75:'#FF0000'}

def get_nearest(p,dic):
    dmin = 10000
    c = None
    for d in dic:
        if abs(d-p) < dmin:
            dmin = abs(d-p)
            best = dic[d]
    return best

def get_nearest2d(p,dic):
    dmin = 50000
    c = None
    for p2 in dic:
        d = np.sqrt(np.power(p[0]-dic[p2][0],2)+np.power(p[1]-dic[p2][1],2))
        if d < dmin:
            dmin = d
            c = p2
    return c
            
        
for a in np.arange(0,3,0.1):
    x[round(a,1)] = []
    y[round(a,1)] = []

xx = np.arange(150000,650000,10000)
yy = np.arange(0,600000,10000)

z = np.zeros((len(x),len(y)))

avs_ = {}
with open(stem+'cars-MSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 7:
            continue
        try:
            float(row[1])
        except:
            continue
        msoa = row[0][:9]
        av = 1*float(row[3])+2*float(row[4])+3*float(row[5])+4*float(row[6])
        av = av/float(row[1])
        avs_[msoa] = av
        av = round(av,1)
        if av > 2.9:
            av = 2.9
        x[av].append(locs[msoa][0])
        y[av].append(locs[msoa][1])

'''
for i in range(len(xx)):
    x = xx[i]
    for j in range(len(yy)):
        y = yy[j]
        c = get_nearest2d([x,y],locs)
        if c != None:
            try:
                z[i][j] = avs_[c]
            except:
                continue

plt.figure()
plt.imshow(z)
plt.show()
'''
a_ = 0.1
plt.figure()
for a in np.arange(2.9,0,-0.1):#x:
    plt.scatter(x[round(a,1)],y[round(a,1)],c=get_nearest(a,c_),s=3)
plt.show()



