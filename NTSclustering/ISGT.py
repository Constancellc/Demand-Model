import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise
import scipy.ndimage


data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

rTypes = {}

      
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
for vehicle in weProfiles:
    data.append(weProfiles[vehicle])

random.shuffle(data)

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

plt.figure(5)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
for i in range(9):
    plt.subplot(3,3,i+1)
    plt.ylim(0,0.2)
    plt.plot(data[i])
    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid()
    
sampleN = 30000
CE = ClusteringExercise(data[:sampleN])

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

css = []
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
for k in range(2,11):
    plt.subplot(3,4,k-1)

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
plt.plot(range(2,11),css)
plt.xlabel('Number of clusters')
plt.ylabel('Distance between two closest centroids')
plt.grid()

fig = plt.figure(2)
CE.k_means(5)
n = 1

clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}

locs = {1:[2.5,-0.4],2:[1.3,-0.6],3:[0.1,-0.8],4:[2.5,0.2],5:[1.3,0.0]}
pdfs = {}
for label in CE.clusters:
    pdfs[label] = CE.clusters[label].distance_pdf(maxWDist,200)
    plt.subplot(2,3,n)

    mean = copy.copy(CE.clusters[label].mean)
    upper, lower = CE.clusters[label].get_cluster_bounds(0.9)
    # convert to mph
    for i in range(48):
        mean[i] = mean[i]*maxWDist*2
        upper[i] = upper[i]*maxWDist*2
        lower[i] = lower[i]*maxWDist*2
        
    plt.plot(np.arange(0.5,48.5),mean,clrs[label],
             label=str(CE.clusters[label].get_av_distance(maxWDist,1))+' miles')

    plt.fill_between(np.arange(0.5,48.5),lower,upper,alpha=0.2,color=clrs[label])

    plt.ylim(0,35)
    if n == 1 or n ==4:
        plt.ylabel('Average Speed (mph)')

    plt.title(str(int(label)+1)+'\n('+
              str(int(CE.clusters[label].nPoints*10000/sampleN)/100)+'%)',y=0.7)

    plt.xlim(0,48)
    plt.xticks(x,x_ticks)
    plt.grid()
    plt.legend(loc=locs[n],frameon=False)


    n += 1


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
            av[i] += meaProfiles[vehicle][day][i]/(n*maxWDist)
    test_data.append(av)
    
plt.figure(4)
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
plt.legend()
plt.grid()
plt.xlabel('Cluster #')
plt.ylabel('Probability')

plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
for label in pdfs:
    plt.subplot(2,3,int(label)+1)

    pdf = pdfs[label]
    pdf = scipy.ndimage.filters.gaussian_filter1d(pdf,5)
    plt.title(str(int(label)+1)+'\n('+str(round(100*sum(pdf[:85]),2))+'%)',y=0.65)
    plt.bar(np.arange(85),pdf[:85],width=1,color='b',label='< 85')
    plt.bar(np.arange(85,200),pdf[85:],width=1,color='r',label='> 85')
    plt.xlim(0,150)
    plt.ylim(0,0.06)
    if label in ['3','4']:
        plt.xlabel('Distance (miles)')
    if label in ['0','3']:
        plt.ylabel('Probability (%)')
        plt.yticks([0.02,0.04,0.06],['2','4','6'])
    else:
        plt.yticks([0.02,0.04,0.06],['','',''])
                   
    if label == '0':
        plt.legend(loc=[2.5,-0.7])
    plt.grid()
    

plt.show()
