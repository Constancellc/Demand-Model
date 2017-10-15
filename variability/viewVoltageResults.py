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

high = ['highest_no_ev.csv','highest_with_evs.csv']
low = ['lowest_no_ev.csv','lowest_with_evs.csv']

titles = ['No EVs','1 EV per Household']
for sim in range(0,2):
    uH = [0]*1440
    uM = [0]*1440
    uL = [1000]*1440

    lH = [0]*1440
    lM = [0]*1440
    lL = [1000]*1440

    t = 0
    with open(high[sim],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            x = []
            for i in range(0,100):
                x.append(float(row[i]))

            uH[t] = max(x)
            uL[t] = min(x)
            uM[t] = sorted(x)[49]
            t += 1


    t = 0               
    with open(low[sim],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            x = []
            for i in range(0,100):
                x.append(float(row[i]))

            lH[t] = max(x)
            lL[t] = min(x)
            lM[t] = sorted(x)[49]
            t += 1

    plt.subplot(1,2,sim+1)
    plt.plot(t_,uM,'r',label='Highest in Network')
    plt.fill_between(t_,uH,uL,color='r',alpha=0.2)
    plt.plot(t_,lM,'b',label='Lowest in Network')
    plt.fill_between(t_,lH,lL,color='b',alpha=0.2)
    plt.xlim(0,1440)
    plt.xticks(x_,x_ticks)
    plt.title(titles[sim])
    plt.grid()
    plt.ylim(236,256)
    plt.xlabel('Time')
    if sim == 0:
        plt.ylabel('Voltage (V)')
        plt.legend(loc=[0.5,1.1],ncol=2)
    

plt.show()
            
