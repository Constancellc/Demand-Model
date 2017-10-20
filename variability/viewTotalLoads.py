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

high = ['0%ev_total_load.csv','100%ev_total_load.csv','100%ev_opt_total_loads.csv']
titles = ['No EVs','Dumb Charging','Smart Charging']

for sim in range(0,3):
    l = [0.0]*1440
    h = [0.0]*1440
    m = [0.0]*1440

    allP = {}
    allE = []
    for i in range(0,1440):
        allP[i] = []
        
    with open(high[sim],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            x = []
            
            for i in range(0,1440):
                x.append(float(row[i]))
                allP[i].append(float(row[i]))

            allE.append([sum(x)]+x)

    for i in range(0,1440):
        x = sorted(allP[i])
        l[i] = x[0]
        h[i] = x[-1]
        m[i] = x[int(len(x)/2)]

    allE = sorted(allE)
    m2 = allE[int(len(allE)/2)][1:]

    plt.subplot(1,3,sim+1)

    plt.plot(t_,m2,'b')
    plt.fill_between(t_,h,l,color='b',alpha=0.2)
    plt.xlim(0,1440)
    plt.ylim(0,60)
    plt.xticks(x_,x_ticks)
    plt.title(titles[sim])
    plt.grid()
    #plt.ylim(236,256)
    plt.xlabel('Time')
    if sim == 0:
        plt.ylabel('Total Load (kW)')

plt.show()
            
