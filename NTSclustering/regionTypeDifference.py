import csv
import matplotlib.pyplot as plt
import random
import numpy as np
from clustering import Cluster, ClusteringExercise


data = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'

rTypes = {}

with open(households,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    for row in reader:
        rTypes[row[0]] = row[149]

wProfiles = {}
weProfiles = {}

nDays = {}

rt = {}
with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        rt[row[2]] = rTypes[row[1]]
        vehicle = row[2]
        
        if vehicle == '':
            continue
        elif vehicle == ' ':
            continue

        weekday = int(row[5])

        if weekday > 5:
            profiles = weProfiles
        else:
            profiles = wProfiles
            
        try:
            start = int(row[8])
            end = int(row[9])
        except:
            continue

        distance = float(row[10])
            
        if vehicle not in profiles:
            profiles[vehicle] = [0]*48
       

        if start < end:
            l = end-start
        else:
            l = end+24*60-start

        distPerMin = distance/l

        start_index = int(start/30)
        delay = start%30

        if l < 30-delay:
            profiles[vehicle][start_index] += l*distPerMin
            l = 0
        else:
            profiles[vehicle][start_index] += (30-delay)*distPerMin
            l -= (30-delay)
            index = start_index+1
            if index >= 48:
                index -= 48

        while l > 0:
            if l < 30:
                profiles[vehicle][index] += l*distPerMin
                l = 0
            else:
                profiles[vehicle][index] += 30*distPerMin
                l -= 30
                index += 1
                if index >= 48:
                    index -= 48
        
wTotal = [0]*48
weTotal = [0]*48

# first scale all of the distances:
maxWDist = 0.0
maxWeDist = 0.0

for vehicle in wProfiles:
    for i in range(0,48):
        if wProfiles[vehicle][i] > maxWDist:
            maxWDist = wProfiles[vehicle][i]
                
for vehicle in weProfiles:
    for i in range(0,48):
        if weProfiles[vehicle][i] > maxWeDist:
            maxWeDist = weProfiles[vehicle][i]
                
        
# max Distance isn't what i actuall want to use, come back here!
for vehicle in wProfiles:
    for i in range(0,48):
        wProfiles[vehicle][i] = float(wProfiles[vehicle][i])/maxWDist
        wTotal[i] += wProfiles[vehicle][i]

for vehicle in weProfiles:
    for i in range(0,48):
        weProfiles[vehicle][i] = float(weProfiles[vehicle][i])/maxWeDist
        weTotal[i] += weProfiles[vehicle][i]


clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}

data = []

for vehicle in wProfiles:
    data.append(wProfiles[vehicle]+[rt[vehicle]])

random.shuffle(data)

plainData = []
rts = []

for i in range(0,len(data)):
    plainData.append(data[i][:len(data[i])-1])
    rts.append(data[i][-1])

sampleN = 20000

CE = ClusteringExercise(plainData[:sampleN])
CE.k_means(4)

nPerClst = {}

for clst in CE.clusters:

    for pointName in CE.clusters[clst].points:
        rtype = rts[int(pointName)]

        if rtype not in nPerClst:
            nPerClst[rtype] = {}

        if clst not in nPerClst[rtype]:
            nPerClst[rtype][clst] = 0

        nPerClst[rtype][clst] += 1

print(nPerClst)

labels = {'1':'Urban Conurbation','2':'Urban Town','3':'Rural Town','4':'Rural Village'}
x_ticks = ['1','2','3','4']
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
for rt in nPerClst:
    if rt == '5':
        continue
    per = [0]*4
    for clst in nPerClst[rt]:
        per[int(clst)] += nPerClst[rt][clst]

    tot = sum(per)
    for i in range(0,4):
        per[i] = per[i]*100/tot
    plt.bar(np.arange(0,4)+0.2*int(rt),per,width=0.2,label=labels[rt],alpha=0.5)
    #plt.title(titles[rt])
    plt.ylim(0,100)
    
    plt.xlim(0,4)
    plt.xticks(np.arange(0.5,4.5),x_ticks)
    plt.ylabel('% points')
    plt.grid()
plt.legend()

x = [12,24,36]
x_ticks = ['06:00','12:00','18:00']
plt.figure(2)
plt.rcParams["font.family"] = 'serif'
for clst in CE.clusters:
    plt.subplot(2,2,int(clst)+1)
    plt.title(str(int(clst)+1),y=0.8)
    plt.xlim(0,48)
    plt.ylim(0,0.4)
    plt.plot(CE.clusters[clst].mean)
    plt.xticks(x,x_ticks)
    plt.grid()
    
plt.show()
