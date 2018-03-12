import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime
import copy
import sys

from clustering import ClusteringExercise
day = '3'

# get profiles
'''
data = '../../Documents/sharonb/7591/csv/profiles.csv'

profiles = {}

with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[-1] != day:
            continue

        if row[0] not in profiles:
            profiles[row[0]] = [0.0]*48

        for i in range(48):
            profiles[row[0]][i] += float(row[i+2])

data = []
hhID = []
for hh in profiles:
    new = []

    for i in range(48):
        new.append(profiles[hh][i]/sum(profiles[hh]))

    data.append(new)
    hhID.append(hh)

with open('../../Documents/sharonb/7591/csv/'+day+'_av.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(data)):
        writer.writerow([hhID[i]]+data[i])
'''

# get data from file

data = []
hhID = []
with open('../../Documents/sharonb/7591/csv/'+day+'_av.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        hhID.append(row[0])
        new = []
        for i in range(48):
            new.append(float(row[i+1]))
        data.append(new)

CE = ClusteringExercise(data)


css = []
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
for k in range(2,11):

    CE.k_means(k)
    css.append(CE.get_sum_of_squares())
    CE.reset_clusters()


plt.plot(range(2,11),css)
plt.xlabel('Number of clusters')
plt.ylabel('Sum of squares')
plt.grid()
clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c','5':'m'}
CE.k_means(2)
n = 1

plt.figure(2)
for label in CE.clusters:
    plt.subplot(2,1,n)

    mean = copy.copy(CE.clusters[label].mean)
    upper, lower = CE.clusters[label].get_cluster_bounds(0.9)
        
    plt.plot(np.arange(0.5,48.5),mean,clrs[label])

    plt.fill_between(np.arange(0.5,48.5),lower,upper,alpha=0.2,color=clrs[label])
    plt.title(str(int(label)+1)+'\n('+
              str(int(CE.clusters[label].nPoints*10000/len(data))/100)+'%)',y=0.7)

    plt.ylim(0,0.125)
    plt.xlim(0.5,47.5)
    n += 1
    plt.grid()

    

CE.reset_clusters()

CE.k_means(6)

n = 1
plt.figure(3)
for label in CE.clusters:
    plt.subplot(3,2,n)

    mean = copy.copy(CE.clusters[label].mean)
    upper, lower = CE.clusters[label].get_cluster_bounds(0.9)
        
    plt.plot(np.arange(0.5,48.5),mean,clrs[label])

    plt.fill_between(np.arange(0.5,48.5),lower,upper,alpha=0.2,color=clrs[label])
    plt.title(str(int(label)+1)+'\n('+
              str(int(CE.clusters[label].nPoints*10000/len(data))/100)+'%)',y=0.7)

    plt.ylim(0,0.125)
    plt.xlim(0.5,47.5)
    n += 1
    plt.grid()
plt.show()
