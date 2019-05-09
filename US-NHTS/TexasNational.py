# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np


stem = '../../Documents/simulation_results/NTS/national/'

profiles = {}
for m in range(12):
    profiles[str(m+1)] = {}
with open('../../Documents/elec_demand/Native_Load_2018.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        m = str(int(row[0][:2]))
        d = int(row[0][3:5])
        h = int(row[0][11:13])-1

        if d not in profiles[m]:
            profiles[m][d] = [0]*24

        profiles[m][d][h] = float(row[-1].replace(',',''))/1000        

mts = {'1':'wt','2':'wt','3':'sp','4':'sp','5':'sp','6':'su','7':'su','8':'su',
       '9':'au','10':'au','11':'au','12':'wt'}
wrst = {'wt':[0]*24,'sp':[0]*24,'su':[0]*24,'au':[0]*24}

for m in profiles:
    for d in profiles[m]:
        if sum(profiles[m][d]) > sum(wrst[mts[m]]):
            wrst[mts[m]] = profiles[m][d]
            
plt.figure(figsize=(6.5,4.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
ss = ['wt','sp','su','au']

for f in range(4):
    plt.subplot(2,2,f+1)
    plt.plot(wrst[ss[f]],c='k',ls=':',label='Current')
    plt.ylim(0,80)
    plt.xlim(0,23)
    '''
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
    plt.xlim(0,287)'''
plt.show()
