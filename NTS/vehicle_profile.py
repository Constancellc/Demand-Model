import csv
import matplotlib.pyplot as plt
import random
import numpy as np

rawData = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

profiles = {}
vehicles = []

with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        if row[7] != '2014':
            continue
        vehicle = row[2]


        try:
            start = int(row[8])+int(row[5])*24*60
            end = int(row[9])+int(row[5])*24*60
        except:
            continue

        
        if vehicle not in vehicles:
            vehicles.append(vehicle)
            profiles[vehicle] = [0]*(24*60*7)

        if start >= 24*60*7:
            start -= 24*60*7
        if end >= 24*60*7:
            end -= 24*60*7

        if start < end:
            for i in range(start,end):
                profiles[vehicle][i] = 1
        else:
            for i in range(start,24*60*7):
                profiles[vehicle][i] = 1
            for i in range(0,end):
                profiles[vehicle][i] = 1

num_plot = 3

t = np.linspace(0,24*7,num=24*60*7)
x = np.linspace(8,160,num=14)
x_ticks = ['8AM \n Mon','8PM','8AM \n Tue','8PM','8AM \n Wed','8PM',
           '8AM \n Thu','8PM','8AM \n Fri','8PM','8AM \n Sat','8PM',
           '8AM \n Sun','8PM']

plt.figure(1)
for i in range(0,num_plot):
    ID = vehicles[int(random.random()*len(vehicles))];
    plt.plot(t,profiles[ID])
plt.xticks(x,x_ticks)
plt.xlim(0,24*7)
plt.ylabel('in use')

plt.show()
