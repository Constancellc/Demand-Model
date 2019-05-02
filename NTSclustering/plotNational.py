import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
import datetime

day0 = datetime.datetime(2018,1,1)
stem = '../../Documents/simulation_results/NTS/national/'

stem2 = '../../Documents/elec_demand/'

def fill(p,new):
    p_ = copy.deepcopy(p)
    while new > 0:
        lwst = np.argmin(p_)
        p_[lwst] += 0.01
        new -= 0.01

    return p_

tm = ['sp','su','au','wt']
ttls = ['Spring','Summer','Autumn','Winter']
u = {'sp':[0.0]*288,'su':[0.0]*288,'wt':[0.0]*288,'au':[0.0]*288}
d = {'sp':[0.0]*288,'su':[0.0]*288,'wt':[0.0]*288,'au':[0.0]*288}

for fg in tm:
    with open(stem+'uncontrolled_'+fg+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            try:
                d[fg][int(int(row[0])/5)] += float(row[1])/5000000
                u[fg][int(int(row[0])/5)] += float(row[2])/5000000
            except:
                print(row[0])

av = {'sp':[0.0]*288,'su':[0.0]*288,'wt':[0.0]*288,'au':[0.0]*288}

ttls = ['Spring','Summer','Autumn','Winter']

for fg in range(4):
    profiles = {}
    lgst = 0
    with open(stem2+tm[fg]+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            dt = row[1].replace(' ','')
            day = datetime.datetime(int(dt[:4]),int(dt[5:7]),int(dt[8:10]))
            dayN = (day-day0).days
            if dayN < 1:
                continue
            elif day.isoweekday() > 5:
                continue
            elif dayN not in profiles:
                profiles[dayN] = [0.0]*288

            t = int((60*int(dt[10:12])+int(dt[13:15]))/5)

            profiles[dayN][t]+=float(row[2])/1000

    for da in profiles:
        if sum(profiles[da]) > lgst:
            lgst = sum(profiles[da])
            for t in range(288):
                av[tm[fg]][t] = profiles[da][t]#/len(profiles)
                if t > 1:
                    if abs(av[tm[fg]][t]-av[tm[fg]][t-1]) > 2:
                        av[tm[fg]][t] = av[tm[fg]][t-1]

plt.figure(figsize=(6.5,4.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
for f in range(4):
    plt.subplot(2,2,f+1)
    plt.plot(av[tm[f]],c='k',ls=':',label='Current')
    plt.plot(fill(av[tm[f]],sum(u[tm[f]])),label='Controlled',c='r',ls='--')

    for t in range(288):
        u[tm[f]][t] += av[tm[f]][t]
        d[tm[f]][t] += av[tm[f]][t]
    
    plt.title(ttls[f])
    #plt.plot(d[tm[f]],label='Uncontrolled (a)',c='g',ls='--')
    plt.plot(u[tm[f]],label='Uncontrolled',c='b')

    if f in [0,2]:
        plt.ylabel('Power (GW)')
    elif f == 1:
        plt.legend(ncol=1)
    plt.xticks(np.linspace(23,263,num=5),['02:00','07:00','12:00','17:00','22:00'])
    #plt.xticks(np.linspace(47,239,num=5),['04:00','08:00','12:00','16:00','20:00'])
    plt.ylim(20,60)
    plt.grid()
    plt.xlim(0,287)

plt.tight_layout()

#plt.savefig('../../Dropbox/thesis/chapter5/img/national.eps', format='eps',
#            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.savefig('../../Dropbox/papers/Nature/img/national.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()

dumb = []
l = []
m = []
u = []
base_ = []
for t in range(1440):
    p1 = int(t/5)
    p2 = p1 + 1
    if p2 == len(base):
        p2 -= 1
    f = float(t%5)/5
    base_.append((1-f)*base[p1]/1000+f*base[p2]/1000)
base = base_
with open(stem+'uncontrolled_smr.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        dumb.append(float(row[1])/1000000+base[int(row[0])])
        m.append(float(row[2])/1000000+base[int(row[0])])
        l.append(float(row[3])/1000000+base[int(row[0])])
        u.append(float(row[4])/1000000+base[int(row[0])])

print(sum(dumb))
print(sum(base))
plt.figure()
plt.plot(m)
plt.plot(dumb)
plt.plot(base,c='k',ls=':')
#plt.fill_between(range(1440),l,u,alpha=0.2)
plt.xticks()
plt.ylim(0,70)
plt.xlim(0,1439)
plt.ylabel('Power (GW)')
plt.xticks([2*60,6*60,10*60,14*60,18*60,22*60],
           ['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.grid()
plt.tight_layout()
plt.show()

