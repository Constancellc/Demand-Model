import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

weekdays = {}

with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        weekday = row[2]
        hour = int(float(row[4])/60)

        if weekday not in weekdays:
            weekdays[weekday] = [0]*24

        weekdays[weekday][hour] += 1

days = {'1':'Mon','2':'Tue','3':'Wed','4':'Thur','5':'Fri','6':'Sat','7':'Sun'}
plt.figure(1)
for day in weekdays:
    plt.subplot(4,2,int(day))
    plt.bar(np.arange(0.5,24.5),weekdays[day],0.9)
    plt.title(days[day],y=0.75)
    plt.xlim(0,24)
    plt.ylim(0,8500)
plt.show()
