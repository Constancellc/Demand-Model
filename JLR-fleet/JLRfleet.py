import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

rnd = 10

# first getting the JLR distances
weeklyDistanceJLR = {}
with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[0]
        
        if userID not in weeklyDistanceJLR:
            weeklyDistanceJLR[userID] = {}
            
        dayNo = int(row[1])
        weekNo = dayNo/7

        if weekNo not in weeklyDistanceJLR[userID]:
            weeklyDistanceJLR[userID][weekNo] = 0

        distance = int(row[5])
        weeklyDistanceJLR[userID][weekNo] += distance

jlr_distances = [0]*int(1000/rnd)

for user in weeklyDistanceJLR:
    for week in weeklyDistanceJLR[user]:
        try:
            jlr_distances[int(weeklyDistanceJLR[user][week]/1609)/rnd] += 1
        except:
            print int(weeklyDistanceJLR[user][week]/1609)


# now getting other datasets for comparison, MEA first
weeklyDistanceMEA = {}
with open('../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[0]
        
        if userID not in weeklyDistanceMEA:
            weeklyDistanceMEA[userID] = {}
            
        dayNo = int(row[1])
        weekNo = dayNo/7

        if weekNo not in weeklyDistanceMEA[userID]:
            weeklyDistanceMEA[userID][weekNo] = 0

        distance = int(row[4])
        weeklyDistanceMEA[userID][weekNo] += distance

mea_distances = [0]*int(1000/rnd)

for user in weeklyDistanceMEA:
    for week in weeklyDistanceMEA[user]:
        try:
            mea_distances[int(weeklyDistanceMEA[user][week]/1609)/rnd] += 1
        except:
            print int(weeklyDistanceMEA[user][week]/1609)

# and lastly NTS, surveys were only 1 week long so no need to look into date

weeklyDistanceNTS = {}
with open('../../Documents/UKDA-5340-tab/csv/tripsUseful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        vehicleID = row[2]
        distance = float(row[10])

        if vehicleID not in weeklyDistanceNTS:
            weeklyDistanceNTS[vehicleID] = 0.0

        weeklyDistanceNTS[vehicleID] += distance
    
nts_distances = [0]*int(2000/rnd)

for user in weeklyDistanceNTS:
    try:
        nts_distances[int(weeklyDistanceNTS[user])/rnd] += 1
    except:
        print int(weeklyDistanceNTS[user])
            
# normalising
for dist in [jlr_distances,mea_distances,nts_distances]:
    s = sum(dist)
    for i in range(0,len(dist)):
        dist[i] = float(dist[i])/s

plt.figure(1)
plt.plot(range(0,2000,rnd),nts_distances,label='NTS Fleet')#,alpha=0.3)
plt.plot(range(0,1000,rnd),mea_distances,label='MEA Fleet')#,alpha=0.3)
plt.plot(range(0,1000,rnd),jlr_distances,label='JLR Fleet')#,alpha=0.3)
plt.ylabel('probability density')
plt.xlabel('weekly distance (miles)')
plt.legend()
plt.xlim(0,600)
plt.ylim(0,0.06)
plt.show()

    
