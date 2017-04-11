import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
import random
from operator import itemgetter

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'

charges = {}
trips = {}
Float = {}

with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        ID = row[0]

        startTime = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                      int(row[1][8:10]),int(row[1][11:13]),
                                      int(row[1][14:16]))
        endTime = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                      int(row[2][8:10]),int(row[2][11:13]),
                                      int(row[2][14:16]),int(row[1][17:19]))
        
        if ID not in charges:
            charges[ID] = []

        charges[ID].append(endTime)

with open(tripData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        ID = row[0]
        
        tripTime = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                     int(row[1][8:10]),int(row[1][11:13]),
                                     int(row[1][14:16]),int(row[1][17:19]))
        if ID not in trips:
            trips[ID] = []

        trips[ID].append(tripTime)
        #charges[ID].append(endTime)

y = []
yerrP = []
yerrM = []
for ID in charges:
    charges[ID] = sorted(charges[ID])
    trips[ID] = sorted(trips[ID])

    
    Float[ID] = []

    for charge in charges[ID]:
        i = 0
        try:
            while trips[ID][i] < charge:
                i += 1
            nextJourney = trips[ID][i]
        except:
            continue

        possibleSlip = (nextJourney-charge).seconds
        #print charge
        #print nextJourney
        #print trips[ID][i-1]
        #print ''
        Float[ID].append(possibleSlip)

    av = sum(Float[ID])/len(Float[ID])
    var = 0

    for p in Float[ID]:
        var += (p-av)*(p-av)

    if len(charges[ID]) < 5:
        continue
    y.append(av)

    sd = math.sqrt(float(var)/len(Float[ID]))
    yerrP.append(sd)

    if sd < av:
        yerrM.append(sd)
    else:
        yerrM.append(av)
    #yerrM.append(av-min(Float[ID]))
    if av > 700*60:
        print ID
    
#y.sort()   
#print Float

y_sorted = []
yerrP_sorted = []
yerrM_sorted = []

index = range(0,len(y))

while len(index) > 0:
    best = len(y)
    smallest = 1000000
    for i in index:

        if y[i] < smallest:
            best = i
            smallest = y[i]
    y_sorted.append(y[best])
    yerrP_sorted.append(yerrP[best])
    yerrM_sorted.append(yerrM[best])

    index.remove(best)

        
        
        
plt.figure(1)
plt.errorbar(range(0,len(y)),y_sorted,yerr=[yerrM_sorted, yerrP_sorted], fmt='o')

plt.xlabel('vehicle')
plt.ylabel('average float time (seconds)')
plt.title('The Elasticity of Vehicle Load')

plt.show()    
