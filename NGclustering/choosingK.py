import matplotlib.pyplot as plt
import numpy as np
import csv
import sklearn.cluster as clst
import datetime

maxDemand = 0

profiles = {}
with open('../../Documents/gridwatch.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        '''
        year = row[1][:4]
        month = row[1][5:7]
        day = int(row[1][8:10]
        '''        
        date = row[1][:11]
        
        if date not in profiles:
            profiles[date] = [0.0]*24*12
            
        time = int(int(row[1][11:13])*12+int(row[1][14:16])/5)

        demand = int(row[2])

        if demand > maxDemand:
            maxDemand = demand

        profiles[date][time] = demand

data = []
dates = []

for date in profiles:
    skip = False

    sf = sum(profiles[date])

    for i in range(24*12):
        if profiles[date][i] == 0:
            skip = True
        if i >= 1:
            if profiles[date][i] == profiles[date][i-1]:
                skip = True
            
        #profiles[date][i] = profiles[date][i]/maxDemand
        profiles[date][i] = profiles[date][i]/sf

    if skip == False:
        data.append(profiles[date])
        dates.append(date)

k_values = range(2,50)
maxDiff = []

for k in k_values:
    centroid, label, inertia = clst.k_means(data,k)

    smallest = 100000000
    for i in range(k-1):
        for j in range(i+1,k):
            d = np.linalg.norm(centroid[i]-centroid[j])
            if d < smallest:
                smallest = d
    maxDiff.append(smallest)

plt.figure(1)
plt.scatter(k_values,maxDiff,marker='x')
plt.xlim(0,len(k_values)+1)
plt.ylim(0,max(maxDiff)*1.05)
plt.xlabel('number of clusters')
plt.ylabel('distance between two closest centroids')
plt.grid()
plt.show()
'''
plt.figure(1)
for j in range(0,6):
    plt.subplot(2,3,1+j)
    centroid, label, inertia = clst.k_means(data,k_values[j])
    smallest = 0
    for i in range(0,k_values[j]):
        plt.plot(centroid[i])
    plt.title('k='+str(k_values[j]))

plt.show()
'''

