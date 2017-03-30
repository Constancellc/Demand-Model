import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import datetime

results = []
#distances = []
#energies = []

distances = {}

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
        if userID not in distances:
            distances[userID] = {}
            
        date = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                      int(row[1][8:10]))
        distance = float(row[3])*0.000621 # m -> mi
        energy = float(row[4]) # Wh

        weekNo = (date-startDates[userID]).days/7

        if weekNo not in distances[userID]:
            distances[userID][weekNo] = 0.0

        distances[userID][weekNo] += distance

y = [0]*1000
zeros = [0]*1000
x = range(0,1000)

for ID in distances:
    for week in distances[ID]:
        n = int(distances[ID][week])
        if n == 0:
            continue
        y[n] += 1

plt.figure(1)
plt.fill_between(x,y,zeros)
plt.show()

