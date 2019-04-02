import csv
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.ndimage.filters as filt
'''
c = 0
hhProfiles = {}
with open('../../../Documents/pecan-street/1min-texas/profiles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = [0.0]*48
        for t in range(1440):
            p[int(t/30)] += float(row[t])/30
        hhProfiles[c] = p
        c += 1
'''
c = 0
hhProfiles = {}
with open('../../../Documents/pecan-street/hourly-texas/profiles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = [0.0]*48
        for t in range(48):
            p[t] += float(row[t])
        p = filt.gaussian_filter1d(p,1)
        hhProfiles[c] = p
        c += 1

av = []
l = []
u = []

t_ = np.arange(0.25,24.25,0.5)

for t in range(48):
    x = []
    for h in hhProfiles:
        x.append(hhProfiles[h][t])
    x = sorted(x)

    av.append(sum(x)/len(x))
    l.append(x[int(0.1*len(x))])
    u.append(x[int(0.9*len(x))])
    
plt.figure(figsize=(6,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.xticks([2,6,10,14,18,22],['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.fill_between(t_,l,u,color='#CCFFCC')
plt.plot(t_,av,c='g')
plt.ylabel('Power (kW)')
plt.grid()
plt.xlim(0.25,23.75)
plt.tight_layout()
plt.savefig('../../../Dropbox/papers/V2G/img/texas_hh.eps',
            format='eps', dpi=1000)


c = 0
hhProfiles = {}
with open('../../../Documents/sharonb/7591/csv/profiles.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        day = int(row[-1])
        if day != 3:
            continue
        if random.random() > 0.1:
            continue
        p = []
        for t in range(48):
            p.append(float(row[2+t]))
        hhProfiles[c] = p
        c += 1

av = []
l = []
u = []

t_ = np.arange(0.25,24.25,0.5)

for t in range(48):
    x = []
    for h in hhProfiles:
        x.append(hhProfiles[h][t])
    x = sorted(x)

    av.append(sum(x)/len(x))
    l.append(x[int(0.1*len(x))])
    u.append(x[int(0.9*len(x))])
    
plt.figure(figsize=(6,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.xticks([2,6,10,14,18,22],['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.fill_between(t_,l,u,color='#CCCCFF')
plt.plot(t_,av,c='b')
plt.ylabel('Power (kW)')
plt.grid()
plt.xlim(0.25,23.75)
plt.tight_layout()
plt.savefig('../../../Dropbox/papers/V2G/img/uk_hh.eps',
            format='eps', dpi=1000)

plt.show()
