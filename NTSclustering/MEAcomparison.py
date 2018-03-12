import csv
import matplotlib.pyplot as plt
import random
import numpy as np
from clustering import Cluster, ClusteringExercise

a = [0.0]*48
b = [0.0]*48
c = [0.0]*48

a[12] = 1.0
a[36] = 1.0

b[13] = 1.0
b[37] = 1.0

c[20] = 1.0
c[22] = 1.0

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.subplot(3,1,1)
plt.plot(a)
plt.title('(a)',y=0.6)
plt.xlim(0,48)
plt.grid()
plt.subplot(3,1,2)
plt.plot(b)
plt.title('(b)',y=0.6)
plt.xlim(0,48)
plt.grid()
plt.subplot(3,1,3)
plt.plot(c)
plt.title('(c)',y=0.6)
plt.xlim(0,48)
plt.grid()
plt.show()

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

meaProfiles = {}
with open(data2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        
        if row[-1] == '1': #weekend
            continue
        
        vehicle = row[0]
        day = int(row[1])
        start = int(row[2])
        end = int(row[3])

        if end == start:
            continue

        if end < start:
            end += 1440
            
        distance = float(row[4])*0.000621371192

        distancePerMin = distance/(end-start)

        if vehicle not in meaProfiles:
            meaProfiles[vehicle] = {}
        if day not in meaProfiles[vehicle]:
            meaProfiles[vehicle][day] = [0.0]*48

        if end < 1440:
            for t in range(start,end):
                meaProfiles[vehicle][day][int(t/30)] += distancePerMin
        else:
            if day+1 not in meaProfiles[vehicle]:
                meaProfiles[vehicle][day+1] = [0.0]*48
            for t in range(start,1440):
                meaProfiles[vehicle][day][int(t/30)] += distancePerMin
            for t in range(end-1440):
                meaProfiles[vehicle][day+1][int(t/30)] += distancePerMin
            
# now getting average profiles
test_data = []
for vehicle in meaProfiles:
    av = [0.0]*48
    n = len(meaProfiles[vehicle])
    for day in meaProfiles[vehicle]:
        for i in range(48):
            av[i] += meaProfiles[vehicle][day][i]/n
    test_data.append(av)
        
# get MEA data
      
wProfiles = {}

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

        weekday = int(row[6])

        if weekday > 5:
            continue #profiles = weProfiles
        else:
            profiles = wProfiles
            
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
                profiles[vehicle][int(t/30)] += distancePerMin/5
            else:
                profiles[vehicle][int((t-1440)/30)] += distancePerMin/5
        
wTotal = [0]*48
weTotal = [0]*48

# first scale all of the distances:
maxWDist = 0.0
maxWeDist = 0.0

for vehicle in wProfiles:
    for i in range(0,48):
        if wProfiles[vehicle][i] > maxWDist:
            maxWDist = wProfiles[vehicle][i]
        
# max Distance isn't what i actuall want to use, come back here!
for vehicle in wProfiles:
    for i in range(0,48):
        wProfiles[vehicle][i] = float(wProfiles[vehicle][i])/maxWDist
        wTotal[i] += wProfiles[vehicle][i]

for profile in test_data:
    for i in range(48):
        profile[i] = profile[i]/maxWDist
data = []
for vehicle in wProfiles:
    data.append(wProfiles[vehicle])

random.shuffle(data)

sampleN = 30000
CE = ClusteringExercise(data[:sampleN])

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

css = []
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'

CE.k_means(5)

n = 1

clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}

locs = {1:[2.5,-0.4],2:[1.3,-0.6],3:[0.1,-0.8],4:[2.5,0.2],5:[1.3,0.0]}

for label in CE.clusters:
    plt.subplot(2,3,n)
    plt.plot(np.arange(0.5,48.5),CE.clusters[label].mean,clrs[label],
             label=str(CE.clusters[label].get_av_distance(maxWDist,1))+' miles')

    upper, lower = CE.clusters[label].get_cluster_bounds(0.9)
    plt.fill_between(np.arange(0.5,48.5),lower,upper,alpha=0.2,color=clrs[label])

    plt.ylim(0,0.6)

    plt.title(str(int(label)+1)+'\n('+
              str(int(CE.clusters[label].nPoints*10000/sampleN)/100)+'%)',y=0.7)

    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid()
    plt.legend(loc=locs[n],frameon=False)

    n += 1

plt.figure(2)
NTS = [0.0]*5
MEA = [0.0]*5

# get NTS cluster composition
for j in range(5):
    NTS[j] = CE.clusters[str(j)].nPoints

# for each MEA profile find nearest cluster
for point in test_data:
    closest = CE.find_nearest(point)
    MEA[int(closest)] += 1

# normalise and plot both
sN = sum(NTS)
sM = sum(MEA)


for i in range(5):
    NTS[i] = float(NTS[i])/sN
    MEA[i] = float(MEA[i])/sM


plt.bar(np.arange(1,6)+0.2,MEA,0.4,label='MEA')
plt.bar(np.arange(1,6)-0.2,NTS,0.4,label='NTS')
plt.show()
