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
            
        time = int(int(row[1][12:14])*12+int(row[1][15:17])/5)

        demand = int(row[2])

        if demand > maxDemand:
            maxDemand = demand

        profiles[date][time] = demand

data = []
dates = []

for date in profiles:
    skip = False
    for i in range(24*12):
        if profiles[date][i] == 0:
            skip = True
        profiles[date][i] = profiles[date][i]/maxDemand

    if skip == False:
        data.append(profiles[date])
        dates.append(date)


k_values = [6,8,10,12,14,16]

plt.figure(1)
for j in range(0,6):
    plt.subplot(2,3,1+j)
    centroid, label, inertia = clst.k_means(data,k_values[j])
    for i in range(0,k_values[j]):
        plt.plot(centroid[i])
    plt.title('k='+str(k_values[j]))

plt.show()

