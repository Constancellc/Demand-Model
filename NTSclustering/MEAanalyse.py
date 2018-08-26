import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

use = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'
charge = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'
    
wProfiles = {}
weProfiles = {} #weekend analysis would be a good extension

nDays = {}

# I have two obectives here:
#   1. how often do people begin charging after a journey
#   2. the relationship between distance and energy expenditure

distances = []
energys = []
distances2 = []
energys2 = []
distances3 = []
energys3 = []

endTimes = {}

def calc_closest(p,l):
    d = 1440
    best = None

    for i in range(len(l)):
        new = abs(p-l[i])
        if new < d:
            d = new
            best = l[i]

    return [d,best]

# first get all of the data points 
with open(use,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]
        day = int(row[1])

        if vehicle not in endTimes:
            endTimes[vehicle] = {}

        if day not in endTimes[vehicle]:
            endTimes[vehicle][day] = []

        if int(row[4]) < 20000:
            distances.append(int(row[4]))
            energys.append(int(row[5]))

        elif int(row[4]) < 60000:
            distances2.append(int(row[4]))
            energys2.append(int(row[5]))

        else:
            distances3.append(int(row[4]))
            energys3.append(int(row[5]))

        end = int(row[3])

        if end > 1440:
            day += 1
            if day not in endTimes[vehicle]:
                endTimes[vehicle][day] = []

            end -= 1440
            
        # note end times can be greater than 1440
        endTimes[vehicle][day].append(int(row[3]))

y = 0
n = 0

y2 = 0
n2 = 0

pdf = [0]*200
with open(charge,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]
        day = int(row[1])

        if vehicle not in endTimes:
            continue
        if day not in endTimes[vehicle]:
            continue # may want to reconsider later

        start = int(row[2])

        [dist,best] = calc_closest(start,endTimes[vehicle][day])

        try:
            pdf[dist] += 1
        except:
            continue

        if best == endTimes[vehicle][day][-1]:
            y2 += 1
        else:
            n2 += 1

        if dist > 2:
            n += 1
        else:
            y += 1


            
p = np.polyfit(distances,energys,1)
p2 = np.polyfit(distances2,energys2,1)
p3 = np.polyfit(distances3,energys3,1)
print(p)
print(p2)
print(p3)

print(100*y/(n+y))

print(100*y2/(n2+y2))

x = range(max(distances))
x2 = range(max(distances2))
x3 = range(max(distances3))
y = []
y2 = []
y3 = []
for i in range(len(x)):
    y.append(p[0]*x[i]+p[1])
for i in range(len(x2)):
    y2.append(p2[0]*x2[i]+p2[1])
for i in range(len(x3)):
    y3.append(p3[0]*x3[i]+p3[1])
plt.figure()
plt.scatter(distances,energys)
plt.scatter(distances2,energys2)
plt.scatter(distances3,energys3)
plt.plot(x,y)
plt.plot(x2,y2)
plt.plot(x3,y3)
plt.show()
