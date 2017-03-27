import numpy as np
import matplotlib.pyplot as plt
import random
import datetime
import csv

tripData = '../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'
chargeData = '../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'

data = [tripData, chargeData]

vehicles = []
charges = {}
initialSOC = {}
finalSOC = {}
trips = {}
distance = {}
energy = {}
tripRanges = {}
chargeRanges = {}


with open(data[0]) as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:

        userID = row[0]

        if userID not in vehicles:
            vehicles.append(userID)
            trips[userID] = 0
            distance[userID] = 0.0
            charges[userID] = 0
            initialSOC[userID] = 0.0
            finalSOC[userID] = 0.0
            energy[userID] = 0.0
            tripRanges[userID] = {'earliest':datetime.datetime.now(),
                              'latest':datetime.datetime(2010,01,01)}
            chargeRanges[userID] = {'earliest':datetime.datetime.now(),
                              'latest':datetime.datetime(2010,01,01)}
            

        tripStart = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                            int(row[1][8:10]),int(row[1][11:13]),
                                            int(row[1][14:16]))
        tripEnd = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                             int(row[2][8:10]),int(row[2][11:13]),
                                             int(row[2][14:16]))

        if tripStart < tripRanges[userID]['earliest']:
            tripRanges[userID]['earliest'] = tripStart
        if tripEnd > tripRanges[userID]['latest']:
            tripRanges[userID]['latest'] = tripEnd

        trips[userID] += 1
        energy[userID] += float(row[4]) # m
        distance[userID] += float(row[3]) # Wh


with open(data[1]) as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:

        userID = row[0]
            
        chargeStart = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                            int(row[1][8:10]),int(row[1][11:13]),
                                            int(row[1][14:16]))
        chargeEnd = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                             int(row[2][8:10]),int(row[2][11:13]),
                                             int(row[2][14:16]))

        if chargeStart < chargeRanges[userID]['earliest']:
            chargeRanges[userID]['earliest'] = chargeStart
        if chargeEnd > chargeRanges[userID]['latest']:
            chargeRanges[userID]['latest'] = chargeEnd
            
        initialSOC[userID] += float(row[3])/12
        finalSOC[userID] += float(row[4])/12
        charges[userID] += 1


results = {'ID':[], 'energyConsumed':[], 'initialSOC':[],'finalSOC':[],
           'chargesPerDay':[], 'tripsPerDay':[], 'tripLength':[]}

fieldnames = ['ID','energyConsumed','initialSOC','finalSOC','chargesPerDay',
              'tripsPerDay','tripLength']

for vehicle in vehicles:
    results['ID'].append(vehicle)
    
    tripsRange = (tripRanges[vehicle]['latest']-
                  tripRanges[vehicle]['earliest']).days
    chargeRange = (chargeRanges[vehicle]['latest']-
                   chargeRanges[vehicle]['earliest']).days
    
    results['energyConsumed'].append(energy[vehicle]/trips[vehicle])
    results['initialSOC'].append(initialSOC[vehicle]/charges[vehicle])
    results['finalSOC'].append(finalSOC[vehicle]/charges[vehicle])
    results['chargesPerDay'].append(float(charges[vehicle])/chargeRange)
    results['tripsPerDay'].append(float(trips[vehicle])/tripsRange)
    results['tripLength'].append(distance[vehicle]/trips[vehicle])


with open('MEAclustering/MEAaverages.csv','w') as csvfile:
    dw = csv.DictWriter(csvfile,fieldnames=fieldnames)
    dw.writeheader()
    for i in range(0,len(results['ID'])):
        row = {}
        for field in fieldnames:
            row[field] = results[field][i]
        dw.writerow(row)
    

