import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/pecan-street/1min-april2018/'
          
hh = {}
t0 = datetime.datetime(2018,4,1)

for f in range(1,2):    
    with open(stem+str(f)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            date = datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                                     int(row[0][8:10]),int(row[0][11:13]),
                                     int(row[0][14:16]),int(row[0][17:19]))
            t = int((date-t0).seconds/60+1440*(date-t0).days)
            
            hhid = row[1]
            
            if hhid not in hh:
                hh[hhid] = [0.0]*(1440*7)
            solar = float(row[2])
            if solar < 0:
                solar = 0
            try:
                hh[hhid][t] += solar
            except:
                continue
toRemove = []
for hhid in hh:
    s = sum(hh[hhid])
    
    if s == 0:
        toRemove.append(hhid)
        continue
    
    for t in range(1440*7):
        hh[hhid][t] = hh[hhid][t]/s
    if max(hh[hhid]) > 0.01:
        toRemove.append(hhid)

for hhid in toRemove:
    del hh[hhid]
    
hh_ = []
for hhid in hh:
    hh_.append(hhid)
sorted(hh_)
    
N = len(hh_)

corr = []
for i in range(N):
    corr.append([0.0]*N)

for i in range(N):
    for j in range(N):
        if i == j:
            corr[i][j] = 1.0
            continue
        if i > j:
            continue
        ex = 0.0
        ey = 0.0
        exy = 0.0
        ex2 = 0.0
        ey2 = 0.0

        for t in range(1440*7):
            ex += hh[hh_[i]][t]/(1440*7)
            ey += hh[hh_[j]][t]/(1440*7)
            ex2 += (hh[hh_[i]][t]*hh[hh_[i]][t])/(1440*7)
            ey2 += (hh[hh_[j]][t]*hh[hh_[j]][t])/(1440*7)
            exy += (hh[hh_[i]][t]*hh[hh_[j]][t])/(1440*7)

        corr[i][j] = (exy-ex*ey)/np.sqrt((ex2-ex*ex)*(ey2-ey*ey))
        corr[j][i] = (exy-ex*ey)/np.sqrt((ex2-ex*ex)*(ey2-ey*ey))
    
plt.figure(1)
plt.imshow(corr)
plt.show()
