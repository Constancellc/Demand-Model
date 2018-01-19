# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)

totals = {0:[],1:[],2:[]}
diffs = [[],[]]

with open('results/lf_lm_losses.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row == []:
            continue
        for i in range(3):
            totals[i].append(100*float(row[i])/float(row[3]))
        diffs[0].append(float(row[4]))
        diffs[1].append(float(row[5]))

av = []
for key in range(3):
    data = totals[key]
    data = sorted(data)
    av.append(data[int(len(data)/2)])
    
x2_ticks = ['Load\nFlattening','Loss\nMinimizing','Uncontrolled']
plt.figure(1)
#plt.subplot(2,1,1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
plt.boxplot([totals[0],totals[1],totals[2]],0,'',whis=[0.05, 99.5])
plt.xticks([1,2,3],x2_ticks)
plt.plot([0.5,3.5],[av[1],av[1]])
plt.grid()
plt.ylabel('Losses (%)')
'''
plt.subplot(2,1,2)
plt.scatter(diffs[0],diffs[1])
#plt.plot([0,],[0,])
plt.ylabel('predicted')
plt.xlabel('observed')
'''
loads = {'lf':[],'lm':[],'uc':[]}
for typ in ['lf','lm','uc']:
    with open('results/'+typ+'_loads.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            profile = []
            for i in range(len(row)):
                profile.append(float(row[i]))
            loads[typ].append(profile)

plt.figure(2)
plt.subplot(1,2,1)
clrs = {'lf':'b','lm':'r','uc':'g'}
for typ in ['lf','lm','uc']:
    h = [0.0]*1440
    l = [0.0]*1440
    m = [0.0]*1440

    for t in range(1440):
        values = sorted(loads[typ][t])
        
        l[t] = values[0]
        h[t] = values[-1]
        m[t] = values[int(len(values)/2)]

    plt.plot(m,clrs[typ])
    plt.fill_between(range(len(m)),l,h,color=clrs[typ],alpha=0.2)

plt.subplot(1,2,2)
for typ in ['lf','lm','uc']:
    av = [0.0]*1440
    for t in range(1440):
        av[t] = sum(loads[typ][t])/len(loads[typ])
    
    plt.plot(av,clrs[typ])

plt.figure(3)
hh = [0,54]
for i in range(2):
    plt.subplot(2,1,i+1)
    lm = []
    lf = []
    bl = []
    with open('results/lf_lm_inidividuals'+str(hh[i])+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row == []:
                continue
            lf.append(float(row[1]))
            lm.append(float(row[2]))
            bl.append(float(row[3]))
        plt.plot(lf)
        plt.plot(lm)
        plt.plot(bl)

plt.show()
plt.show()
            
