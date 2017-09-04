import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

RLPs = {}
with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        userID = row[0]

        if userID not in RLPs:
            RLPs[userID] = {'weekday':[[0]*48,0],'weekend':[[0]*48,0]}

        day = int(row[2])

        if day <= 5:
            dayType = 'weekday'
        else:
            dayType = 'weekend'

        start = int(row[4])
        end = int(row[5])

        if end < start:
            end += 24*60

        if start < end:
            length = end-start

            sIn = int(start/30)
            n = 30-start%30

            if n < length:
                RLPs[userID][dayType][0][sIn] += n
                length -= n

            while length > 30:
                sIn += 1

                if sIn == 48:
                    sIn -= 48
                    
                RLPs[userID][dayType][0][sIn] += n
                length -= 30

            if sIn == 47:
                sIn -= 48

            RLPs[userID][dayType][0][sIn+1] += length

            RLPs[userID][dayType][1] += 1
                


# create heatmap
heatmap = []
heatmap2 = []
nVehicles = 0

# normalise
for userID in RLPs:
    nVehicles += 1
    for dayType in RLPs[userID]:
        N = RLPs[userID][dayType][1]

        if N < 10:
            RLPs[userID][dayType][0] = [0]*48
            continue

        for i in range(0,48):
            RLPs[userID][dayType][0][i] = RLPs[userID][dayType][0][i]/N

    heatmap.append(RLPs[userID]['weekday'][0])
    heatmap2.append(RLPs[userID]['weekend'][0])

mapT = []
mapT2 = []
for i in range(0,48):
    mapT.append([0.0]*nVehicles)
    mapT2.append([0.0]*nVehicles)

for i in range(0,nVehicles):
    for j in range(0,48):
        mapT[j][i] = heatmap[i][j]
        mapT2[j][i] = heatmap2[i][j]
        
x = range(0,nVehicles)
y = range(4,50,8)

y_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']


plt.figure(1)
plt.rcParams["font.family"] = 'serif'

plt.subplot(2,1,1)
plt.imshow(mapT,cmap='coolwarm',aspect=5)
plt.title('Weekdays')
plt.yticks(y,y_ticks)

plt.subplot(2,1,2)
plt.imshow(mapT2,cmap='coolwarm',aspect=5)
plt.title('Weekends')
plt.yticks(y,y_ticks)
plt.xlabel('Vehicle No.')
plt.show()

