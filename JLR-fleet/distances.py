import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

rnd = 10

# first getting the JLR distances
distances = {}

with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        ID = int(row[0])
        if ID not in distances:
            distances[ID] = {}
        day = int(row[1])
        if day not in distances[ID]:
            distances[ID][day] = 0

        distances[ID][day] += int(row[5])

daily = [0]*400

for ID in distances:
    for day in distances[ID]:
        try:
            daily[distances[ID][day]/1000] += 1
        except:
            print distances[ID][day]/1000,
            print 'km'

plt.figure(1)
plt.bar(range(0,400),daily)
plt.show()

    
