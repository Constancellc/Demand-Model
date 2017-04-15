import csv
import matplotlib.pyplot as plt
import numpy as np

from vehicleModelCopy import Drivecycle, Vehicle
fleetSize = 28000000

def getStartTimes(nextday,month):
    startTimes = {}
    with open('../../Documents/UKDA-5340-tab/csv/tripsUseful.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            if row[5] != nextday:
                continue
            if row[6] != month:
                continue
            vehicle = row[2]

            if vehicle not in startTimes:
                startTimes[vehicle] = 24*60
                
            try:
                tripStart = int(row[8])
            except:
                continue

            if tripStart < startTimes[vehicle]:
                startTimes[vehicle] = tripStart

    return startTimes

day = '7' # day of week
nextday = '1'
month = '7' # month

accessoryLoad = {'1':1.4,'2':1.2,'3':0.8,'4':0.35,'5':0.05,'6':0.0,'7':0.0,
                 '8':0.0,'9':0.0, '10':0.3,'11':0.85,'12':1.25}

energy = {}
distance = {}
endTimes = {}
#startTimes = {}
rTypes = {}
rTypes2 = {}

nissanLeaf = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)

# getting region types
with open('../../Documents/UKDA-5340-tab/tab/householdeul2015.tab','rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    reader.next()
    for row in reader:
        householdID = row[0]
        region = row[28]
        regionType1 = row[148] # 1:urban, 2:rural, 3:scotland
        regionType2 = row[149] # 1: uc, 2:ut, 3:rt, 4:rv, 5:scotland

        if householdID not in rTypes:
            rTypes[householdID] = regionType1
            rTypes2[householdID] = regionType2

# predicting energy expenditure
def predictEnergy(day, month, car, regionType=None):
    with open('../../Documents/UKDA-5340-tab/csv/tripsUseful.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            if row[5] != day: # skip trips that are the wrong day of the week
                continue
            if row[6] != month: # or the wrong month
                continue

            if rTypes2[row[1]] != '1':
                continue

            vehicle = row[2]

            if vehicle == ' ': # or have missing vehicle ids
                continue
            
            #household = row[1]
            #purposeFrom = row[11]
            #purposeTo = row[12]
            try:
                passengers = int(row[13]) # find the number of people in the car
            except:
                passengers = 1

            try:
                #tripStart = int(row[8])
                tripEnd = int(row[9])
                tripDistance = float(row[10])*1609.34 #convert from miles to m
            except:
                continue

            if vehicle not in energy:
                energy[vehicle] = 0
                distance[vehicle] = 0

            distance[vehicle] += tripDistance/1609.34

            if rTypes[row[1]] == '1':
                cycle = Drivecycle(tripDistance,'rural')
            elif rTypes[row[1]] == '2':
                cycle = Drivecycle(tripDistance,'urban')
            else:
                continue

            car.load = passengers*75 # add passengers
            energySpent = nissanLeaf.getEnergyExpenditure(cycle,0.0)
            energy[vehicle] += energySpent
            car.load = 0 # remove passengers
            
            if vehicle not in endTimes:
                endTimes[vehicle] = tripEnd
            else:
                if tripEnd > endTimes[vehicle]:
                    endTimes[vehicle] = tripEnd
#


startTimes = getStartTimes(nextday,month)


dailyMiles = [0]*200
dailyEnergy = [0]*60
good = 0
bad = 0

for vehicle in energy:
    dist = int(distance[vehicle])
    en = int(energy[vehicle])
    if en <= 24:
        good += 1
    else:
        bad += 1
    try:
        dailyMiles[dist] += 1
    except:
        print dist,
        print ' miles'

    try:
        dailyEnergy[en] += 1
    except:
        print en,
        print ' kWh'

print good,
print ' ok'
print bad,
print ' not ok'

dumbCharging = [0]*(48*60)
power = 3.5

n = 0
for vehicle in energy:
    try:
        kWh = energy[vehicle]
        plugIn = endTimes[vehicle]
    except:
        continue
    n += 1

    chargeTime = int(kWh*60/power)

    for i in range(plugIn,plugIn+chargeTime):
        try:
            dumbCharging[i] += power
        except:
            continue

scale = float(fleetSize)/n
for i in range(0,48*60):
    dumbCharging[i] = scale*dumbCharging[i]

plt.figure(1)
plt.bar(range(0,60),dailyEnergy)
plt.title('Histogram of Predicted Daily Energy Consumption')
plt.xlabel('Energy Consumption (kWh)')
plt.ylabel('# Vehicles')

plt.figure(2)
plt.bar(range(0,200),dailyMiles)
plt.title('Histogram of Daily Mileage')
plt.xlabel('Distance Driven (miles)')
plt.ylabel('# Vehicles')

t = np.linspace(0,48,num=60*48)
plt.figure(3)
plt.plot(t,dumbCharging)
plt.ylabel('Power (kW)')
plt.xlim(0,48)
plt.show()
