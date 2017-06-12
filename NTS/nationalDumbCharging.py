# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

accessoryLoad = {'1':1.5,'2':1.3,'3':0.8,'4':0.4,'5':0.1,'6':-0.2,'7':-0.2,
                 '8':-0.1,'9':-0.1,'10':0.2,'11':0.7,'12':1.3}
day = '3'
#month = '1'

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

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plotMonths = {'1':1,'4':2,'7':3,'10':4}
titles = {'1':'January','4':'April','7':'July','10':'October'}

nHours = 36
t = np.linspace(0,nHours,nHours*60)

x = np.linspace(8,32,num=5)
my_xticks = ['08:00 \n Wed','14:00','20:00','02:00','08:00 \n Thu']

pointsPerHour = 1

shortfalls = {}

for month in ['1','4','7','10']:
    run = NationalEnergyPrediction(day,month)
    dumbProfile = run.getNationalDumbChargingProfile(3.5,nHours) # GW
 #   shortfalls[month] = run.getNationalMissingCapacity()

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

        # baseLoad is in GW

    smartProfiles = run.getNationalOptimalChargingProfiles(72.0,baseLoad,
                                                           pointsPerHour=pointsPerHour)

    summed = [0.0]*36
    for vehicle in smartProfiles:
        for i in range(0,len(summed)):
            summed[i] += smartProfiles[vehicle][i]
    
    for i in range(0,len(baseLoad)):
        dumbProfile[i] += baseLoad[i]
        if i%60 == 0:
            summed[i/60] += baseLoad[i]

    plt.subplot(2,2,plotMonths[month])
    plt.plot(t,baseLoad,ls=':',c='g',label='Base Load')
    plt.plot(t,dumbProfile,label='Uncontrolled Charging')
    plt.plot(summed,ls='--',label='Controlled Charging',)
    if month == '1':
        plt.legend(loc=[-0.2,1.1],ncol=3)

    plt.grid()
        
    plt.xticks(x, my_xticks)
    plt.xlabel('time')
    plt.ylabel('Power Demand (GW)')
    plt.xlim(6,34)
    plt.ylim(20,85)
    plt.title(titles[month],y=0.8)

'''
plt.figure(2)
for month in ['1','4','7','10']:
    plt.subplot(2,2,plotMonths[month])
    plt.bar(range(0,len(shortfalls[month])),shortfalls[month])
    plt.xlabel('extra capacity required (kWh)')
    plt.ylabel('Thousands of vehicles')
    plt.title(titles[month],y=0.85)

'''
    
plt.show()
