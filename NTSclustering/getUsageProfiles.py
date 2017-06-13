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


def polyfit(series,dof,plot=False,clr='b'):
    p_ = np.polyfit(range(0,len(series)),series,dof)

    def p(x):
        rv = 0
        for i in range(0,len(p_)):
            rv += p_[len(p_)-1-i]*x**i
        return rv

    y = []
    for i in np.arange(0,len(series),0.1):
        y.append(p(i))

    if plot == True:
        plt.plot(np.arange(0,len(series),0.1),y,clr)

    return p_


x = np.arange(8,48,8)
x_ticks = range(4,24,4)
for i in range(0,len(x_ticks)):
    if x_ticks[i] < 10:
        x_ticks[i] = '0'+str(x_ticks[i])+':00'
    else:
        x_ticks[i] = str(x_ticks[i])+':00'
        
wTotal = [0]*48
weTotal = [0]*48

clrs = ['k','r','b','g','y']

plt.figure(1)
plt.subplot(2,1,1)
n = 0
for vehicle in wProfiles:
    if n < 5:
            polyfit(wProfiles[vehicle],20,plot=True,clr=clrs[n])
            plt.plot(range(0,48),wProfiles[vehicle],clrs[n]+'x')
            n += 1
    for i in range(0,48):
        wTotal[i] += wProfiles[vehicle][i]

plt.subplot(2,1,2)
n = 0
for vehicle in weProfiles:
    if n < 5:
            polyfit(weProfiles[vehicle],20,plot=True,clr=clrs[n])
            plt.plot(range(0,48),weProfiles[vehicle],clrs[n]+'x')
            n += 1
    for i in range(0,48):
        weTotal[i] += weProfiles[vehicle][i]

plt.figure(2)
plt.subplot(2,1,1)
plt.bar(range(0,48),wTotal)
polyfit(wTotal,20,plot=True)
plt.title('Week Day')
plt.xticks(x,x_ticks)
plt.xlim(0,48)

plt.subplot(2,1,2)
plt.bar(range(0,48),weTotal)
polyfit(weTotal,20,plot=True)
plt.title('Weekend')
plt.xticks(x,x_ticks)
plt.xlim(0,48)
plt.show()
