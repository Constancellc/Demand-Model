# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

nHours = 36
pointsPerHour = 10

run = EnergyPrediction('3','2')
dumb = run.getDumbChargingProfile(3.5,nHours*60)
baseLoad = []

for i in range(0,pointsPerHour*nHours):
    baseLoad.append(random.random()*6000)
    
smartProfiles = run.getOptimalChargingProfiles(7.0,baseLoad,
                                               pointsPerHour=pointsPerHour)

smart = [0.0]*nHours*pointsPerHour
for vehicle in smartProfiles:
    for i in range(0,nHours*pointsPerHour):
        smart[i] += smartProfiles[vehicle][i]


plt.figure(1)
plt.plot(dumb)
plt.plot(range(0,36*60,60/pointsPerHour),smart)
plt.plot(range(0,36*60,60/pointsPerHour),baseLoad)
'''
run = NationalEnergyPrediction('3','2')
dumbProfile = run.getNationalDumbChargingProfile(3.5,nHours)

# getting the baseLoad to compare against
dayOne = []
dayTwo = []

with open('../ng-data/Demand_Data2016.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == '17-Feb-16':
            dayOne.append(float(row[4]))
        elif row[0] == '18-Feb-16':
            dayTwo.append(float(row[4]))

halfHourly = dayOne+dayTwo[:(nHours-24)*2]

baseLoad = [0.0]*nHours*60

for i in range(0,len(baseLoad)):
    p1 = int(i/30)
    if p1 == len(halfHourly)-1:
        p2 = p1
    else:
        p2 = p1+1

    f2 = float(i)/30 - p1
    f1 = 1.0-f2

    baseLoad[i] = f1*float(halfHourly[p1])+f2*float(halfHourly[p2])
    baseLoad[i] = float(int(baseLoad[i]))/1000 # MW -> rounded GW

    # baseLoad is in GW

for i in range(0,len(baseLoad)):
    dumbProfile[i] += baseLoad[i]

t = np.linspace(0,36,num=36*60)

plt.figure(1)
plt.plot(t,dumbProfile)
plt.plot(t,baseLoad)
plt.xlim(8,32)
'''
plt.show()
