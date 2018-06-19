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


CE.k_means(5)
n = 1

clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}

locs = {1:[2.5,-0.4],2:[1.3,-0.6],3:[0.1,-0.8],4:[2.5,0.2],5:[1.3,0.0]}

for label in CE.clusters:
    plt.subplot(2,3,int(label)+1)

    pdf = CE.clusters[label].distance_pdf(maxWDist,200)
    pdf = scipy.ndimage.filters.gaussian_filter1d(pdf,5)
    plt.title(str(int(label)+1)+'\n('+str(round(100*sum(pdf[:85]),2))+'%)',y=0.7)
    plt.bar(np.arange(85),pdf[:85],width=1,color='b',label='< 85 miles')
    plt.bar(np.arange(85,200),pdf[85:],width=1,color='r',label='> 85 miles')
    plt.xlim(0,150)
    plt.ylim(0,0.06)
    if label in ['3','4']:
        plt.xlabel('Distance (miles)')
    if label in ['0','3']:
        plt.ylabel('Probability')
    if label == '0':
        plt.legend(loc=[2.5,-0.8])

plt.show()



