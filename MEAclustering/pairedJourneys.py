import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
import random

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'

users = []
vehicles = ['GC08']#,'GC06','GC08','GC10']

journeys = {}
earliest = {}
latest = {}

data = {'charge':chargeData, 'use':tripData}

overallHistogram = [0]*13

with open(tripData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:

        if row[0] not in users:
            users.append(row[0])
            journeys[row[0]] = {}
            earliest[row[0]] = datetime.datetime.now()
            latest[row[0]] = datetime.datetime(2010,01,01)

        day = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),int(row[1][8:10]))

        if day not in journeys[row[0]]:
            journeys[row[0]][day] = 1
        else:
            journeys[row[0]][day] += 1

        if day < earliest[row[0]]:
            earliest[row[0]] = day
        if day > latest[row[0]]:
            latest[row[0]] = day

for user in users:
    day = earliest[user]
    while day < latest[user]:
        if day not in journeys[user]:
            journeys[user][day] = 0
        day += datetime.timedelta(1)

plt.figure(1)

n = 30
x = range(0,n)
y_weekdays = [0]*n
y_weekends = [0]*n

for vehicle in users:#vehicles:
    for day in journeys[vehicle]:
        if journeys[vehicle][day] >= n:
            print 'skipping'
            continue
        if day.weekday() < 5:
            y_weekdays[journeys[vehicle][day]] += 1
        else:
            y_weekends[journeys[vehicle][day]] += 1

plt.bar(x,y_weekdays,label='Weekdays')
plt.bar(x,y_weekends,bottom=y_weekdays,label='Weekends')
plt.title('Number of trips per day across all vehicles')#for vehicle '+vehicle)
plt.xlabel('trips')
plt.ylabel('frequency')
plt.xlim(-1,17)
plt.legend()

plt.show()
    
