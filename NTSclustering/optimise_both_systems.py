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

def cap(p,lim):
    p_ = copy.deepcopy(p)
    extra = 0
    for t in range(48):
        if p_[t] > lim:
            extra += p_[t]-lim
            p_[t] = lim
    p_ = fill(p_,extra)
    return p_

def fill2(p,new,lim,goal):
    p_ = copy.deepcopy(goal) # copy goal shape
    sf = new/sum(p_)
    for t in range(48):
        p_[t] = p_[t]*sf+p[t]

    if max(p_) > lim:
        p_ = cap(p_,lim)

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


res = data[0]
ind = data[1]
total = []
for t in range(48):
    total.append(data[0][t]+data[1][t])

total_r = sum(data[0])
total_v = sum(data[2])

ideal = (sum(ind)+total_r+total_v)/48
if ideal < max(total):
    ideal = max(total)

res_evs = [0]*48
goal = []
for t in range(48):
    goal.append(ideal-total[t])

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

    if hr[i][0] < 0:
        p_v = fill(p_h,ev)

    else:
        lim = max(p_h)*(1+hr[i][0]/100)
        p_v = fill2(p_h,ev,lim,goal)

    for t in range(48):
        goal[t] -= p_v[t]
        goal[t] += p_h[t]
        res_evs[t] += p_v[t]-p_h[t]

y1 = []
y2 = []
for t in range(48):
    y1.append(ind[t]+res[t])
    y2.append(ind[t]+res[t]+res_evs[t])
    
plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'

plt.fill_between(range(48),[0]*48,ind,color='b',alpha=0.5,label='Industry')
plt.fill_between(range(48),y1,ind,color='g',alpha=0.5,label='Domestic')
plt.fill_between(range(48),y1,y2,color='r',alpha=0.5,label='Charging')

plt.legend(ncol=3)
plt.xlim(0,47)
plt.ylim(0,60)
plt.xticks([8,16,24,32,40],['04:00','08:00','12:00','16:00','20:00'])
plt.grid()
plt.ylabel('Power (GW)')

# would also be good to show the headroom while we're at it

plt.show()        
    
    
    
