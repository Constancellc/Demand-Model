# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/simulation_results/LV/total_load/'
stem2 = '../../Documents/simulation_results/LV/total_load30/'

# first get data
results = {1:[],2:[],3:[],4:[],5:[]}
for mc in range(118):
    with open(stem+str(mc+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        new = {1:[],2:[],3:[],4:[],5:[]}
        for row in reader:
            for i in range(1,len(row)):
                new[i].append(float(row[i]))
        for i in range(1,6):
            results[i].append(new[i])

# then find mean and bounds for each
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
    plt.fill_between(t_,l[typ],u[typ],color='b',alpha=0.2)#CCCCFF')
    plt.plot(t_,m[typ],'b',label='100%')
    plt.xlim(0,1440)
    plt.xticks(x_,x_ticks)
    plt.title(titles[typ],y=0.85)
    plt.ylim(0,90)
    plt.grid()
    if n in [2,4]:
        plt.ylabel('Power (kW)')

# first get data
results = {1:[],2:[],3:[],4:[],5:[]}
for mc in range(97):
    with open(stem2+str(mc+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        new = {1:[],2:[],3:[],4:[],5:[]}
        for row in reader:
            for i in range(1,len(row)):
                new[i].append(float(row[i]))
        for i in range(1,6):
            results[i].append(new[i])

# then find mean and bounds for each
m2 = {1:[],2:[],3:[],4:[],5:[]}
u2 = {1:[],2:[],3:[],4:[],5:[]}
l2 = {1:[],2:[],3:[],4:[],5:[]}

for typ in results:
    for t in range(1440):
        x = []
        for mc in range(len(results[1])):
            x.append(results[typ][mc][t])
        x = sorted(x)
        l2[typ].append(x[0])
        u2[typ].append(x[-1])
        m2[typ].append(x[int(len(x)/2)])

# now plot results
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
t_ = range(0,1440)
x_ = np.linspace(4*60,20*60,num=3)
x_ticks = ['04:00','12:00','20:00']
titles = {1:'No EVs',2:'Uncontrolled',4:'Load Flattening',5:'Loss Minimising'}
n = 2
for typ in [2,4,5]:
    plt.subplot(2,2,n)
    n += 1
    #plt.fill_between(t_,l2[typ],u[typ],color='b',alpha=0.2)#'#CCCCCC')
    plt.fill_between(t_,l2[typ],l[typ],color='#FFCCCC')
    plt.fill_between(t_,l[typ],u2[typ],color='#CC99CC')
    plt.plot(t_,m2[typ],'r',label='50%')
plt.legend()
    
plt.tight_layout()
plt.savefig('../../Dropbox/papers/losses/img/total_load.eps', format='eps', dpi=1000)
plt.show()
            
