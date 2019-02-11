# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/simulation_results/LV/manc-models/'

# first get data
results = {1:[],2:[],3:[],4:[]}
fs = {1:'b',2:'u',3:'f',4:'m'}

for r in results:
    with open(stem+'1-loads-'+fs[r]+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for t in range(1440):
            results[r].append([])
        t = 0
        for row in reader:
            for i in range(1,len(row)):
                results[r][t].append(float(row[i]))
            t += 1

# then find mean and bounds for each
m = {1:[],2:[],3:[],4:[]}
u = {1:[],2:[],3:[],4:[]}
l = {1:[],2:[],3:[],4:[]}

for typ in results:
    for t in range(1440):
        x = sorted(results[typ][t])
        l[typ].append(x[int(len(x)*0.1)])
        u[typ].append(x[int(len(x)*0.9)])
        m[typ].append(x[int(len(x)/2)])

# now plot results
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
t_ = range(0,1440)
x_ = np.linspace(4*60,20*60,num=3)
x_ticks = ['04:00','12:00','20:00']
titles = {1:'No EVs',2:'Uncontrolled',3:'Load Flattening',4:'Loss Minimising'}


for typ in [1,2,3,4]:
    plt.subplot(2,2,typ)
    plt.fill_between(t_,l[typ],u[typ],color='#CCCCFF')
    plt.plot(t_,m[typ],'b')
    plt.xlim(0,1440)
    plt.xticks(x_,x_ticks)
    plt.title(titles[typ],y=0.78)
    plt.ylim(0,100)
    plt.grid()
    if typ in [1,3]:
        plt.ylabel('Power (kW)')
    
plt.tight_layout()
plt.savefig('../../Dropbox/papers/losses/img/total_load.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
            
