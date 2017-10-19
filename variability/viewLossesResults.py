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

losses = ['0%ev_losses.csv','100%ev_losses.csv','100%ev_opt_losses.csv']
clrs = ['b','r']

lbl = ['without evs','smart','dumb']

totals = {}

for sim in range(0,3):
    totals[sim] = []
    h = [0]*1440
    m = [0]*1440
    l = [1000]*1440

    total = [0.0]*100

    t = 0
    with open(losses[sim],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            x = []
            for i in range(0,100):
                total[i] += float(row[i])/60
                x.append(float(row[i]))

            h[t] = max(x)
            l[t] = min(x)
            m[t] = sorted(x)[49]
            t += 1

    totals[sim].append(total)

    #plt.subplot(2,1,sim+1)
    plt.plot(t_,m,clrs[sim],label=lbl[sim])
    plt.fill_between(t_,h,l,color=clrs[sim],alpha=0.2)
    plt.xlim(0,1440)
    plt.xticks(x_,x_ticks)
    #plt.title(titles[sim])
    if sim == 0:
        plt.grid()
    plt.xlabel('Time')
    plt.legend(ncol=3,loc=[0.1,1.05])
    plt.ylabel('Power Lost (kW)')

x2_ticks = ['no\nevs','dumb\ncharging','smart\ncharging']
plt.figure(2)
plt.boxplot([totals[0],totals[1],totals[2]],0,'')
plt.xticks([1,2,3],x2_ticks)
plt.grid()
plt.ylabel('Daily Losses (kWh)')
plt.show()
            
