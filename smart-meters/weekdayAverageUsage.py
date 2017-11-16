import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime
import copy

data = '../../Documents/sharonb/7591/csv/profiles.csv'
dates = '../../Documents/sharonb/7591/csv/dates.csv'

days = {}
n = {}
for i in range(1,8):
    days[str(i)] = [0.0]*48
    n[str(i)] = 0

with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:

        profile = row[2:50]
        wday = row[-1]

        for i in range(0,48):
            days[wday][i] += float(profile[i])

        n[wday] += 1

for day in days:
    for i in range(0,48):
        days[day][i] = days[day][i]/n[day]

lbls = {'1':'Monday','2':'Tuesday','3':'Wednesday','4':'Thursday','5':'Friday',
        '6':'Saturday','7':'Sunday'}
x_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
x = range(4,52,8)

plt.figure(1)
for day in days:
    plt.plot(days[day],label=lbls[day])
plt.xticks(x,x_ticks)
plt.legend()
plt.show()
