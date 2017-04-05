import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
import random
from operator import itemgetter

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'

overallHistogram = [0]*13
charges = {}
lengthsBetweenCharges = {}

with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        ID = row[0]

        if ID != 'GC06':
            continue
            
        finalSOC = int(row[4])
        overallHistogram[finalSOC] += 1

        startTime = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                      int(row[1][8:10]),int(row[1][11:13]),
                                      int(row[1][14:16]))
        endTime = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                      int(row[2][8:10]),int(row[2][11:13]),
                                      int(row[2][14:16]))
        
        if ID not in charges:
            charges[ID] = []

        charges[ID].append(startTime)
        #charges[ID].append(endTime)

N = sum(overallHistogram)

for i in range(0,13):
    overallHistogram[i] = float(overallHistogram[i])/N
    
plt.figure(1)
plt.bar(range(0,13),overallHistogram)
plt.title('State of Charge (out of 12) on Unplug')

times = [0]*800

for ID in charges:
    charges[ID] = sorted(charges[ID])
    lengthsBetweenCharges[ID] = []
    
    #for i in range(0,len(charges[ID])/2-1):
        #timedelta = charges[ID][2*i+2]-charges[ID][2*i+1]
    for i in range(0,len(charges[ID])-1):
        timedelta = charges[ID][i+1]-charges[ID][i]
        dayGap = timedelta.days
        minGap = timedelta.seconds/60
        gap = dayGap*1440+minGap

        lengthsBetweenCharges[ID].append(gap)
        

for ID in lengthsBetweenCharges:
    for gap in lengthsBetweenCharges[ID]:
        try:
            times[gap/60] += 1
        except:
            print gap

plt.figure(2)
plt.bar(range(0,800),times)
plt.xlim(0,150)
#plt.ylim(0,5000)
plt.title('Histogram of gap between consecutive charges')
plt.ylabel('frequency')
plt.xlabel('time (hours)')


plt.show()


    
