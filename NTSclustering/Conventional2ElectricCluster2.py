import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise

# This is the case for single day clustering rather than week average

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'


wProfiles = {}
weProfiles = {} #weekend analysis would be a good extension

nDays = {}
nDaysWE = {}

seen = {}

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

        if weekday < 6:
            profiles = wProfiles
            n = nDays
        else:
            profiles = weProfiles
            n = nDaysWE
            
        if vehicle+row[6] not in seen:
            seen[vehicle+row[6]] = 0
            if vehicle not in n:
                n[vehicle] = 1
            else:
                n[vehicle] += 1
            
        try:
            start = int(row[9])
            end = int(row[10])
        except:
            continue

        vehicle += row[6]

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

del seen

wProfiles2 = {}
weProfiles2 = {}

# now get the MEA data
with open(data2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]
        
        if row[-1] == '0':
            profiles = wProfiles2
        else:
            profiles = weProfiles2
            
        vehicle += row[1]
        
        start = int(row[2])
        end = int(row[3])

        if end == start:
            continue
        elif end < start:
            end += 1440

        distance = float(row[4])/1609 # m -> miles

        if vehicle not in profiles:
            profiles[vehicle] = [0.0]*48

        distPerMin = distance/(end-start)
        
        for t in range(start,end):
            if t < 1440:
                profiles[vehicle][int(t/30)] += distPerMin
            else:
                profiles[vehicle][int((t-1440)/30)] += distPerMin


# work out % of unused vehicles
percentage_used = []

y = 0
n = 0
for vehicle in nDays:
    y += nDays[vehicle]
    n += 5-nDays[vehicle]
percentage_used.append(100*y/(y+n))

y = 0
n = 0
for vehicle in nDaysWE:
    y += nDaysWE[vehicle]
    n += 2-nDaysWE[vehicle]
percentage_used.append(100*y/(y+n))

print(percentage_used)

# normalise
NTS_scales = {}
toRemove = []
toRemoveWE = []
for vehicle in wProfiles:
    s = sum(wProfiles[vehicle])
    if s > 300 or s == 0:
        toRemove.append(vehicle)
        continue
    
    NTS_scales[vehicle] = s
    for i in range(0,48):
        wProfiles[vehicle][i] = float(wProfiles[vehicle][i])/s
        
for vehicle in weProfiles:
    s = sum(weProfiles[vehicle])
    if s > 300 or s == 0:
        toRemoveWE.append(vehicle)
        continue
    
    NTS_scales[vehicle] = s
    for i in range(0,48):
        weProfiles[vehicle][i] = float(weProfiles[vehicle][i])/s

# remove outliers
for vehicle in toRemove:
    del wProfiles[vehicle]
for vehicle in toRemoveWE:
    del weProfiles[vehicle]

MEA_scales = {}
for vehicle in wProfiles2:
    s = sum(wProfiles2[vehicle])
    if s == 0:
        continue
    MEA_scales[vehicle] = s
    for i in range(0,48):
        wProfiles2[vehicle][i] = float(wProfiles2[vehicle][i])/s
for vehicle in weProfiles2:
    s = sum(weProfiles2[vehicle])
    if s == 0:
        continue
    MEA_scales[vehicle] = s
    for i in range(0,48):
        weProfiles2[vehicle][i] = float(weProfiles2[vehicle][i])/s


# this bit will be for finding the number of clusters
'''
data = []
for vehicle in wProfiles:
    data.append(wProfiles[vehicle])

random.shuffle(data)
data = data[:10000]

CE = ClusteringExercise(data)
css = []
plt.figure(figsize=(5,2.2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.subplot(1,2,1)
for k in range(1,11):
    CE.k_means(k)
    css.append(CE.get_sum_of_squares())
    CE.reset_clusters()
plt.plot(range(1,11),css)
plt.grid()
plt.xlim(0.5,10)
plt.xlabel('# Clusters')
plt.ylabel('Sum of Squares')
plt.title('Weekdays')

data = []
for vehicle in weProfiles:
    data.append(weProfiles[vehicle])

random.shuffle(data)
data = data[:10000]

CE = ClusteringExercise(data)
css = []
plt.subplot(1,2,2)
for k in range(1,11):
    CE.k_means(k)
    css.append(CE.get_sum_of_squares())
    CE.reset_clusters()
plt.plot(range(1,11),css)
plt.grid()
plt.xlim(0.5,10)
plt.xlabel('# Clusters')
plt.ylabel('Sum of Squares')
plt.title('Weekends')
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/choosing_k.eps', format='eps', dpi=1000)

plt.show()

'''
# first cluster the wProfiles
data = []
for vehicle in wProfiles:
    data.append([vehicle]+wProfiles[vehicle])
nTotal = len(data)
random.shuffle(data)

sampleN = 25000

data2 = []
chosen = []
for i in range(sampleN):
    data2.append(data[i][1:])
    chosen.append(data[i][0])

data = data[sampleN:]

CE = ClusteringExercise(data2)

CE.k_means(3)

# first plot and save the chosen centroids with confindence intervals on them
plt.figure(figsize=(5,1.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

locs = {'0':[2.68,-0.5],'1':[1.39,-0.7],'2':[0.1,-0.9],'3':[2.68,0.2],'4':[1.39,0.0]}
clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}
clrs2 = {'2':'#CCFFCC','3':'#FFFFCC','1':'#CCCCFF','0':'#FFCCCC','4':'#CCFFFF'}

pts = {}
mean = {}
upper = {}
lower = {}

for c  in range(3):
    mean[c] = [0.0]*48
    upper[c] = [0.0]*48
    lower[c] = [0.0]*48
    pts[c] = {}
    for t in range(48):
        pts[c][t] = []

# first get the training pts
trainingLabels = CE.labels
labels = {}
for i in range(sampleN):
    labels[chosen[i]] = int(trainingLabels[i])
    for t in range(48):
        pts[int(trainingLabels[i])][t].append(data2[i][t]*NTS_scales[chosen[i]]*2)
    
# then add the other pts
for i in range(len(data)):
    c = int(CE.find_nearest(data[i][1:]))
    labels[data[i][0]] = c
    for t in range(48):
        pts[c][t].append(data[i][t+1]*NTS_scales[data[i][0]]*2)

# calculate mean and bounds
for c in range(3):
    N = len(pts[c][t])
    print(N)
    for t in range(48):
        mean[c][t] = sum(pts[c][t])/N

        v = 0
        for i in range(N):
            v += np.power(mean[c][t]-pts[c][t][i],2)/N
        v = np.sqrt(v)

        if mean[c][t]-v > 0:
            lower[c][t] = mean[c][t]-v
        else:
            lower[c][t] = 0
        upper[c][t] = mean[c][t]+v
        
    plt.subplot(1,3,c+1)

    print(sum(mean[c])/2)
        
    plt.plot(np.arange(0.5,48.5),mean[c],clrs[str(c)])
    plt.fill_between(np.arange(0.5,48.5),lower[c],upper[c],color=clrs2[str(c)])
    plt.ylim(0,20)
    if c == 0:
        plt.ylabel('Average Speed (mph)')
    plt.title(str(c+1)+'\n('+str(int(N*100*percentage_used[0]/nTotal)/100)+
              '%)',y=0.65)

    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid()
    #plt.legend(loc=locs[label],frameon=False)
    plt.tight_layout()
    plt.savefig('../../Dropbox/papers/clustering/img/weekday_clusters2.eps', format='eps', dpi=1000)

del pts
del mean
del upper
del lower

# then find the cluster ssociated with each of the vehicles in the conventional
# data set and store in csv file
with open(stem+'NTSlabels.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for vehicle in labels:
        writer.writerow([vehicle,labels[vehicle]])

# then do the same for the EV data
labels = {}
for vehicle in wProfiles2:
    clst = CE.find_nearest(wProfiles2[vehicle])
    labels[vehicle] = clst

with open(stem+'MEAlabels.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for vehicle in labels:
        writer.writerow([vehicle,labels[vehicle]])

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

# first plot and save the chosen centroids with confindence intervals on them
plt.figure(figsize=(5,1.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

locs = {'0':[2.68,-0.5],'1':[1.39,-0.7],'2':[0.1,-0.9],'3':[2.68,0.2],'4':[1.39,0.0]}
clrs = {'0':'y','1':'m','2':'c'}
clrs2 = {'0':'#FFFFCC','1':'#FFCCFF','2':'#CCFFFF'}

pts = {}
mean = {}
upper = {}
lower = {}

for c  in range(3):
    mean[c] = [0.0]*48
    upper[c] = [0.0]*48
    lower[c] = [0.0]*48
    pts[c] = {}
    for t in range(48):
        pts[c][t] = []

# first get the training pts
trainingLabels = CE.labels
labels = {}
for i in range(sampleN):
    labels[chosen[i]] = int(trainingLabels[i])
    for t in range(48):
        pts[int(trainingLabels[i])][t].append(data2[i][t]*NTS_scales[chosen[i]]*2)
    
# then add the other pts
for i in range(len(data)):
    c = int(CE.find_nearest(data[i][1:]))
    labels[data[i][0]] = c
    for t in range(48):
        pts[c][t].append(data[i][t+1]*NTS_scales[data[i][0]]*2)

# calculate mean and bounds
for c in range(3):
    N = len(pts[c][t])
    print(N)
    for t in range(48):
        mean[c][t] = sum(pts[c][t])/N

        v = 0
        for i in range(N):
            v += np.power(mean[c][t]-pts[c][t][i],2)/N
        v = np.sqrt(v)

        if mean[c][t]-v > 0:
            lower[c][t] = mean[c][t]-v
        else:
            lower[c][t] = 0
        upper[c][t] = mean[c][t]+v
        
    plt.subplot(1,3,c+1)

    print(sum(mean[c])/2)
        
    plt.plot(np.arange(0.5,48.5),mean[c],clrs[str(c)])
    plt.fill_between(np.arange(0.5,48.5),lower[c],upper[c],color=clrs2[str(c)])
    plt.ylim(0,20)
    if c == 0:
        plt.ylabel('Average Speed (mph)')
    plt.title(str(c+1)+'\n('+str(int(N*100*percentage_used[1]/nTotal)/100)+
              '%)',y=0.65)

    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid()
    #plt.legend(loc=locs[label],frameon=False)
    plt.tight_layout()
    plt.savefig('../../Dropbox/papers/clustering/img/weekend_clusters2.eps', format='eps', dpi=1000)

# then find the cluster ssociated with each of the vehicles in the conventional
# data set and store in csv file


with open(stem+'NTSlabelsWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for vehicle in labels:
        writer.writerow([vehicle,labels[vehicle]])

# then do the same for the EV data
labels = {}
for vehicle in weProfiles2:
    clst = CE.find_nearest(weProfiles2[vehicle])
    labels[vehicle] = clst

with open(stem+'MEAlabelsWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for vehicle in labels:
        writer.writerow([vehicle,labels[vehicle]])
       
plt.show()
# this is the only clustering we will need to do, from now on it will
# just be analysis
