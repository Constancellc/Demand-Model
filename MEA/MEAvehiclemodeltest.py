import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from cvxopt import matrix, spdiag, solvers, sparse

results = []
#distances = []
#energies = []

distanceVsEnergy = {}

cars = []

with open('../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[0]
        
        year = row[1][:4]
        month = row[1][5:7]
        day = row[1][8:10]
        outHour = int(row[1][11:13])
        outMins = int(row[1][14:16])
        outSecs = int(row[1][17:19])
        backHour = int(row[2][11:13])
        backMins = int(row[2][14:16])
        backSecs = int(row[2][17:19])
        distance = float(row[3]) # m
        energy = float(row[4]) # Wh

        if outHour == backHour:
            timeLength = (backMins-outMins)*60+(backSecs-outSecs)
        elif outHour < backHour:
            timeLength = (backHour-outHour)*3600+(backMins-outMins)*60+\
                         (backSecs-outSecs)
        else:
            timeLength = (backHour-outHour+24)*3600+(backMins-outMins)*60+\
                         (backSecs-outSecs)
        if int(distance) == 0:
            continue
        if timeLength > 30000:
            continue
            
        if userID[0:2] not in cars:
            cars.append(userID[0:2])
            currentCar = userID[0:2]
            distanceVsEnergy[userID[0:2]] = {'distances':[],'energies':[],
                                             'times':[]}

        distanceVsEnergy[currentCar]['distances'].append(distance)
        distanceVsEnergy[currentCar]['energies'].append(energy)
        distanceVsEnergy[currentCar]['times'].append(timeLength)
        

        #distances.append(distance)
        #energies.append(energy)

#distances = np.array(distances)
#energies = np.array(energies)

plt.figure(1)
plt.subplot(2,1,1)
for userID in cars:
    plt.scatter(distanceVsEnergy[userID]['distances'],
                distanceVsEnergy[userID]['energies'],label=userID,alpha=0.4)
    plt.xlabel('distance (m)')
    plt.ylabel('energy expenditure (Wh)')
plt.subplot(2,1,2)
for userID in cars:
    plt.scatter(distanceVsEnergy[userID]['times'],
                distanceVsEnergy[userID]['energies'],label=userID,alpha=0.4)
    plt.xlabel('trip time (s)')
    plt.ylabel('energy expenditure (Wh)')
plt.show()


