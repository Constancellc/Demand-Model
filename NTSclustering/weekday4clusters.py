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

    
data = []
for vehicle in wProfiles:
    data.append(wProfiles[vehicle])

random.shuffle(data)

sampleN = 30000
CE = ClusteringExercise(data[:sampleN])

x = range(4,52,8)
x_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']

plt.figure(1)
for k in range(2,8):
    plt.subplot(3,2,k-1)

    CE.k_means(k)
    #'''
    for label in CE.clusters:
        plt.plot(CE.clusters[label].mean,label=str(CE.clusters[label].nPoints))
    '''
    medians = CE.get_cluster_median()
    for label in medians:
        plt.plot(medians[label],label=str(CE.clusters[label].nPoints))

    '''
    plt.legend()

    CE.reset_clusters()
    plt.title('k='+str(k),y=0.8)

plt.figure(2)
CE.k_means(4)
n = 1

clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}

for label in CE.clusters:
    plt.subplot(2,2,n)
    plt.plot(np.arange(0.5,48.5),CE.clusters[label].mean,clrs[label],
             label=str(CE.clusters[label].get_av_distance(maxWDist,7))+' miles')

    upper, lower = CE.clusters[label].get_cluster_bounds(0.9)
    plt.fill_between(np.arange(0.5,48.5),lower,upper,alpha=0.2,color=clrs[label])

    plt.ylim(0,0.6)

    plt.title(str(int(CE.clusters[label].nPoints*10000/sampleN)/100)+'%',
              y = 0.85)

    plt.xlim(0,48)
    plt.xticks(x,x_ticks)

    plt.legend()

    n += 1

plt.show()
