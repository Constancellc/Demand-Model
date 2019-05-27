import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.cbook
import csv
import datetime
import copy

stem = '../../Documents/elec_demand/'
day0 = datetime.datetime(2018,3,25)


stem2 = '../../Documents/simulation_results/NTS/national/'


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

for fg in tm:
    with open(stem2+'uncontrolled_'+fg+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            try:
                u[fg][int(int(row[0])/30)] += float(row[2])/30000000
            except:
                print(row[0])

# get the elexon profiles
e7 = {'sp':[],'su':[],'wt':[],'au':[]}
std = {'sp':[],'su':[],'wt':[],'au':[]}

with open(stem+'ProfileClass1.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        std['sp'].append(float(row[10]))
        std['au'].append(float(row[1]))
        std['wt'].append(float(row[13]))
        std['su'].append(float(row[7]))

with open(stem+'ProfileClass2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        e7['sp'].append(float(row[10]))
        e7['au'].append(float(row[1]))
        e7['wt'].append(float(row[13]))
        e7['su'].append(float(row[7]))


av = {'sp':[0.0]*48,'su':[0.0]*48,'wt':[0.0]*48,'au':[0.0]*48}

tm = ['sp','su','au','wt']
ttls = ['Spring','Summer','Autumn','Winter']
plt.figure(figsize=(6.5,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
for fg in range(4):
    lgst = 0
    profiles = {}
    with open(stem+tm[fg]+'.csv','rU') as csvfile:
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
                profiles[dayN] = [0.0]*48

            t = int((60*int(dt[10:12])+int(dt[13:15]))/30)

            profiles[dayN][t]+=float(row[2])/6000

    for da in profiles:
        if sum(profiles[da]) > lgst:
            lgst = sum(profiles[da])
            for t in range(48):
                av[tm[fg]][t] = profiles[da][t]#/len(profiles)
                if t > 1:
                    if abs(av[tm[fg]][t]-av[tm[fg]][t-1]) > 5:
                        av[tm[fg]][t] = av[tm[fg]][t-1]


    dom = []
    for t in range(48):
        dom.append(0.214*e7[tm[fg]][t]+0.786*std[tm[fg]][t])
        
    tot = sum(dom)
    for t in range(48):
        dom[t] = dom[t]*sum(av[tm[fg]])*0.388/tot

    ind = []
    for t in range(48):
        ind.append(av[tm[fg]][t]-dom[t])
    plt.figure(1)
    plt.subplot(2,2,fg+1)
    plt.plot(av[tm[fg]],label='total')
    plt.plot(dom,label='domestic')
    plt.plot(ind,label='industry')
    plt.title(ttls[fg])
    if fg == 0:
        plt.legend()
    plt.ylim(0,60)
    plt.xlim(0,47)
    plt.xticks(np.linspace(0,47,num=5),['0:00','06:00','12:00','18:00','23:59'])
    #plt.yticks([0,10000,20000,30000,40000],[0,10,20,30,40])
    plt.grid()

    pk_dom = max(dom)
    sm_dom = sum(dom)
    sm_new = sm_dom+135*2

    if pk_dom < sm_new/48:
        dom_new = [sm_new/48]*48

    else:
        dom_new = fill(dom,135*2)

    tot_new = []
    for t in range(48):
        tot_new.append(ind[t]+dom_new[t])

    if fg == 3:
        plt.tight_layout()

    plt.figure(2)
    plt.subplot(2,2,fg+1)
    plt.plot(av[tm[fg]],c='k',ls=':',label='No Charging')

    for t in range(48):
        u[tm[fg]][t] += av[tm[fg]][t]
    plt.plot(u[tm[fg]],label='Uncontrolled',c='b')
    plt.plot(tot_new,label='Controlled',c='r',ls='--')

    if fg == 1:
        plt.legend()
    if fg in [0,2]:
        plt.ylabel('Power (GW)')
    plt.ylim(20,60)
    plt.xlim(0,47)
    plt.title(ttls[fg])
    plt.xticks(np.linspace(3,43,num=5),['02:00','07:00','12:00','17:00','22:00'])
    #plt.xticks(np.linspace(0,47,num=5),['0:00','06:00','12:00','18:00','23:59'])
    #plt.yticks([0,10000,20000,30000,40000],[0,10,20,30,40])
    plt.grid()
plt.tight_layout()
plt.savefig('../../Dropbox/papers/Nature/img/national2.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
