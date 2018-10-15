import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise

# This is the case for single day clustering rather than week average

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'
    
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
                profiles[vehicle][int(t/30)] += distPerMin
            else:
                profiles[vehicle][int((t-1440)/30)] += distPerMin

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

for vehicle in weProfiles:
    for i in range(0,48):
        weProfiles[vehicle][i] = float(weProfiles[vehicle][i])/maxWeDist
       

# first cluster the wProfiles
data = []
for vehicle in wProfiles:
    data.append([vehicle]+wProfiles[vehicle])

random.shuffle(data)

sampleN = 10000

data2 = []
chosen = []
for i in range(sampleN):
    data2.append(data[i][1:])
    chosen.append(data[i][0])

data = data[sampleN:]

CE = ClusteringExercise(data2)

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

css = []
plt.figure(figsize=(5,2.3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'
plt.subplot(1,2,1)

for k in range(1,11):

    CE.k_means(k)
    css.append(CE.get_sum_of_squares())

    CE.reset_clusters()

S = max(css)*0.5
for i in range(10):
    css[i] = css[i]/S
    
plt.plot(range(1,11),css)
plt.grid()
plt.xlim(0.5,9.5)
plt.xlabel('# Clusters')
plt.ylabel('Sum of Squares')
plt.title('Weekdays')

# first cluster the wProfiles
data = []
for vehicle in weProfiles:
    data.append([vehicle]+weProfiles[vehicle])

random.shuffle(data)

data2 = []
chosen = []
for i in range(sampleN):
    data2.append(data[i][1:])
    chosen.append(data[i][0])

data = data[sampleN:]

CE = ClusteringExercise(data2)

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

css = []

for k in range(1,11):
    CE.k_means(k)
    css.append(CE.get_sum_of_squares())

for i in range(10):
    css[i] = css[i]/S
    
plt.subplot(1,2,2)
plt.plot(range(1,11),css)
plt.grid()
plt.xlim(0.5,9.5)
plt.xlabel('# Clusters')
plt.title('Weekends')
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/choosing_k.eps', format='eps', dpi=1000)
plt.show()

