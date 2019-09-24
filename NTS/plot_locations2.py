# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np


nV = 0
trips = '../../Documents/UKDA-5340-tab/constance-trips.csv'
jLogs = {}
with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        wd = int(row[6])
        if wd > 5:
            continue

        try:
            s = int(row[9])+1440*(wd-1)
            of = int(30*random.random())
            s = 30*int(s/30)+of
            e = int(row[10])+1440*(wd-1)
            e = 30*int(e/30)+of
            #pf = row[12]
            pt = row[13]
        except:
            continue
        
        v = row[2]
        if v == '':
            continue
        
        if v not in jLogs:
            jLogs[v] = []
            nV += 1

        jLogs[v].append([s,e,pt])

print(nV)
nV = nV/100
_h = [0]*7200
_w = [0]*7200
_t = [0]*7200
_s = [0]*7200

for v in jLogs:
    d = sorted(jLogs[v])

    for t in range(0,d[0][0]):
        _h[t] += 1/nV

    for i in range(len(d)-1):
        s = d[i][0]
        e = d[i][1]
        if e > 7199:
            e = 7199
            
        p = d[i][2]

        for t in range(s,e):
            _t[t] += 1/nV
        if p == '23':
            for t in range(e,d[i+1][0]):
                _h[t] += 1/nV
        if p in ['4','5']:
            for t in range(e,d[i+1][0]):
                _s[t] += 1/nV
        if p == '1':
            for t in range(e,d[i+1][0]):
                _w[t] += 1/nV

    p = d[-1][2]
    if p == '23':
        for t in range(e,7200):
            _h[t] += 1/nV
    if p in ['4','5']:
        for t in range(e,7200):
            _s[t] += 1/nV
    if p == '1':
        for t in range(e,7200):
            _w[t] += 1/nV

plt.figure(figsize=(6,3.3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 11
plt.plot(_h[2880:4320],label='Home')
plt.plot(_w[2880:4320],label='Work')
plt.plot(_s[2880:4320],label='Shops')
plt.plot(_t[2880:4320],label='Transit',ls='--')
plt.xlim(0,1439)
plt.xticks([4*60,8*60,12*60,16*60,20*60],
           ['04:00','08:00','12:00','16:00','20:00'])
plt.ylim(0,100)
plt.legend()
plt.ylabel('Vehicles (%)')
plt.tight_layout()
plt.grid(ls=':')
plt.savefig('../../Dropbox/thesis/chapter1/loc.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0.0)
plt.show()
        
