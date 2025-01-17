# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
#plt.rcParams['font.size'] = 8
t_ = range(0,1440)
x_ = np.linspace(4*60,20*60,num=3)
x_ticks = ['04:00','12:00','20:00']

ld = ['0%ev_total_load.csv','100%ev_total_load.csv','100%PsOptev_total_load.csv',
      '100%TOUev_total_load.csv','100%ev_opt_total_loads.csv']
titles = ['No EVs','Uncontrolled\nCharging','Psuedo Optimal\nCharging',
          'TOU Charging','Load Flattening\nCharging']

for sim in range(0,5):
    l = [0.0]*1440
    h = [0.0]*1440
    m = [0.0]*1440

    allP = {}
    allE = []
    for i in range(0,1440):
        allP[i] = []
        
    with open(ld[sim],'rU') as csvfile:
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
        m[i] = sum(x)/len(x)#x[int(len(x)/2)]

    allE = sorted(allE)
    m2 = allE[int(len(allE)/2)][1:]

    plt.subplot(2,5,sim+1)

    plt.plot(t_,m,'g',label='Total Feeder Load')
    #plt.plot(t_,m2,'g',label='Total Feeder Load')
    print(sum(m2))
    plt.fill_between(t_,h,l,color='g',alpha=0.2)
    plt.xlim(0,1440)
    plt.ylim(0,180)
    plt.xticks(x_,x_ticks)
    plt.title(titles[sim])
    plt.grid()
    #plt.ylim(236,256)
    #plt.xlabel('Time')
    if sim == 0:
        plt.ylabel('Total Load (kW)')
        plt.legend(loc=[1.65,1.3])
    else:
        plt.yticks(np.arange(50,200,50),['']*3)

high = ['highest_no_ev.csv','highest_with_evs.csv','PsOpthighest_with_evs.csv',
        'TOUhighest_with_evs.csv','highest_with_evs_opt.csv']
low = ['lowest_no_ev.csv','lowest_with_evs.csv','PsOptlowest_with_evs.csv',
       'TOUlowest_with_evs.csv','lowest_with_evs_opt.csv']

for sim in range(0,5):
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
            for i in range(0,len(row)):
                x.append(float(row[i])/240)

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
            for i in range(0,len(row)):
                x.append(float(row[i])/240)

            lH[t] = max(x)
            lL[t] = min(x)
            lM[t] = sorted(x)[49]
            t += 1

    plt.subplot(2,5,sim+6)
    plt.plot(t_,uM,'r',label='Highest Voltage in Network')
    plt.fill_between(t_,uH,uL,color='r',alpha=0.2)
    plt.plot(t_,lM,'b',label='Lowest Voltage in Network')
    plt.fill_between(t_,lH,lL,color='b',alpha=0.2)
    plt.xlim(0,1440)
    plt.xticks(x_,x_ticks)
    #plt.title(titles[sim])
    plt.grid()
    plt.ylim(0.93,1.08)
    plt.xlabel('Time')
    if sim == 0:
        plt.ylabel('Voltage (p.u.)')
        #plt.legend(loc=[0.7,1.11],ncol=2)
        plt.legend(loc=[0.7,1.11],ncol=2)
    else:
        plt.yticks([0.95,1,1.05],['']*3)
plt.tight_layout()    
plt.savefig('../../papers/PES-GM/voltage-time',format='pdf')
plt.show()
            
