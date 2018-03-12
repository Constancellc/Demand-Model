import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise



data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

rTypes = {}

      
wProfiles = {}
weProfiles = {}

nDays = {}

sHist = [0.0]*60

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

        if weekday > 5:
            profiles = weProfiles
        else:
            profiles = wProfiles
            
        try:
            start = int(row[9])
            end = int(row[10])
        except:
            continue

        sHist[start%60] += 1

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
                profiles[vehicle][int(t/30)] += distPerMin/5
            else:
                profiles[vehicle][int((t-1440)/30)] += distPerMin/5

        ''''

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
        '''
        
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

    
data = []
for vehicle in wProfiles:
    data.append(wProfiles[vehicle])

random.shuffle(data)

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

sampleN = 30000
CE = ClusteringExercise(data[:sampleN])

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

css = []
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
for k in range(1,11):
    plt.subplot(3,4,k)

    CE.k_means(k)
    css.append(CE.get_sum_of_squares())
    #'''
    for label in CE.clusters:
        plt.plot(CE.clusters[label].mean,label=str(int(CE.clusters[label].nPoints*100/sampleN))+'%')
    '''
    medians = CE.get_cluster_median()
    for label in medians:
        plt.plot(medians[label],label=str(CE.clusters[label].nPoints))

    '''
    plt.legend()

    CE.reset_clusters()
    plt.title('k='+str(k),y=0.8)
    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.ylim(0,0.35)
    plt.grid()

plt.figure(3)
plt.plot(range(1,11),css,linestyle='-',marker='x')
plt.xlabel('Number of clusters')
plt.ylabel('Within cluster sum of squares')
plt.grid()

s = sum(sHist)
for i in range(60):
    sHist[i] = sHist[i]/s
    
plt.figure(4)
plt.bar(range(60),sHist)
plt.xlabel('Mins past hour of journey start time')
plt.ylabel('Probability')
plt.grid()
plt.show()
