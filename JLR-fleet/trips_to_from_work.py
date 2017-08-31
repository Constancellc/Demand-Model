import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

# what percentage of trips are to or from work?
for mode in ['weekday']:#,'weekend']:
    nTripsToFromWork = {}
    nTripsToFromHome = {}
    nTrips = {}

    with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            userID = row[0]

            if mode == 'weekday':
                if int(row[2]) > 5:
                    continue
            else:
                if int(row[2]) < 6:
                    continue

            if userID not in nTrips:
                nTrips[userID] = 0
                nTripsToFromWork[userID] = 0
                nTripsToFromHome[userID] = 0
                
            nTrips[userID] += float(row[6])

            if row[7] == '1' or row[8] == '1':
                nTripsToFromWork[userID] += float(row[6])
            if row[9] == '1' or row[10] == '1':
                nTripsToFromHome[userID] += float(row[6])

    if mode == 'weekday':    
        plt.figure(1)
        offset = 0
    else:
        offset = 0.5
        
    #plt.subplot(2,1,1)

    percent = [0]*101

    for user in nTrips:
        percent[int(nTripsToFromWork[user]*100/nTrips[user])] += 1

    # normalise
    s = sum(percent)
    for i in range(0,101):
        percent[i] = float(percent[i])/s

    plt.bar(np.arange(offset,101+offset),percent,0.45)
    plt.xlabel('Percentage of distance to or from work')
    plt.ylabel('Probability')
    plt.xlim(0,100)
    '''
    plt.subplot(2,1,2)
    percent = [0]*101

    for user in nTrips:
        percent[int(nTripsToFromHome[user]*100/nTrips[user])] += 1

    # normalise
    s = sum(percent)
    for i in range(0,101):
        percent[i] = float(percent[i])/s

    plt.bar(np.arange(offset,101+offset),percent,0.45)
    plt.xlabel('Percentage of trips to or from home')
    plt.ylabel('Probability')
    plt.xlim(0,100)
    '''

plt.show()

