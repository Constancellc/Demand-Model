import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

stem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA/'


def fill(p,new):
    p_ = copy.deepcopy(p)
    while new > 0:
        lwst = np.argmin(p_)
        p_[lwst] += 0.0001
        new -= 0.0001

    return p_

hs = {}
hs_sum = 0
vs = {}
vs_sum = 0
with open(stem+'lvScaling.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        hs[row[0]] = float(row[1])
        vs[row[0]] = float(row[2])
        #hs_sum += float(row[1])
        vs_sum += float(row[2])

data = []
with open('winter.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        p = []
        for i in range(1,49):
            p.append(float(row[i]))
        data.append(p)

plt.figure()
for i in range(3):
    plt.plot(data[i])
plt.show()

res = data[0]
ind = data[i]

total_r = sum(data[0])
total_v = sum(data[2])

hr = []
# now need to get my list of how constrained the individual networks are
with open('headroom.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        hr.append([float(row[1]),row[0],float(row[2])])
        hs_sum += float(row[2])*hs[row[0]]

hr = sorted(hr)
for i in range(len(hr)):
    LA = hr[i][1]
    nN = hr[i][2]
    rsf = nN*hs[LA]/hs_sum
    p_h = []
    for t in range(48):
        p_h.append(res[t]*rsf)
    ev = vs[LA]*total_v/vs_sum

    plt.plot(p_h)
    p_v = fill(p_h,ev)
    plt.plot(p_v)
    plt.show()

    
    
    
