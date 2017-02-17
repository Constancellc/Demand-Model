import numpy as np
import matplotlib.pyplot as plt
import random
import csv

timeInterval = 15

times = []
powers = []

day = '02'
month = '01'

with open('pv/GBPV_data.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == 'substation_id':
            continue
        
        if row[1][8:10] != day:
            continue
        elif row[1][5:7] != month:
            continue
        
        print row[1]
        
        hour = int(row[1][11:13])-4
        mins = int(row[1][14:16])
        time = hour*(60/timeInterval)+int(mins/timeInterval)
        times.append(time)
        powers.append(float(row[2]))

print times

t = 24*(60/timeInterval)

interpolated = [0.0]*t

for i in range(0,t):
    if i < times[0]:
        continue
    elif i > times[-1]:
        continue

    gap = times[1]-times[0]

    j = 0
    while times[j] < i and j < t-1:
        j += 1

    distance = times[j] - i
    f = float(distance)/gap

    interpolated[i] = float(int(100*(powers[j]+f*(powers[j-1]-powers[j]))))/100
    
print interpolated

plt.figure(1)
plt.plot(interpolated)
plt.show()


        
