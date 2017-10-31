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

losses = ['0%ev_losses.csv','100%ev_losses.csv',
          '100%TOUev_losses.csv','100%ev_opt_losses.csv']
loads = ['0%ev_total_load.csv','100%ev_total_load.csv',
         '100%TOUev_total_load.csv','100%ev_opt_total_loads.csv']

pfs = ['0%ev_pf.csv','100%ev_pf.csv','%ev_pf.csv']
clrs = ['b','r','g','k']

lbl = ['without evs','dumb','tou','smart']

totals = {}

for sim in range(0,4):
    lds = []

    with open(loads[sim],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            x = []
            for i in range(0,len(row)):
                x.append(float(row[i]))
            lds.append(x)
            
    totals[sim] = []
    h = [0]*1440
    m = [0]*1440
    l = [1000]*1440

    t = 0
    with open(losses[sim],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            if t == 0:
                total = [0.0]*len(row)
                print(len(total))
            x = []
            for i in range(0,len(row)):
                total[i] += float(row[i])*100/(sum(lds[i]))
                #total[i] += float(row[i])/60 # this is for raw energy losses
                x.append(float(row[i]))

            h[t] = max(x)
            l[t] = min(x)
            m[t] = sorted(x)[49]
            t += 1
            
    '''
    for i in range(0,len(total)):
        total[i] = total[i]*100/sum(lds[i])
    '''
    totals[sim].append(total)

    #plt.subplot(2,1,sim+1)
    plt.plot(t_,m,clrs[sim],label=lbl[sim])
    #plt.fill_between(t_,h,l,color=clrs[sim],alpha=0.2)
    plt.xlim(0,1440)
    plt.xticks(x_,x_ticks)
    #plt.title(titles[sim])
    if sim == 0:
        plt.grid()
    plt.xlabel('Time')
    plt.legend(ncol=3,loc=[0.1,1.05])
    plt.ylabel('Power Lost (kW)')

x2_ticks = ['Without\nEVs','Uncontrolled\nCharging','TOU\nCharging',
            'Load Flattening\nCharging']
plt.figure(2)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
plt.boxplot([totals[0],totals[1],totals[2],totals[3]],0,'',whis=[0.05, 99.5])
plt.xticks([1,2,3,4],x2_ticks)
#plt.ylim(0,20)
plt.grid()
plt.ylabel('Energy Lost (%)')
'''
pf = [[],[]]
for i in range(0,2):
    with open(pfs[i],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            pf[i].append(float(row[0]))
plt.figure(3)
plt.boxplot(pf,0,'')
plt.grid()
'''
plt.show()
            
