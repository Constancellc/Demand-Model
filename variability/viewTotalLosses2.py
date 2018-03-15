# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/simulation_results/LV/total_losses/'

# first get data
results = {1:[],2:[],3:[],4:[],5:[]} # W
results2 = {1:[],2:[],3:[],4:[],5:[]} # %

for mc in range(100):
    with open(stem+str(mc+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        row = next(reader)
        noEV = float(row[1])*1000
        withEV = float(row[3])*1000
        next(reader)
        new = {1:[],2:[],3:[],4:[],5:[]}
        for row in reader:
            for i in range(1,len(row)):
                new[i].append(float(row[i]))
        for i in range(1,6):
            results[i].append(new[i])
            if i == 1:
                results2[i].append(100*sum(new[i])/noEV)
            else:
                results2[i].append(100*sum(new[i])/withEV)

x2_ticks = ['Without\nEVs','Uncontrolled\n(3.5kW)','Uncontrolled\n(7kW)',
            'Load\nFlattening','Loss\nMinimizing']
plt.figure(figsize=(5,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
plt.boxplot([results2[1],results2[2],results2[3],results2[4],
             results2[5]],0,'',whis=[0.05, 99.5])
plt.xticks([1,2,3,4,5],x2_ticks)
#plt.plot([0.5,4.5],[av[1],av[1]],'k',ls=':',alpha=0.5)
plt.grid()
plt.ylabel('Losses (%)')

# this gives the variation throughout the day in losses (W)
'''
m = {1:[],2:[],3:[],4:[],5:[]}
u = {1:[],2:[],3:[],4:[],5:[]}
l = {1:[],2:[],3:[],4:[],5:[]}

for typ in results:
    for t in range(1440):
        x = []
        for mc in range(len(results[1])):
            x.append(results[typ][mc][t])
        x = sorted(x)
        l[typ].append(x[0])
        u[typ].append(x[-1])
        m[typ].append(x[int(len(x)/2)])

# now plot results
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
t_ = range(0,1440)
x_ = np.linspace(4*60,20*60,num=3)
x_ticks = ['04:00','12:00','20:00']
titles = {1:'No EVs',2:'Uncontrolled',4:'Load Flattening',5:'Loss Minimising'}
n = 1
for typ in [1,2,4,5]:
    plt.subplot(2,2,n)
    n += 1
    plt.fill_between(t_,l[typ],u[typ],color='#c5d9f9')
    plt.plot(t_,m[typ],'b')
    plt.xlim(0,1440)
    plt.xticks(x_,x_ticks)
    plt.title(titles[typ],y=0.85)
    plt.grid()
    plt.ylim(0,3000)
    if n in [2,4]:
        plt.ylabel('Power Losses (W)')
plt.tight_layout()
#plt.savefig('../../Dropbox/papers/losses/total_load.eps', format='eps', dpi=1000)
'''
plt.tight_layout()
plt.savefig('../../Dropbox/papers/losses/losses.eps', format='eps', dpi=1000)

plt.show()
            
