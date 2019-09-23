import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

stem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA/'


def fill(p,new,stp=0.0001):
    p_ = copy.deepcopy(p)
    while new > 0:
        lwst = np.argmin(p_)
        p_[lwst] += stp
        new -= stp

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

frs = 30
lim = 820
fes = 14000
plt.figure(figsize=(7,8.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 12
plt.subplot(3,2,1)
plt.plot(goal,c='b',label='National EVs')
plt.legend()
plt.ylim(0,19)
plt.ylabel('Power (GW)')
plt.subplot(3,2,2)
sg = []
for i in range(48):
    sg.append(goal[i]*fes/sum(goal))
sg_old = copy.deepcopy(sg)
plt.fill_between(range(48),[0]*48,sg,color='#CCCCFF',label='Local EVs')
plt.legend()
plt.ylim(0,800)
plt.ylabel('Power (MW)')
for t in range(48):
    sg[t] += frs*res[t]
plt.subplot(3,2,3)
plt.plot(frs*np.array(res),c='k',ls=':',label='Existing Demand')
plt.fill_between(range(48),frs*np.array(res),sg,color='#CCCCFF')
plt.plot(range(48),[lim]*48,c='r',ls='--',label='Transformer Limit')
plt.ylim(0,1190)
plt.legend(loc=8)
plt.yticks([0,200,400,600,800,1000],['0.0','0.2','0.4','0.6','0.8','1.0'])
plt.ylabel('Power (GW)')

ov = 0
for t in range(48):
    if sg[t] > lim:
        ov += sg[t]-lim
        sg[t] = lim
sg = fill(sg,ov,stp=1)

plt.subplot(3,2,4)
plt.plot(frs*np.array(res),c='k',ls=':')
plt.fill_between(range(48),frs*np.array(res),sg,color='#CCCCFF')
plt.plot(range(48),[lim]*48,c='r',ls='--')
plt.ylim(0,1190)
plt.yticks([0,200,400,600,800,1000],['0.0','0.2','0.4','0.6','0.8','1.0'])
plt.ylabel('Power (GW)')

for t in range(48):
    sg[t] -= frs*res[t]

plt.subplot(3,2,5)
plt.fill_between(range(48),[0]*48,sg,color='#CCCCFF')
plt.plot(sg_old,c='gray',ls='--',label='Old version')
plt.legend()
plt.ylim(0,800)
plt.ylabel('Power (MW)')

plt.subplot(3,2,6)
plt.plot(goal,c='gray',ls='--')
plt.ylim(0,19)
plt.ylabel('Power (GW)')
for t in range(48):
    goal[t] -= sg[t]/1000
plt.plot(goal,c='b')

    
for i in range(1,7):
    plt.subplot(3,2,i)
    plt.xlim(0,47)
    plt.xticks([7.5,23.5,39.5],['04:00','12:00','20:00'])
    plt.grid(ls=':')
    plt.title(str(i),y=0.7)
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter7/img/diag_heuristic.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0.0)
plt.show()

hr = []
# now need to get my list of how constrained the individual networks are
with open('headroom.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        hr.append([float(row[1]),row[0],float(row[2])])
        hs_sum += float(row[2])*hs[row[0]]

plt.figure(figsize=(9,3.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 11
hr = sorted(hr)
pn = 1
ttls = {1:'Bracknell Forest',2:'Cheltenham',3:'North Devon'}
for i in range(len(hr)):
    LA = hr[i][1]
    nN = hr[i][2]
    if hr[i][0] < 0:
        thr = '0'
    else:
        thr = str(round(hr[i][0]))
    rsf = nN*hs[LA]/hs_sum
    p_h = []
    for t in range(48):
        p_h.append(res[t]*rsf)
    if i in [0,150,300]:
        plt.subplot(1,3,pn)
        plt.title(ttls[pn]+'\n('+thr+'%)')
        pn += 1
        plt.plot(p_h,c='k',ls=':',label='No Charging')
    ev = vs[LA]*total_v/vs_sum

    if hr[i][0] < 0:
        p_v = fill(p_h,ev)

    else:
        lim = max(p_h)*(1+hr[i][0]/100)
        p_v = fill2(p_h,ev,lim,goal)
    if i in [0,150,300]:
        plt.plot(p_v,c='r',label='Controlled Charging')
        plt.xlim(0,47)
        plt.ylim(0,0.08)
        plt.xticks([8,24,40],['04:00','12:00','20:00'])
        plt.grid()
        if i == 0:
            plt.yticks([0,0.02,0.04,0.06,0.08],[0,2,4,6,8])
            plt.ylabel('Power MW')
            plt.legend()
        else:
            plt.yticks([0,0.02,0.04,0.06,0.08],['']*5)
        if i == 300:
            plt.tight_layout()

    for t in range(48):
        goal[t] -= p_v[t]
        goal[t] += p_h[t]
        res_evs[t] += p_v[t]-p_h[t]

y1 = []
y2 = []
for t in range(48):
    y1.append(ind[t]+res[t])
    y2.append(ind[t]+res[t]+res_evs[t])
plt.savefig('../../Dropbox/thesis/chapter7/img/eg_heuristic.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0.0)
plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 14
plt.fill_between(range(48),[0]*48,ind,color='#CCCCFF',label='Industry')
plt.fill_between(range(48),y1,ind,color='#CCFFCC',label='Domestic')
plt.fill_between(range(48),y1,y2,color='#FFCCCC',label='Charging')
plt.plot(range(48),y2,c='k')

plt.legend(ncol=3)
plt.xlim(0,47)
plt.ylim(0,60)
plt.xticks([8,16,24,32,40],['04:00','08:00','12:00','16:00','20:00'])
plt.grid()
plt.ylabel('Power (GW)')
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter7/img/heuristic.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0.0)
plt.show()        

    # otherwise we want to maybe scale the resultant profile until the peak
    # demand limit is reached
    
    
    
