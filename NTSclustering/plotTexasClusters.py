import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

# Texas
data = '../../Documents/NHTS/constance/texas-trips.csv'
labels =  '../../Documents/simulation_results/NHTS/clustering/labels/'


wProfiles = {}
weProfiles = {} #weekend analysis would be a good extension

nDays = {}
wDays = {}

DM = {'1':'7','2':'1','3':'2','4':'3','5':'4','6':'5','7':'6'}
KM = {0:2,1:1,2:0}
KM2 = {0:2,1:0,2:1}

# first get all of the data points 
with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]
        
        if vehicle == '':
            continue
        elif vehicle == ' ':
            continue

        weekday = DM[row[2]]
        wDays[vehicle] = weekday

        if weekday in ['6','7']:
            profiles = weProfiles
        else:
            profiles = wProfiles
            
        try:
            start = int(row[5])
            end = int(row[6])
        except:
            continue

        distance = float(row[7])
        
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
with open(labels+'NHTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            NTS[row[0]] = int(row[1])
        except:
            continue

# get the labels for both data types
with open(labels+'NHTSLabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            NTS[row[0]] = int(row[1])
        except:
            continue

# now check the
totalsWD = {}
for d in range(1,8):
    totalsWD[str(d)] = [0]*3
for v in NTS:
    d = wDays[v]
    if int(d) < 6:
        k = KM[NTS[v]]
    else:
        k = KM2[NTS[v]]
    totalsWD[d][k] += 1

c1 = [0.0]*7
c2 = [0.0]*7
c3 = [0.0]*7

for d in totalsWD:
    t = sum(totalsWD[d])
    c3[int(d)-1] = 100*totalsWD[d][0]/t
    c2[int(d)-1] = c3[int(d)-1]+100*totalsWD[d][1]/t
    c1[int(d)-1] = 100

 
plt.figure(figsize=(5,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.bar(range(5),[100]*5,color='#FFBBBB')
plt.bar(range(5),c2[:5],color='#BBBBFF')
plt.bar(range(5),c3[:5],color='#BBFFBB')
plt.bar(range(5,7),[100]*2,color='#FFFFBB')
plt.bar(range(5,7),c2[5:],color='#FFBBFF')
plt.bar(range(5,7),c3[5:],color='#BBFFFF')
plt.xticks(range(7),['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
for d in range(7):
    plt.annotate('3',(d-0.1,c3[d]/2))
    plt.annotate('2',(d-0.1,c3[d]-3+(c2[d]-c3[d])/2))
    plt.annotate('1',(d-0.1,c2[d]-3+(c1[d]-c2[d])/2))
        
plt.ylim(0,100)
plt.ylabel('Percentage')
#plt.grid(zorder=1)
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/composition_tx.eps', format='eps', dpi=1000)
plt.show()


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
    plt.subplot(1,3,KM[k]+1)

    mean = get_av(wAvs[k])
    lower,upper = get_bounds(wAvs[k],0.9)
        
    plt.plot(np.arange(0.5,48.5),mean,clrs[str(KM[k])])

    plt.fill_between(np.arange(0.5,48.5),lower,upper,color=clrs2[str(KM[k])])

    plt.ylim(0,40)
    if KM[k] == 0:
        plt.ylabel('Average Speed (mph)')
    plt.title(str(KM[k]+1),y=0.7)
    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid(ls=':')
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/texas_weekday_clusters.eps', format='eps', dpi=1000)


plt.figure(figsize=(5,1.35))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']
clrs = {'0':'y','1':'m','2':'c'}
clrs2 = {'0':'#FFFFCC','1':'#FFCCFF','2':'#CCFFFF'}
for k in range(3):
    plt.subplot(1,3,KM2[k]+1)

    mean = get_av(weAvs[k])
    lower,upper = get_bounds(weAvs[k],0.9)
        
    plt.plot(np.arange(0.5,48.5),mean,clrs[str(KM2[k])])

    plt.fill_between(np.arange(0.5,48.5),lower,upper,color=clrs2[str(KM2[k])])

    plt.ylim(0,40)
    if KM2[k] == 0:
        plt.ylabel('Average Speed (mph)')
    plt.title(str(KM2[k]+1),y=0.7)
    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid(ls=':')
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/texas_weekend_clusters.eps', format='eps', dpi=1000)


plt.show()
