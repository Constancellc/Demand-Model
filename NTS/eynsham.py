# packages
import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import sklearn.cluster as clst
import sys
from cvxopt import matrix, spdiag, solvers, sparse

# I think I'm going to need to do two passes, one finding commuters and one
# filling in details

data = []
threshold = 50
eff = 0.9

with open('../../Documents/simulation_results/eynsham.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        shift = int(random.random()*30)
        a = 30*int(float(row[0])/30)+shift
        d = 30*int(float(row[1])/30)+shift
        
        e = float(row[2])
        if e > threshold:
            e = float(row[3])
        e = e/eff
        data.append([a,d,e])
        
cP = 3.5 # kW
dumb = []
for t in range(1440):
    dumb.append([])
    
for mc in range(200):
    chosen = []
    while len(chosen) < 100:
        ran = int(random.random()*len(data))
        if ran not in chosen:
            chosen.append(ran)
    
    p = [0.0]*1440
    for i in range(100):
        [a,d,e] = data[chosen[i]]
        
        chargeLen = int(e*60/cP)
        for t in range(chargeLen):
            if a+t < d:
                p[a+t] += cP

    for t in range(1440):
        dumb[t].append(p[t])
                
av = []
up = []
lo = []

for t in range(1440):
    av.append(sum(dumb[t])/len(dumb[t]))
    x = sorted(dumb[t])
    up.append(x[int(0.975*len(x))])
    lo.append(x[int(0.025*len(x))])

x_ticks = []
x = []
for h in range(4,24,4):
    if h < 10:
        x_ticks.append('0'+str(h)+':00')
    else:
        x_ticks.append(str(h)+':00')
    x.append(h*60)
plt.figure(1)
plt.ylabel('Power (kW)')
plt.plot(range(1440),av,c='b')
plt.xlim(0,1440)
plt.xticks(x,x_ticks)
plt.fill_between(range(1440),lo,up,color='b',alpha=0.2)
plt.ylim(0,1.1*max(up))
plt.grid()
plt.show()
