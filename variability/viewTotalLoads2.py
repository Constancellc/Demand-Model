# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/simulation_results/LV/total_load/'

# first get data
results = {1:[],2:[],3:[],4:[],5:[]}
for mc in range(118getMSOA):
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
    plt.fill_between(t_,l[typ],u[typ],color='#c5d9f9')
    plt.plot(t_,m[typ],'b')
    plt.xlim(0,1440)
    plt.xticks(x_,x_ticks)
    plt.title(titles[typ],y=0.85)
    plt.ylim(0,90)
    plt.grid()
    if n in [2,4]:
        plt.ylabel('Power (kW)')
plt.tight_layout()
plt.savefig('../../Dropbox/papers/losses/img/total_load.eps', format='eps', dpi=1000)
plt.show()
            
