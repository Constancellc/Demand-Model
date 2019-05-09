import csv
import matplotlib.pyplot as plt
import random
import numpy as np

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'
data2 = '../../Documents/NHTS/constance/texas-trips.csv'
stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

# this assigns the Texas clusters to the UK ones

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

n = 0
for profiles in [wProfiles, weProfiles]:
    for v in profiles:
        n += 1
        s = sum(profiles[v])
        if s == 0:
            continue
        for t in range(48):
            profiles[v][t] = profiles[v][t]/s
print(n)
# first get centroids
stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

clst = {0:[0.0]*48,1:[0.0]*48,2:[0.0]*48}
clstWE = {0:[0.0]*48,1:[0.0]*48,2:[0.0]*48}
nClst = {0:0,1:0,2:0}
nClstWE = {0:0,1:0,2:0}
           
with open(stem+'NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        k = int(row[1])
        nClst[k] += 1
        for t in range(48):
            clst[k][t] += wProfiles[row[0]][t]
with open(stem+'NTSlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        k = int(row[1])
        nClstWE[k] += 1
        for t in range(48):
            clstWE[k][t] += weProfiles[row[0]][t]

for k in range(3):
    for t in range(48):
        clst[k][t] = clst[k][t]/nClst[k]
        clstWE[k][t] = clstWE[k][t]/nClstWE[k]

def euc(a,b):
    d = 0
    for i in range(len(a)):
        d += np.power(a[i]-b[i],2)
    return d

def assign_to_clst(p,WE=False):
    if WE == False:
        cls = clst
    else:
        cls = clstWE
    lwst = 1000000
    best = None
    for k in range(3):
        d = euc(p,cls[k])
        if d < lwst:
            lwst = d
            best = k
    return best

# now get texas data
wProfiles = {}
weProfiles = {}
with open(data2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        v = row[0]
        d = row[2]

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
                
n = 0
for profiles in [wProfiles, weProfiles]:
    for v in profiles:
        n += 1
        s = sum(profiles[v])
        if s == 0:
            continue
        for t in range(48):
            profiles[v][t] = profiles[v][t]/s
print(n)

NHTS = {}
for v in wProfiles:
    k = assign_to_clst(wProfiles[v])
    NHTS[v] = k
NHTS2 = {}
for v in weProfiles:
    k = assign_to_clst(weProfiles[v],WE=True)
    NHTS2[v] = k

with open(stem+'texasLabels.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for v in NHTS:
        writer.writerow([v,NHTS[v]])
with open(stem+'texasLabelsWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for v in NHTS2:
        writer.writerow([v,NHTS2[v]])
