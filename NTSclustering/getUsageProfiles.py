import csv
import matplotlib.pyplot as plt
import random
import numpy as np
from clustering import Cluster, ClusteringExercise

data = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

wProfiles = {}
weProfiles = {}

nDays = {}

with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
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
        
        if vehicle not in profiles:
            profiles[vehicle] = [0]*48

        if start < end:
            l = end-start
        else:
            l = end+24*60-start

        start_index = int(start/30)
        delay = start%30

        if l < 30-delay:
            profiles[vehicle][start_index] += l
            l = 0
        else:
            profiles[vehicle][start_index] += 30-delay
            l -= (30-delay)
            index = start_index+1
            if index >= 48:
                index -= 48

        while l > 0:
            if l < 30:
                profiles[vehicle][index] += l
                l = 0
            else:
                profiles[vehicle][index] += 30
                l -= 30
                index += 1
                if index >= 48:
                    index -= 48
        
wTotal = [0]*48
weTotal = [0]*48

for vehicle in wProfiles:
    for i in range(0,48):
        wProfiles[vehicle][i] = float(wProfiles[vehicle][i])/150 # 5days*30mins
        wTotal[i] += wProfiles[vehicle][i]

for vehicle in weProfiles:
    for i in range(0,48):
        weProfiles[vehicle][i] = float(weProfiles[vehicle][i])/150 # 5days*30mins
        weTotal[i] += weProfiles[vehicle][i]

    
data = []
for vehicle in wProfiles:
    data.append(wProfiles[vehicle])

'''
x = np.arange(8,48,8)
x_ticks = range(4,24,4)
for i in range(0,len(x_ticks)):
    if x_ticks[i] < 10:
        x_ticks[i] = '0'+str(x_ticks[i])+':00'
    else:
        x_ticks[i] = str(x_ticks[i])+':00'
'''



CE = ClusteringExercise(data[:10000])


plt.figure(1)
for k in range(2,8):
    plt.subplot(3,2,k-1)

    CE.k_means(k)
    for label in CE.clusters:
        plt.plot(CE.clusters[label].mean,label=str(CE.clusters[label].nPoints))
    plt.legend()

    CE.reset_clusters()
    plt.title('k='+str(k),y=0.8)

plt.show()
