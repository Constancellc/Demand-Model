# packages
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import copy
# my code
from vehicleModelCopy import Drivecycle, Vehicle

energyLogs = {}


accessoryLoad = {'1':1.5,'2':1.3,'3':0.8,'4':0.4,'5':0.1,'6':0.0,'7':0.0,
                 '8':0.0,'9':0.0,'10':0.2,'11':0.7,'12':1.3}

tesla = Vehicle(2273.0,37.37,0.1842,0.01508,0.94957,60.0)
tesla.load = 80.0

chargePower = [3.5,7.0]

uCycle = Drivecycle(10000,'urban')
mCycle = Drivecycle(10000,'motorway')

uEnergy = tesla.getEnergyExpenditure(uCycle,0.1)/10000
mEnergy = tesla.getEnergyExpenditure(mCycle,0.1)/10000

with open('../../Documents/JLRCompanyCars/trips_useful.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:

        userID = row[0]
        dayNo = int(row[1])
        
        startTime = int(row[4])+dayNo*24*60
        endTime = int(row[5])+dayNo*24*60
        if endTime < startTime:
            endTime += dayNo*24*60
            
        distance = int(row[6]) #m

        if row[-1] == '1':
            toHome = 1
        else:
            toHome = 0
            
        if row[-3] == '1':
            toWork = 1
        else:
            toWork = 0

        if userID not in energyLogs:
            energyLogs[userID] = []

        '''
        
        if distance > 5000:
            cycle = Drivecycle(distance,'motorway')
        else:
            cycle = Drivecycle(distance,'urban')

        energy = tesla.getEnergyExpenditure(cycle,accessoryLoad[row[3]])

        '''

        if distance > 5000:
            energy = distance*mEnergy
        else:
            energy = distance*uEnergy

        energyLogs[userID].append([startTime,endTime,energy,toHome,toWork])

#x_ticks = ['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35-40','40-45',
#           '45-50','50-55','55-60'

longestTrips = {}

per = 90

for userID in energyLogs:
    
    log = copy.copy(energyLogs[userID])
    
    # find number of journeys
    N = len(log)
    n = int(N*(100-per)/100) # 5% of journeys

    if n == 0:
        longestTrips[userID] = [[0.0,0.0]]
        continue

    longestTrips[userID] = [[0.0,0.0]]*n

    # now i need to find the longest N journeys:
    for trip in log:

        if trip[2] > longestTrips[userID][0][0]:
            longestTrips[userID][0] = [trip[2],trip[0]]

            longestTrips[userID] = sorted(longestTrips[userID])

   
    

maxCap = 200
capStep = 20

x = np.arange(capStep/2,maxCap+capStep/2,capStep)
x_ticks = []

for i in range(0,len(x)):
    x_ticks.append(str(int(x[i]-capStep/2))+'-'+str(int(x[i]+capStep/2)))

x_ticks[-1] = str(maxCap)+'+'
    
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.suptitle('Required capacity of vehicles in order to carry out',y=1)


plotNumbers = {'home':[1,2],'work':[3,4],'both':[5,6]}


for p in [0,1]:
    for chargeLoc in ['home','work','both']:
        plt.subplot(3,2,plotNumbers[chargeLoc][p])

        batterySize = [[0]*int(maxCap/capStep),[0]*int(maxCap/capStep)]
        # now I need to size the required battery for each vehicle
        for userID in energyLogs:
            
            log = sorted(energyLogs[userID])
            

            for j in range(0,len(chargePower)):

                requiredCap = 0.0
                energySpent = 0.0
                
                for i in range(0,len(log)):

                    if p == 1:
                        if [log[i][2],log[i][0]] in longestTrips[userID]:
                            continue

                    energySpent += log[i][2]
                    if energySpent > requiredCap:
                        requiredCap = energySpent
                        

                    if chargeLoc == 'home':
                        if log[i][3] != 1 or i == len(log)-1:
                            continue
                    elif chargeLoc == 'work':
                        if log[i][4] != 1 or i == len(log)-1:
                            continue
                    else:
                        if (log[i][3] != 1 and log[i][4] != 1) or i == len(log)-1:
                            continue

                    timeAvaliable = log[i+1][0]-log[i][1]
                    maxPower = float(timeAvaliable)*chargePower[j]/60

                    if maxPower > energySpent:
                        energySpent = 0.0
                    else:
                        energySpent -= maxPower

                try:
                    batterySize[j][int(requiredCap/capStep)] += 1
                except:
                    batterySize[j][-1] += 1


        plt.bar(np.arange(0,maxCap,capStep)+0.275*capStep,batterySize[0],
                width=0.45*capStep,label=str(chargePower[0])+'kW')
        plt.bar(np.arange(0,maxCap,capStep)+0.725*capStep,batterySize[1],
                width=0.45*capStep,label=str(chargePower[1])+'kW')

        plt.xticks(x,x_ticks,rotation=70)
        plt.ylabel('number of vehicles')
        plt.xlabel('battery capacity (kWh)')
        if p == 0:
            plt.title('100% of journeys\ncharging at '+chargeLoc,y=0.7)
        elif p == 1:
            plt.title(str(per)+'% of journeys\ncharging at '+chargeLoc,y=0.7)
        plt.ylim(0,400)
        plt.xlim(0,maxCap)

        if chargeLoc == 'home' and p == 0:
            plt.legend(ncol=2,loc=[1.7,1.1])
    
plt.show()

        
    
