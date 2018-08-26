import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise

# This is the case for single day clustering rather than week average

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

data3 = '../../Documents/NHTS/constance/trips_useful.csv'

stem = '../../Documents/simulation_results/NTS/clustering/labels/'


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

wProfiles2 = {}
weProfiles2 = {}
# now get the MEA data
with open(data2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]+row[1]
        
        if row[-1] == '0':
            profiles = wProfiles2
        else:
            profiles = weProfiles2
        
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

wProfiles3 = {}
weProfiles3 = {}

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

        weekday = int(row[7])

        if weekday < 6:
            profiles = wProfiles
        else:
            profiles = weProfiles
            
        try:
            start = int(row[5])
            end = int(row[16])
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
       
# normalise
for vehicle in wProfiles:
    for i in range(0,48):
        wProfiles[vehicle][i] = float(wProfiles[vehicle][i])/maxWDist
for vehicle in weProfiles:
    for i in range(0,48):
        weProfiles[vehicle][i] = float(weProfiles[vehicle][i])/maxWeDist
        
for vehicle in wProfiles2:
    for i in range(0,48):
        wProfiles2[vehicle][i] = float(wProfiles2[vehicle][i])/maxWDist
for vehicle in weProfiles2:
    for i in range(0,48):
        weProfiles2[vehicle][i] = float(weProfiles2[vehicle][i])/maxWeDist

for vehicle in wProfiles3:
    for i in range(0,48):
        wProfiles3[vehicle][i] = float(wProfiles3[vehicle][i])/maxWDist
for vehicle in weProfiles3:
    for i in range(0,48):
        weProfiles3[vehicle][i] = float(weProfiles3[vehicle][i])/maxWeDist


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


for label in CE.clusters:
    plt.subplot(1,3,int(label)+1)

    mean = copy.copy(CE.clusters[label].mean)
    upper, lower = CE.clusters[label].get_cluster_bounds(0.9)
    
    # convert to mph
    for i in range(48):
        mean[i] = mean[i]*maxWDist*2
        upper[i] = upper[i]*maxWDist*2
        lower[i] = lower[i]*maxWDist*2
        
    plt.plot(np.arange(0.5,48.5),mean,clrs[label])#,label=str(CE.clusters[label].get_av_distance(maxWDist,1))+' miles')

    plt.fill_between(np.arange(0.5,48.5),lower,upper,color=clrs2[label])

    plt.ylim(0,70)
    if label in ['0','3']:
        plt.ylabel('Average Speed (mph)')
    print(CE.clusters[label].get_av_distance(maxWDist,1))

    plt.title(str(int(label)+1)+'\n('+
              str(int(CE.clusters[label].nPoints*10000/sampleN)/100)+'%)',y=0.6)

    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid()
    #plt.legend(loc=locs[label],frameon=False)
    plt.tight_layout()
    plt.savefig('../../Dropbox/papers/clustering/img/weekday_clusters.eps', format='eps', dpi=1000)


# then find the cluster ssociated with each of the vehicles in the conventional
# data set and store in csv file

trainingLabels = CE.labels
labels = {}
for i in range(sampleN):
    labels[chosen[i]] = trainingLabels[i]
for i in range(len(data)):
    clst = CE.find_nearest(data[i][1:])
    labels[data[i][0]] = clst

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

# then do the same for the US data
labels = {}
for vehicle in wProfiles3:
    clst = CE.find_nearest(wProfiles3[vehicle])
    labels[vehicle] = clst

with open(stem+'USlabels.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for vehicle in labels:
        writer.writerow([vehicle,labels[vehicle]])

# next repeat for weekends
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

for label in CE.clusters:
    plt.subplot(1,3,int(label)+1)

    mean = copy.copy(CE.clusters[label].mean)
    upper, lower = CE.clusters[label].get_cluster_bounds(0.9)
    
    # convert to mph
    for i in range(48):
        mean[i] = mean[i]*maxWeDist*2
        upper[i] = upper[i]*maxWeDist*2
        lower[i] = lower[i]*maxWeDist*2
        
    plt.plot(np.arange(0.5,48.5),mean,clrs[label])
    print(CE.clusters[label].get_av_distance(maxWeDist,1))

    plt.fill_between(np.arange(0.5,48.5),lower,upper,color=clrs2[label])

    plt.ylim(0,75)
    if label in ['0','3']:
        plt.ylabel('Average Speed (mph)')

    plt.title(str(int(label)+1)+'\n('+
              str(int(CE.clusters[label].nPoints*10000/sampleN)/100)+'%)',y=0.6)

    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid()
    #plt.legend(loc=locs[label],frameon=False)
    plt.tight_layout()
    plt.savefig('../../Dropbox/papers/clustering/img/weekend_clusters.eps', format='eps', dpi=1000)

# then find the cluster ssociated with each of the vehicles in the conventional
# data set and store in csv file

trainingLabels = CE.labels
labels = {}
for i in range(sampleN):
    labels[chosen[i]] = trainingLabels[i]
for i in range(len(data)):
    clst = CE.find_nearest(data[i][1:])
    labels[data[i][0]] = clst

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
        
# then do the same for the US data
labels = {}
for vehicle in weProfiles3:
    clst = CE.find_nearest(weProfiles3[vehicle])
    labels[vehicle] = clst

with open(stem+'USlabelsWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for vehicle in labels:
        writer.writerow([vehicle,labels[vehicle]])
        
plt.show()
# this is the only clustering we will need to do, from now on it will
# just be analysis
