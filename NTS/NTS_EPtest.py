# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

day = '3'
month = '1'

# find right date for day of the week
calender = {'1':{'1':11,'2':12,'3':13,'4':14,'5':15,'6':16,'7':17},
            '2':{'1':15,'2':16,'3':17,'4':18,'5':19,'6':20,'7':21},
            '3':{'1':14,'2':15,'3':16,'4':17,'5':18,'6':19,'7':20},
            '4':{'1':11,'2':12,'3':13,'4':14,'5':15,'6':16,'7':17},
            '5':{'1':16,'2':17,'3':18,'4':19,'5':20,'6':21,'7':22},
            '6':{'1':13,'2':14,'3':15,'4':16,'5':17,'6':18,'7':19},
            '7':{'1':11,'2':12,'3':13,'4':14,'5':15,'6':16,'7':17},
            '8':{'1':15,'2':16,'3':17,'4':18,'5':19,'6':20,'7':21},
            '9':{'1':12,'2':13,'3':14,'4':15,'5':16,'6':17,'7':18},
            '10':{'1':17,'2':18,'3':19,'4':20,'5':21,'6':22,'7':23},
            '11':{'1':14,'2':15,'3':16,'4':17,'5':18,'6':19,'7':20},
            '12':{'1':12,'2':13,'3':14,'4':15,'5':16,'6':17,'7':18}}

months = {'1':'-Jan-16','2':'-Feb-16','3':'-Mar-16','4':'-Apr-16','5':'-May-16',
          '6':'-Jun-16','7':'-Jul-16','8':'-Aug-16','9':'-Sep-16',
          '10':'-Oct-16','11':'-Nov-16','12':'-Dec-16'}

nextDay = {'1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'1'}

nHours = 36
# getting the baseLoad to compare against
dayOne = []
dayTwo = []

with open('../ng-data/Demand_Data2016.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == str(calender[month][day])+months[month]:
            dayOne.append(float(row[4]))
        elif row[0] == str(calender[month][nextDay[day]])+months[month]:
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

run = EnergyPrediction(day,month,region='1')

profiles = run.getPsuedoOptimalProfile(4,baseLoad,returnIndividual=True)

vehicles = []

for vehicle in profiles[1]:
    vehicles.append(vehicle)

run2 = EnergyPrediction(day,month,region='1')

profiles2 = run.getDumbChargingProfile(3.5,36*60,individuals=vehicles)

plt.figure(1)
n = 1
for vehicle in vehicles:
    plt.subplot(2,2,n)
    plt.plot(profiles2[1][vehicle])
    smart = [0.0]*36*60

    chargeStart = int(profiles[1][vehicle][1])

    for i in range(0,len(profiles[1][vehicle][0])):
        try:
            smart[chargeStart+i] += profiles[1][vehicle][0][i]
        except:
            continue
        
    plt.plot(smart)
    n += 1

plt.show()

