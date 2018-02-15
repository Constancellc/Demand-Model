# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)

totals = {0:[],1:[],2:[],3:[]}
diffs = [[],[]]

with open('results/lf_lm_losses.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row == []:
            continue
        for i in range(4):
            totals[i].append(100*float(row[i])/float(row[4]))
        #diffs[0].append(100*float(row[4])/float(row[4]))
        #diffs[1].append(100*float(row[5])/float(row[4]))

av = []
for key in range(3):
    data = totals[key]
    data = sorted(data)
    av.append(data[int(len(data)/2)-1])
    
x2_ticks = ['Load\nFlattening','Loss\nMinimizing','Psuedo\nOptimal',
            'Uncontrolled']
plt.figure(1)
#plt.subplot(2,1,1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 10
plt.boxplot([totals[0],totals[1],totals[2],totals[3]],0,'',whis=[0.05, 99.5])
plt.xticks([1,2,3,4],x2_ticks)
plt.plot([0.5,4.5],[av[1],av[1]],'k',ls=':',alpha=0.5)
plt.grid()
plt.ylabel('Losses (%)')

plt.figure(4)
plt.scatter(diffs[0],diffs[1])
#plt.plot([0,],[0,])
plt.ylabel('predicted')
plt.xlabel('observed')

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
        av[t] = sum(loads[typ][t])/(55*len(loads[typ][t]))
    
    plt.plot(av,clrs[typ])

plt.figure(3)
hh = [0,54]
for i in range(2):
    plt.subplot(2,1,i+1)
    lm = [0.0]*1440
    lf = [0.0]*1440
    bl = [0.0]*1440
    with open('results/lf_lm_inidividuals'+str(hh[i])+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        r = 0
        for row in reader:
            if row == []:
                continue
            for c in range(100):
                lf[r] += float(row[3*c+1])/100
                lm[r] += float(row[3*c+2])/100
                bl[r] += float(row[3*c+3])/100
            r += 1
    plt.plot(lf,label='load flattening')
    plt.plot(lm,label='loss minimising')
    plt.plot(bl,'k',ls=':',alpha=0.5,label='base load')
    plt.grid()
    plt.ylim(0,1)
    plt.ylabel('Power (kW)')
    plt.title('Household '+str(hh[i]+1))
    plt.xlim(0,1440)

plt.legend(loc=[0.2,2.3],ncol=3)
plt.show()
            
