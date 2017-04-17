# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction

day = '3'
month = '1'

nissanLeaf = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)

uc = EnergyPrediction(day,month,nissanLeaf,regionType='1')
ut = EnergyPrediction(day,month,nissanLeaf,regionType='2')
rt = EnergyPrediction(day,month,nissanLeaf,regionType='3')
rv = EnergyPrediction(day,month,nissanLeaf,regionType='4')

ucScale = float(23650000)/uc.nPeople
utScale = float(28590000)/ut.nPeople
rtScale = float(5900000)/rt.nPeople
rvScale = float(5960000)/rv.nPeople

urban = EnergyPrediction(day,month,nissanLeaf,regionType='1')
urbanScale = float(10300000)/urban.nPeople

ucScale = ucScale/1000000 # kW -> GW
utScale = utScale/1000000 # kW -> GW
rtScale = rtScale/1000000 # kW -> GW
rvScale = rvScale/1000000 # kW -> GW

ucProfile = uc.getDumbChargingProfile(3.5,48*60,scaleFactor=ucScale)
utProfile = ut.getDumbChargingProfile(3.5,48*60,scaleFactor=utScale)
rtProfile = rt.getDumbChargingProfile(3.5,48*60,scaleFactor=rtScale)
rvProfile = rv.getDumbChargingProfile(3.5,48*60,scaleFactor=rvScale)


# getting the baseLoad to compare against
dayOne = []
dayTwo = []

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

with open('../ng-data/Demand_Data2016.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == str(calender[month][day])+months[month]:
            dayOne.append(float(row[4]))
        elif row[0] == str(calender[month][nextDay[day]])+months[month]:
            dayTwo.append(float(row[4]))

halfHourly = dayOne+dayTwo
baseLoad = [0.0]*48*60
forwardFill = [0]*(48*60)

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

totalProfile = []

for i in range(0,48*60):
    totalProfile.append(ucProfile[i]+utProfile[i]+rtProfile[i]+rvProfile[i]+
                        baseLoad[i])

plt.figure(1)
plt.grid()
x = np.linspace(4,36,num=9)
my_xticks = ['04:00 \n Wed','08:00','12:00','16:00','20:00','0:00',
             '04:00 \n Thu','08:00','12:00']
plt.xticks(x, my_xticks)
plt.xlabel('time')
plt.ylabel('power demand (GW)')
plt.xlim(0,32)


t = np.linspace(0,48,48*60)
plt.plot(t,totalProfile,label='Dumb Charging')
plt.plot(t,baseLoad,label='Base Load')
plt.legend()

plt.show()
