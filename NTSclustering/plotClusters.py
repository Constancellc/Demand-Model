import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'
labels =  '../../Documents/simulation_results/NTS/clustering/labels2/'


wProfiles = {}
weProfiles = {} #weekend analysis would be a good extension

nDays = {}

# first get all of the data points 
with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[2]
        
        if vehicle == '':
            continue
        elif vehicle == ' ':
            continue

        weekday = int(row[6])

        vehicle += row[6]

        if weekday < 6:
            profiles = wProfiles
        else:
            profiles = weProfiles
            
        try:
            start = int(row[9])
            end = int(row[10])
        except:
            continue

        distance = float(row[11])
        
        if vehicle not in profiles:
            profiles[vehicle] = [0]*48

        if start < end:
            l = end-start
        else:
            l = end+24*60-start

        distPerMin = distance/l
        
        for t in range(start,end):
            if t < 1440:
                profiles[vehicle][int(t/30)] += distPerMin*2
            else:
                profiles[vehicle][int((t-1440)/30)] += distPerMin*2

wAvs = {}
weAvs = {}
for k in range(3):
    wAvs[k] = {}
    weAvs[k] = {}
    for t in range(48):
        wAvs[k][t] = []
        weAvs[k][t] = []

NTS = {}
# get the labels for both data types
with open(labels+'NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS[row[0]] = int(row[1])

# get the labels for both data types
with open(labels+'NTSlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS[row[0]] = int(row[1])

for v in wProfiles:
    if v not in NTS:
        continue
    for t in range(48):
        wAvs[NTS[v]][t].append(wProfiles[v][t])
for v in weProfiles:
    if v not in NTS:
        continue
    for t in range(48):
        weAvs[NTS[v]][t].append(weProfiles[v][t])

def get_av(dic):
    av = []
    for t in range(48):
        av.append(sum(dic[t])/len(dic[t]))
    return av

def get_bounds(dic,conf):
    alpha = (1-conf)/2
    lower = []
    upper = []
    for t in range(48):
        x = sorted(dic[t])
        lower.append(x[int(alpha*len(x))])
        upper.append(x[int((1-alpha)*len(x))])
    return lower,upper

plt.figure(figsize=(5,1.35))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']
clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}
clrs2 = {'2':'#CCFFCC','3':'#FFFFCC','1':'#CCCCFF','0':'#FFCCCC','4':'#CCFFFF'}

for k in range(3):
    plt.subplot(1,3,k+1)

    mean = get_av(wAvs[k])
    lower,upper = get_bounds(wAvs[k],0.9)
        
    plt.plot(np.arange(0.5,48.5),mean,clrs[str(k)])

    plt.fill_between(np.arange(0.5,48.5),lower,upper,color=clrs2[str(k)])

    plt.ylim(0,30)
    if k == 0:
        plt.ylabel('Average Speed (mph)')
    plt.title(str(k+1),y=0.7)
    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid(ls=':')
    plt.tight_layout()
    plt.savefig('../../Dropbox/papers/uncontrolled/img/weekday_clusters.eps', format='eps', dpi=1000)


plt.figure(figsize=(5,1.35))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']
clrs = {'0':'y','1':'m','2':'c'}
clrs2 = {'0':'#FFFFCC','1':'#FFCCFF','2':'#CCFFFF'}
for k in range(3):
    plt.subplot(1,3,k+1)

    mean = get_av(weAvs[k])
    lower,upper = get_bounds(weAvs[k],0.9)
        
    plt.plot(np.arange(0.5,48.5),mean,clrs[str(k)])

    plt.fill_between(np.arange(0.5,48.5),lower,upper,color=clrs2[str(k)])

    plt.ylim(0,30)
    if k == 0:
        plt.ylabel('Average Speed (mph)')
    plt.title(str(k+1),y=0.7)
    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid(ls=':')
    plt.tight_layout()
    plt.savefig('../../Dropbox/papers/uncontrolled/img/weekend_clusters.eps', format='eps', dpi=1000)


plt.show()
