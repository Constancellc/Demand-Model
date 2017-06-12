import csv
import matplotlib.pyplot as plt
import random
import numpy as np

data = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

wProfiles = {}
weProfiles = {}

with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        vehicle = row[2]
        
        if vehicle == '':
            continue
        elif vehicle == ' ':
            continue

        weekday = int(row[5])

        if weekday > 5:
            profiles = weProfiles
        else:
            profiles = wProfiles
        
        try:
            start = int(row[8])
            end = int(row[9])
        except:
            continue
        
        if vehicle not in profiles:
            profiles[vehicle] = [0]*48

        if start < end:
            l = end-start
        else:
            l = end+24*60-start

        start_index = start/30
        delay = start%30

        if l < 30-delay:
            profiles[vehicle][start_index] += l
            l = 0
        else:
            profiles[vehicle][start_index] += 30-delay
            l -= (30-delay)
            index = start_index+1
            if index >= 48:
                index -= 48

        while l > 0:
            if l < 30:
                profiles[vehicle][index] += l
                l = 0
            else:
                profiles[vehicle][index] += 30
                l -= 30
                index += 1
                if index >= 48:
                    index -= 48
wTotal = [0]*48
weTotal = [0]*48

for vehicle in wProfiles:
    for i in range(0,48):
        wTotal[i] += wProfiles[vehicle][i]

for vehicle in weProfiles:
    for i in range(0,48):
        weTotal[i] += weProfiles[vehicle][i]

x = np.arange(8,48,8)
x_ticks = range(4,24,4)
for i in range(0,len(x_ticks)):
    if x_ticks[i] < 10:
        x_ticks[i] = '0'+str(x_ticks[i])+':00'
    else:
        x_ticks[i] = str(x_ticks[i])+':00'

plt.figure(1)
plt.subplot(2,1,1)
plt.bar(range(0,48),wTotal)
plt.title('Week Day')
plt.xticks(x,x_ticks)
plt.xlim(0,48)

plt.subplot(2,1,2)
plt.bar(range(0,48),weTotal)
plt.title('Weekend')
plt.xticks(x,x_ticks)
plt.xlim(0,48)
plt.show()
