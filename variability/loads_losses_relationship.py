# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)
t_ = range(0,1440)
x_ = np.linspace(2*60,22*60,num=6)
x_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']

losses_csv = ['0%ev_losses.csv','100%ev_losses.csv','100%ev_opt_losses.csv']
loads_csv = ['0%ev_total_load.csv','100%ev_total_load.csv',
         '100%ev_opt_total_loads.csv']
lbls=['no evs','uncontrolled','optimal']

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
for i in [1,2,0]:    
    x = []
    y = []

    losses = []
    t = 0
    with open(losses_csv[i],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            if t == 0:
                for j in range(1,2):#len(row)):
                    losses.append([0.0]*1440)

            for j in range(1,2):#len(row)):
                losses[j-1][t] += float(row[j])
            t += 1

    loads = []
    n = 0
    with open(loads_csv[i],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            n += 1
            if n != 2:
                continue
            p = []
            for j in range(0,len(row)):
                p.append(float(row[j]))
            loads.append(p)

    for s in range(0,len(loads)):
        for t in range(0,1440):
            x.append(loads[s][t])
            y.append(losses[s][t])
        
    plt.scatter(x,y,marker='+',s=5,color='b',label=lbls[i])
    
plt.grid()
#plt.legend()
plt.xlabel('Load (kW)')
plt.ylabel('Losses (kW)')
plt.show()


