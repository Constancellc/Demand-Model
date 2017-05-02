import csv
import datetime
import matplotlib.pyplot as plt
import random
from operator import itemgetter

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges.csv'
newChargeData = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges2.csv'
rangeData =  '../../Documents/My_Electric_avenue_Technical_Data/constance/ranges.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'

charges = {}
trips = {}

with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:

        if row[0] not in charges:
            charges[row[0]] = []

        day = int(row[1])
        start = int(row[2])

        iSOC = float(row[4])
        fSOC = float(row[5])

        if iSOC == fSOC:
            continue

        charges[row[0]].append([day*24*60+start,iSOC,fSOC])

with open(tripData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:

        if row[0] not in trips:
            trips[row[0]] = []

        day = int(row[1])
        start = int(row[2])

        energy = int(row[5]) # Wh

        trips[row[0]].append([day*24*60,energy])
    
        
for vehicle in charges:
    charges[vehicle] = sorted(charges[vehicle], key=itemgetter(0))
    trips[vehicle] = sorted(trips[vehicle], key=itemgetter(0))
        
chargeEnergy = {}

for vehicle in charges:
    chargeEnergy[vehicle] = {}
    
    energyReq = 0
    j = 0
    for i in range(0,len(charges[vehicle])):
        nTrips = len(trips[vehicle])
        while trips[vehicle][j][0] < charges[vehicle][i][0] and j < nTrips-1:
            energyReq += trips[vehicle][j][1]
            j += 1

        if charges[vehicle][i][2] == 1.0:
            if energyReq > 24000:
                energyReq = 24000
            chargeEnergy[vehicle][charges[vehicle][i][0]] = energyReq
            energyReq = 0
        else:
            amountCharged = int(24000*(float(charges[vehicle][i][2])-
                                       float(charges[vehicle][i][1])))
            chargeEnergy[vehicle][charges[vehicle][i][0]] = amountCharged

            energyReq = 24000-int(float(charges[vehicle][i][2])*24000)
            

with open(newChargeData,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID','day No','start time','end time','intial SOC',
                     'final SOC','weekend?','energy (Wh)'])
    with open(chargeData,'rU') as csvfile2:
        reader = csv.reader(csvfile2)
        reader.next()
        for row in reader:
            vehicle = row[0]
            day = int(row[1])
            start = int(row[2])
            
            try:
                row += [chargeEnergy[vehicle][day*24*60+start]]
            except:
                row += [0]

            writer.writerow(row)
