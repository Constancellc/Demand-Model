import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime

trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'
#mea = '../../Documents/My_Electric_Avenue_Technical_Data/EVTripData.csv'

vehicles = {}
distances = {}
monday = {}
tuesday = {}
wednesday = {}
thursday = {}
friday = {}
saturday = {}
sunday = {}

week = {1:monday, 2:tuesday, 3:wednesday, 4:thursday, 5:friday, 6:saturday,
        7:sunday}


i = 2 # index of vehicle no
with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        if row[i] == '' or row[i] == ' ':
            continue
        if row[i] not in vehicles:
            vehicles[row[i]] = 1
            distances[row[i]] = 0.0
            monday[row[i]] = 0
            tuesday[row[i]] = 0
            wednesday[row[i]] = 0
            thursday[row[i]] = 0
            friday[row[i]] = 0
            saturday[row[i]] = 0
            sunday[row[i]] = 0
        else:
            vehicles[row[i]] += 1

        day = int(row[5])
        week[day][row[i]] += 1

        distances[row[i]] += float(row[10])

# first i'm going to plot the number of trips per week undertaken by a vehicle

y = [0]*200
x = range(0,200)

for vehicle in vehicles:
    n = vehicles[vehicle]
    try:
        y[n] += 1
    except:
        print vehicle
plt.figure(1)

plt.bar(x,y)
plt.xlim(0,80)
plt.title('Number of Trips per Vehicle in 1 Week')
plt.xlabel('number of trips')
plt.ylabel('frequency')


# now I want to plot the number of trips per day undertaken by any vehicle

weekdays = [0]*40
weekends = [0]*40
x2 = range(0,40)

for day in [monday,tuesday,wednesday,thursday,friday]:
    for vehicle in day:
        n = day[vehicle]
        try:
            weekdays[n] += 1
        except:
            print vehicle
            print n
for day in [saturday,sunday]:
    for vehicle in day:
        n = day[vehicle]
        weekends[n] += 1

plt.figure(2)
plt.bar(x2,weekdays,label='Weekday')
plt.bar(x2,weekends, bottom=weekdays,label='Weekend')
plt.title('Trips per Day per Vehicle')
plt.xlabel('number of trips')
plt.ylabel('frequency')
plt.legend()
plt.xlim(-1,15)


# now i want to look into the more interesting weekly distance

cap = 1000
f = 1
dist = [0]*(int(cap/f))
zeros = [0]*(int(cap/f))
x3 = np.arange(0,cap,f)

for vehicle in distances:
    n = round(distances[vehicle]/f)
    if n >= cap/f:
        continue
    dist[int(n)] += 1

normalised = []

for i in range(0,len(dist)):
    normalised.append(float(dist[i])/sum(dist))

# getting the MEA data for comparison

distancesMEA = {}

startDates = {}

# first finding participants and start dates

with open('../../Documents/My_Electric_avenue_Technical_Data/Participants.csv') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        ID = row[0]
        
        try:
            delivery = datetime.datetime(int(row[6][:4]),int(row[6][5:7]),
                                     int(row[6][8:10]))
        except:
            delivery = 'NULL'
            print row[6][:4],
            print row[6][5:7],
            print row[6][8:10]
        startDates[ID] = delivery
        
cars = []

with open('../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        userID = row[0]
        if startDates[userID] == 'NULL':
            continue
        if userID not in distancesMEA:
            distancesMEA[userID] = {}
            
        date = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                      int(row[1][8:10]))
        distance = float(row[3])*0.000621 # m -> mi
        energy = float(row[4]) # Wh

        weekNo = (date-startDates[userID]).days/7

        if weekNo not in distancesMEA[userID]:
            distancesMEA[userID][weekNo] = 0.0

        distancesMEA[userID][weekNo] += distance

y4 = [0]*1000
zeros2 = [0]*1000
x4 = range(0,1000)

for ID in distancesMEA:
    for week in distancesMEA[ID]:
        n = int(distancesMEA[ID][week])
        if n == 0:
            continue
        y4[n] += 1

normalised2 = []

for i in range(0,len(y4)):
    normalised2.append(float(y4[i])/sum(y4))

plt.figure(3)

plt.fill_between(x3,zeros,normalised,label='NTS',alpha=0.5)
plt.fill_between(x4,zeros2,normalised2,label='MEA',alpha=0.5)
plt.xlim(-1, 800)
plt.ylim(0,0.008)
plt.title('Distance Driven per Vehicle in 1 Week')
plt.xlabel('miles')
plt.ylabel('probability density')
plt.legend()


plt.show()
