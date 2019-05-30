import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise

# This is the case for single day clustering rather than week average


data = '../../Documents/NHTS/constance/texas-trips.csv'

#data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

stem = '../../Documents/simulation_results/NHTS/clustering/labels/'

DM = {'1':'7','2':'1','3':'2','4':'3','5':'4','6':'5','7':'6'}


# now get texas data
wProfiles = {}
weProfiles = {}
with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        v = row[0]
        d = DM[row[2]]

        if d in ['6','7']:
            profiles = weProfiles
        else:
            profiles = wProfiles
        try:
            start = int(row[5])
            end = int(row[6])
            dist = float(row[7])
        except:
            continue

        if dist < 0:
            continue
        
        if v not in profiles:
            profiles[v] = [0]*48

        if start < end:
            l = end-start
        else:
            l = end+24*60-start

        distPerMin = dist/l
        
        for t in range(start,end):
            if t < 1440:
                profiles[v][int(t/30)] += distPerMin
            else:
                profiles[v][int((t-1440)/30)] += distPerMin

'''               
n = 0
for profiles in [wProfiles, weProfiles]:
    for v in profiles:
        n += 1
        s = sum(profiles[v])
        if s == 0:
            continue
        for t in range(48):
            profiles[v][t] = profiles[v][t]/s

'''
# normalise
toRemove = []
toRemoveWE = []
for vehicle in wProfiles:
    s = sum(wProfiles[vehicle])
    if s > 300 or s == 0:
        toRemove.append(vehicle)
        continue
    
    for i in range(0,48):
        wProfiles[vehicle][i] = float(wProfiles[vehicle][i])/s
        
for vehicle in weProfiles:
    s = sum(weProfiles[vehicle])
    if s > 300 or s == 0:
        toRemoveWE.append(vehicle)
        continue
    
    for i in range(0,48):
        weProfiles[vehicle][i] = float(weProfiles[vehicle][i])/s

for v in toRemove:
    del wProfiles[v]
for v in toRemoveWE:
    del weProfiles[v]

# first cluster the wProfiles
data = []
for vehicle in wProfiles:
    data.append([vehicle]+wProfiles[vehicle])
nTotal = len(data)
random.shuffle(data)

sampleN = 1000

data2 = []
chosen = []
for i in range(sampleN):
    data2.append(data[i][1:])
    chosen.append(data[i][0])

data = data[sampleN:]

CE = ClusteringExercise(data2)
CE.k_means(3)

pts = {}
for c  in range(3):
    pts[c] = {}
    for t in range(48):
        pts[c][t] = []

# first get the training pts
trainingLabels = CE.labels
labels = {}
for i in range(sampleN):
    labels[chosen[i]] = int(trainingLabels[i])
    for t in range(48):
        pts[int(trainingLabels[i])][t].append(data2[i][t])
    
# then add the other pts
for i in range(len(data)):
    c = int(CE.find_nearest(data[i][1:]))
    labels[data[i][0]] = c
    for t in range(48):
        pts[c][t].append(data[i][t+1])

del wProfiles
del data
del data2
del pts

# then find the cluster ssociated with each of the vehicles in the conventional
# data set and store in csv file
with open(stem+'NHTSlabels.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for vehicle in labels:
        writer.writerow([vehicle,labels[vehicle]])

del CE
del labels

# next repeat for weekends
data = []
for vehicle in weProfiles:
    data.append([vehicle]+weProfiles[vehicle])
nTotal = len(data)

random.shuffle(data)

data2 = []
chosen = []
for i in range(sampleN):
    data2.append(data[i][1:])
    chosen.append(data[i][0])

data = data[sampleN:]

CE = ClusteringExercise(data2)
CE.k_means(3)
pts = {}

for c  in range(3):
    pts[c] = {}
    for t in range(48):
        pts[c][t] = []

# first get the training pts
trainingLabels = CE.labels
labels = {}
for i in range(sampleN):
    labels[chosen[i]] = int(trainingLabels[i])
    for t in range(48):
        pts[int(trainingLabels[i])][t].append(data2[i][t])
    
# then add the other pts
for i in range(len(data)):
    c = int(CE.find_nearest(data[i][1:]))
    labels[data[i][0]] = c
    for t in range(48):
        pts[c][t].append(data[i][t+1])

del weProfiles
del data
del data2
del pts

# then find the cluster ssociated with each of the vehicles in the conventional
# data set and store in csv file
with open(stem+'NHTSlabelsWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for vehicle in labels:
        writer.writerow([vehicle,labels[vehicle]])

del CE
del labels
