# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
from cvxopt import matrix, spdiag, solvers, sparse
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSvehicleLocation import LocationPrediction


# CONTENTS:
# classes: BaseLoad, EnergyPrediction, NationalEnergyPrediction,
#          AreaEnergyPrediction

# these are the csv files containing the data
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

class BaseLoad:

    def __init__(self,day,month,nHours,unit='G',pointsPerHour=60):

        units = {'':1,'k':1000,'M':1000000,'G':1000000000}

        nDays = int(nHours/24)+1

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

        months = {'1':'-Jan-2016','2':'-Feb-2016','3':'-Mar-2016',
                  '4':'-Apr-2016','5':'-May-2016','6':'-Jun-2016',
                  '7':'-Jul-2016','8':'-Aug-2016','9':'-Sep-2016',
                  '10':'-Oct-2016','11':'-Nov-2016','12':'-Dec-2016'}

        nextDay = {'1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'1'}

        dates = {}
        n = 0

        profiles = []
        for i in range(0,nDays):
            profiles.append([])

        while nDays > 0:
            dates[str(calender[month][day])+months[month]] = n
            n += 1
            day = nextDay[day]
            nDays -= 1


        with open('../../Documents/DemandData_2011-2016.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] not in dates:
                    continue

                profiles[dates[row[0]]].append(float(row[4]))

                                                

        profile = []

        for i in range(0,len(profiles)):
            profile += profiles[i]

        profile = profile[:nHours*2] # half-hourly


        interpolatedLoad = [0.0]*nHours*pointsPerHour

        for i in range(0,len(interpolatedLoad)):
            p1 = int(2*i/pointsPerHour)
            if p1 == len(profile)-1:
                p2 = p1
            else:
                p2 = p1+1

            f2 = 2*float(i)/pointsPerHour - p1
            f1 = 1.0-f2

            interpolatedLoad[i] = f1*float(profile[p1])+\
                                  f2*float(profile[p2])

            # Change the units to the specified ones
            interpolatedLoad[i] = interpolatedLoad[i]*float(1000000)/units[unit]
            
            # round to 3dp
            interpolatedLoad[i] = float(int(1000000*interpolatedLoad[i]))/1000000

        self.baseLoad = interpolatedLoad

    def getLoad(self,population='full'):

        if population == 'full':
            return self.baseLoad

        else:
            scale = float(population)/65140000
            base = copy.copy(self.baseLoad)
            for i in range(0,len(base)):
                # scale then round
                base[i] = base[i]*scale
                base[i] = float(int(1000000*base[i]))/1000000

            return base

        
class EnergyPrediction:

    def __init__(self, day, month=None, car=None, regionType=None, region=None,
                 model='full',penetration=1.0,smoothTimes=False):
        # day: string of integer 1-7 symbolising day of week
        # month: string of integer 1-12 symbolising month
        # car: vehicle object
        # regionType (opt): string filtering for a specific region type
        # region (opt): string filtering for a specific region

        if car == None:
            nissanLeaf = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)
            car = nissanLeaf
        elif car == 'tesla':
            car = Vehicle(2273.0,37.37,0.1842,0.01508,0.94957,60.0)
        elif car == 'bmw':
            car = Vehicle(1420.0,22.9,0.346,0.01626,0.87785,22.0)
            
        self.day = day
        self.month = month
        self.car = car
        self.regionType = regionType
        self.region = region
        self.chargingEfficiency = 0.95
        self.penetration = penetration
        self.smoothTimes = smoothTimes
        

        # first getting the region types
        
        self.reg1 = {} # 1:urban, 2:rural, 3:scotland

        if regionType is not None:
            self.reg2 = {} # 1:uc, 2:ut, 3:rt, 4:rv, 5:scotland

        if region is not None:
            self.reg3 = {} # 1:NE, 2:NW, 3:Y+H, 4:EM, 5:WM, 6:E, 7:L, 8:SE, 9:SW,
                      # 10: Wales, 11: Scotland
                      
        # setting up counters which will be used to scale predictions
        self.nVehicles = 0 
        self.nHouseholds = 0
        self.nPeople = 0

        with open(households,'rU') as csvfile:
            reader = csv.reader(csvfile,delimiter='\t')
            next(reader)
            for row in reader:

                if month is not None:
                    if row[9] != month: # skip households from the wrong month
                        continue
                
                if row[0] not in self.reg1:

                    self.reg1[row[0]] = row[148]

                    if regionType is not None:
                        self.reg2[row[0]] = row[149]

                        if region is None:
                            if row[149] == regionType:
                                self.nHouseholds += 1
                                self.nPeople += int(row[32])
                        else:
                            self.reg3[row[0]] = row[28]
                            if row[149] == regionType and row[28] == region:
                                self.nHouseholds += 1
                                self.nPeople += int(row[32])

                    elif region is not None:
                        self.reg3[row[0]] = row[28]
                        if row[28] == region:
                            self.nHouseholds += 1
                            self.nPeople += int(row[32])

                    else:
                        if row[148] == '1' or row[148] == '2':
                            # (if this isn't true the trip will be skipped later
                            #  so these households shouldn't be counted)
                            self.nHouseholds += 1
                            self.nPeople += int(row[32])
        
        # now getting the trip data and running it through the vehicle model

        self.distance = {} # miles
        self.energy = {} # kWh
        self.endTimes = {} # mins past 00:00 of last journey end

        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                
                if month is not None:
                    if row[6] != self.month:
                        continue

                if self.regionType is not None:
                    if self.reg2[row[1]] != self.regionType:
                        continue

                if self.region is not None:
                    if self.reg3[row[1]] != self.region:
                        continue

                vehicle = row[2]

                if vehicle == ' ': # skip trips where the vehicle is missing
                    continue

                if vehicle not in self.energy:
                    self.energy[vehicle] = 0.0
                    self.distance[vehicle] = 0.0
                    self.endTimes[vehicle] = 0
                    self.nVehicles += 1

                # leaving day skip until after initialisation of variables allows
                # unused vehicles to be considered
                if row[5] != self.day:
                    continue
                    
                try:
                    passengers = int(row[13]) # find the # people in the car
                except:
                    passengers = 1 # if missing assume only the driver

                try:
                    tripEnd = int(row[9])
                    tripDistance = float(row[10])*1609.34 # miles -> m
                except:
                    continue # skip trips without a time or length

                if smoothTimes == True:
                    tripEnd = int(30*int(tripEnd/30)+30*random.random())
                
                self.distance[vehicle] += int(tripDistance) # m

                if tripEnd > self.endTimes[vehicle]:
                    self.endTimes[vehicle] = tripEnd

                if model == 'full':
                    # if the trip is really long, run the motorway artemis
                    if tripDistance > 30000:
                        cycle = Drivecycle(tripDistance,'motorway')

                    # otherwise run the rural/urban depending on the location
                    elif self.reg1[row[1]] == '1':
                        cycle = Drivecycle(tripDistance,'rural')
                    elif self.reg1[row[1]] == '2':
                        cycle = Drivecycle(tripDistance,'urban')
                    else:
                        # not really sure what to do here..?
                        #continue
                        cycle = Drivecycle(tripDistance,'urban')
                    accessoryLoad = {'1':1.5,'2':1.3,'3':0.8,'4':0.4,'5':0.1,
                                     '6':0.0,'7':0.0,'8':0.0,'9':0.0,'10':0.2,
                                     '11':0.7,'12':1.3}

                    car.load = passengers*75 # add appropriate load to vehicle
                    self.energy[vehicle] += car.getEnergyExpenditure(cycle,
                                                                     accessoryLoad[row[6]])
                    car.load = 0
                    
                elif model == 'linear':
                    self.energy[vehicle] += tripDistance*0.23/1609.34
                


    def getNextDayStartTimes(self):
        # Finds the number of minutes past 00:00 the next day when each
        # vehicle is first required

        self.startTimes = {}

        for vehicle in self.endTimes:
            self.startTimes[vehicle] = 24*60

        nextDay = {'1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'1'}

        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row[5] != nextDay[self.day]:
                    continue
                if row[6] != self.month:
                    continue

                if self.regionType is not None:
                    if self.reg2[row[1]] != self.regionType:
                        continue

                if self.region is not None:
                    if self.reg3[row[1]] != self.region:
                        continue

                vehicle = row[2]

                if vehicle == ' ': # skip trips where the vehicle is missing
                    continue

                try:
                    tripStart = int(row[8])
                except:
                    continue

                if self.smoothTimes == True:
                    tripStart = int(30*int(tripStart/30)+30*random.random())

                if vehicle not in self.startTimes:
                    self.startTimes[vehicle] = tripStart
                else:
                    if tripStart < self.startTimes[vehicle]:
                        self.startTimes[vehicle] = tripStart

    def getCommuters(self):

        self.commutes = {}

        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row[5] != self.day:
                    continue
                if row[6] != self.month:
                    continue

                if self.regionType is not None:
                    if self.reg2[row[1]] != self.regionType:
                        continue

                if self.region is not None:
                    if self.reg3[row[1]] != self.region:
                        continue

                vehicle = row[2]

                if vehicle == ' ': # skip trips where the vehicle is missing
                    continue

                try:
                    purposeTo = int(row[12])
                    purposeFrom = int(row[11])
                    start = int(row[8])
                    end = int(row[9])
                except:
                    continue

                if purposeTo != 1 and purposeFrom != 1:
                    continue
                
                if vehicle not in self.commutes:
                    self.commutes[vehicle] = [-1,-1]
                    
                if purposeTo == 1:
                    self.commutes[vehicle][0] = end
                elif purposeFrom == 1:
                    self.commutes[vehicle][1] = start

        # now go through and remove duds
        toDelete = []

        for vehicle in self.commutes:
            if self.commutes[vehicle][0] == -1 or self.commutes[vehicle][1] == -1:
                toDelete.append(vehicle)

            elif self.commutes[vehicle][0] >= self.commutes[vehicle][1]:
                toDelete.append(vehicle)

        for vehicle in toDelete:
            del self.commutes[vehicle]

    def plotMileage(self,figNo=1,wait=False):
        # figNo (int): the figure number
        # wait (statement): when true the plot is not shown immediately
        
        dailyMiles = [0]*200

        for vehicle in self.distance:
            miles = int(float(self.distance[vehicle])/1609.34)

            try:
                dailyMiles[miles] += 1
            except:
                continue

        plt.figure(figNo)
        plt.bar(range(0,200),dailyMiles)
        plt.xlabel('distance (miles)')
        plt.ylabel('# vehicles')
        plt.title('Histogram of vehicle mileage')

        if wait == False:
            plt.show()

    def plotEnergyConsumption(self,newFigure=True,figNo=1,wait=False,label=None,
                              normalise=False,offset=0,width=0.9,
                              returnResults=False):
        dailyEnergy = [0]*101
        over100 = 0

        for vehicle in self.energy:
            if self.energy[vehicle] == 0:
                dailyEnergy[0] += 1
            else:
                kWh = int(self.energy[vehicle])

                try:
                    dailyEnergy[kWh+1] += 1
                except:
                    over100 += 1
                    continue

        if normalise == True:
            total = sum(dailyEnergy)
            for i in range(0,len(dailyEnergy)):
                dailyEnergy[i] = float(dailyEnergy[i])/total

        if newFigure == True:
            plt.figure(figNo)
            plt.xlabel('energy consumption (kWh)')
            plt.ylabel('# vehicles')
            plt.title('Histogram of vehicle predicted energy consumption')
            
        #plt.bar(np.arange(offset,101+offset,1),dailyEnergy,width=width,label=label)
    

        if wait == False:
            plt.show()
        if returnResults == True:
            dailyEnergy += [over100]
            return dailyEnergy

    def findOverCapacityVehicles(self):
        self.overCapacityVehicles = []
        for vehicle in self.energy:
            if self.energy[vehicle] > self.car.capacity:
                self.overCapacityVehicles.append(vehicle)

    def getOverCapacityTravelDiaries(self):

        try:
            vehicles = self.overCapacityVehicles
        except:
            raise Exception('please run findOverCapacityVehicles first')

        self.overCapacityTravelDiaries = {}

        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                
                if row[5] != self.day:
                    continue

                if self.month is not None:
                    if row[6] != self.month:
                        continue

                if self.regionType is not None:
                    if self.reg2[row[1]] != self.regionType:
                        continue

                if self.region is not None:
                    if self.reg3[row[1]] != self.region:
                        continue

                if row[2] not in vehicles:
                    continue

                try:
                    tripEnd = int(row[9])
                    tripStart = int(row[8])
                    tripDistance = int(float(row[10])*1609.34) # miles -> m
                except:
                    continue # skip trips without a time or length

                                # if the trip is really long, run the motorway artemis
                if tripDistance > 30000:
                    cycle = Drivecycle(tripDistance,'motorway')

                # otherwise run the rural/urban depending on the location
                elif self.reg1[row[1]] == '1':
                    cycle = Drivecycle(tripDistance,'rural')
                elif self.reg1[row[1]] == '2':
                    cycle = Drivecycle(tripDistance,'urban')
                else:
                    continue

                try:
                    passengers = int(row[13]) # find the # people in the car
                except:
                    passengers = 1 # if missing assume only the driver
                accessoryLoad = {'1':1.5,'2':1.3,'3':0.8,'4':0.4,'5':0.1,
                                 '6':0.0,'7':0.0,'8':0.0,'9':0.0,'10':0.2,
                                 '11':0.7,'12':1.3,None:0.6}

                self.car.load = passengers*75 # add appropriate load to vehicle
                energy = self.car.getEnergyExpenditure(cycle,
                                                       accessoryLoad[self.month])
                self.car.load = 0

                if row[12] == '23':
                    location = 1 # home
                elif row[12] == '1':
                    location = 2 # work
                elif row[12] == '4' or row[12] == '5':
                    location = 3 # shopping
                else:
                    location = 0

                if row[2] not in self.overCapacityTravelDiaries:
                    self.overCapacityTravelDiaries[row[2]] = []

                self.overCapacityTravelDiaries[row[2]].append([tripEnd,energy,
                                                                location,tripStart])
        # sort the travel diaries chronologically
        
        newLogs = {}
        for vehicle in self.overCapacityTravelDiaries:
            oldLog = self.overCapacityTravelDiaries[vehicle]
            newLog = []
            
            while len(oldLog) > 0:
                earliest = oldLog[0]
                for j in range(1,len(oldLog)):
                    if oldLog[j][0] < earliest[0]:
                        earliest = oldLog[j]

                newLog.append(earliest)
                oldLog.remove(earliest)

            newLogs[vehicle] = newLog

        self.overCapacityTravelDiaries = newLogs
              
                
    def getDumbChargingProfile(self,power,tmax,scaleFactor=1,logOutofCharge=True,
                               highUseHomeCharging=True,highUseWorkCharging=True,
                               highUseShopCharging=True, scalePerHousehold=False,
                               scalePerVehicle=False,scalePerPerson=False,
                               superCharge=False,individuals=[]):
        # power: the charging power in kW
        
        # tmax: the no. minutes past 00:00 the simulation is run for

        uncharged = 0
        self.nOutOfCharge = 0
        self.dumbScaleFactor = scaleFactor

        individualProfiles = {}

        if logOutofCharge == True:
            self.outOfChargeLog = {}

        if tmax < 24*60:
            print('please choose a simulation length greater than a day')
            tmax = 24*60

        profile = [0.0]*tmax

        if highUseHomeCharging == True or highUseWorkCharging == True or highUseShopCharging == True:
            self.findOverCapacityVehicles()

        for vehicle in self.energy:

            if highUseHomeCharging == True:
                if vehicle in self.overCapacityVehicles:
                    continue
            
            kWh = self.energy[vehicle]

            if highUseHomeCharging == False and highUseWorkCharging == False and highUseShopCharging == False:
                if kWh > self.car.capacity:
                    self.nOutOfCharge += 1

                    if logOutofCharge == True:
                        if vehicle not in self.outOfChargeLog:
                            self.outOfChargeLog[vehicle] = []

                        self.outOfChargeLog[vehicle].append([kWh-24,vehicle])
                    kWh = self.car.capacity

            chargeStart = self.endTimes[vehicle]
            chargeTime = int(kWh*60/power)

            if vehicle in individuals:
                iSOC = 1.0-(float(kWh)/self.car.capacity)
                print(iSOC)
                if iSOC < 0:
                    iSOC = 0

                prof = [0]*tmax

                if iSOC >= 0.8:
                    constPowerTime = 0
                else:
                    constPowerTime = int(self.car.capacity*(0.8-iSOC)*60/power)
                print(constPowerTime)
                for i in range(chargeStart,chargeStart+constPowerTime):
                    try:
                        prof[i] = power
                    except:
                        continue

                # then get the time constant
                a = float(power)/(0.2*24*60)
                t_lim = int(tmax-(chargeStart+constPowerTime))

                t = 0                
                p_t = float(power)*(np.exp(-a*t))

                while p_t > 0.1 and t < t_lim:
                    prof[t+chargeStart+constPowerTime] = p_t
                    t = int(t+1)                
                    p_t = float(power)*(np.exp(-a*t))

                individualProfiles[vehicle] = prof
                

            chargeEnd = chargeStart+chargeTime

            if chargeEnd >= tmax:
                chargeEnd = tmax-1
                uncharged += 1

            for i in range(chargeStart,chargeEnd):
                profile[i] += scaleFactor*power*self.penetration

        # now for the high acheivers:
        if highUseHomeCharging == True:

                
            chargingLocations = [1]

            if highUseWorkCharging == True:
                chargingLocations.append(2)
            if highUseShopCharging == True:
                chargingLocations.append(3)
                
            self.getOverCapacityTravelDiaries()
                                        
            for vehicle in self.overCapacityTravelDiaries: #Vehicles:
                outOfCharge = False
                
                journeys = self.overCapacityTravelDiaries[vehicle]

                energyRequired = 0.0

                while len(journeys) > 1:
                    energyRequired += journeys[0][1]

                    if energyRequired > self.car.capacity:
                        outofCharge = True

                        if logOutofCharge == True:

                            if vehicle not in self.outOfChargeLog:
                                self.outOfChargeLog[vehicle] = []

                            self.outOfChargeLog[vehicle].append([energyRequired-self.car.capacity,
                                                            journeys[0][0]])

                    if journeys[0][2] in chargingLocations:
                        # car gone home
                        if journeys[0][2] == '3':
                            chargePower = power # room for fast charging
                        else:
                            chargePower = power
                            
                        chargeStart = journeys[0][0]                        
                        timeRequired = int(energyRequired*60/chargePower) # mins
                        departure = journeys[1][3]

                        if chargeStart+timeRequired < departure:
                            chargeEnd = chargeStart+timeRequired

                        else:
                            chargeEnd = departure

                        energyRequired -= chargePower*(chargeEnd-chargeStart)/60

                        for i in range(chargeStart,chargeEnd):
                            profile[i] += scaleFactor*chargePower*self.penetration

                    journeys.remove(journeys[0])

                # now it's end of the day and all possible day charging has occured
                energyRequired += journeys[0][1]

                if energyRequired > self.car.capacity:
                    outOfCharge = True

                    if logOutofCharge == True:
                        
                        if vehicle not in self.outOfChargeLog:
                            self.outOfChargeLog[vehicle] = []
                            
                        self.outOfChargeLog[vehicle].append([energyRequired-self.car.capacity,
                                                            journeys[0][0]])
                    energyRequired = self.car.capacity

                chargeStart = journeys[0][0]
                timeRequired = int(energyRequired*60/power) # mins
                
                for i in range(chargeStart,chargeStart+timeRequired):
                    if i >= len(profile):
                        continue
                    profile[i] += scaleFactor*power*self.penetration
                                            

                if outOfCharge is True:
                    self.nOutOfCharge += 1
                    
            if superCharge == True:
                scPower = 72 # kW
                for vehicle in self.outOfChargeLog:
                    for log in self.outOfChargeLog[vehicle]:
                        timeReq = int(log[0]*60/scPower)
                        for i in range(log[1],log[1]+timeReq):
                            try:
                                profile[i] += scaleFactor*scPower*self.penetration
                            except:
                                continue

        # acale for charging efficiency
        for i in range(0,tmax):
            profile[i] = profile[i]/self.chargingEfficiency
            
        if scalePerHousehold == True:
            for i in range(0,tmax):
                profile[i] = profile[i]/self.nHouseholds
                
        elif scalePerVehicle == True:
            for i in range(0,tmax):
                profile[i] = profile[i]/self.nVehicles

        elif scalePerPerson == True:
            for i in range(0,tmax):
                profile[i] = profile[i]/self.nPeople

        print(self.nOutOfCharge,end='')
        print(' out of ',end='')
        print(self.nVehicles,end='')
        print(' vehicles ran out of charge')

        if individuals != []:
            return profile, individualProfiles
        else:
            return profile

    def returnDumbChargingProfiles(self,nProfiles,power,nHours=24):

        profiles = []

        for vehicle in self.energy:

            if random.random() >= 10*nProfiles/len(self.energy):
                continue

            if len(profiles) >= nProfiles:
                continue

            profiles.append([0.0]*60*nHours)
            
            kWh = self.energy[vehicle]

            if kWh > self.car.capacity:
                kWh = self.car.capacity

            chargeStart = self.endTimes[vehicle]
            chargeTime = int(kWh*60/power)

            for i in range(chargeStart,chargeStart+chargeTime):
                if i < len(profiles[-1]):
                    profiles[-1][i] = power
                else:
                    profiles[-1][i-nHours*60] = power

        return profiles

    def returnNextDayStartTimes(self,nTimes):

        times = []

        self.getNextDayStartTimes()
        for vehicle in self.startTimes:

            if random.random() >= 10*nTimes/len(self.energy):
                continue

            if len(times) >= nTimes:
                continue

            times.append(self.startTimes[vehicle])

        return times


    def getMissingCapacity(self,nHours):
        try:
            log = self.outOfChargeLog
        except:
            raise Exception('you need to run dumb charging with logOutOfCharge = True before running this function')

        extraRequirements = [0.0]*100
        
        for vehicle in log:
            extraCapacity = 0
            for entry in log[vehicle]:
                if entry[0] > extraCapacity:
                    extraCapacity = entry[0]

            try:
                extraRequirements[int(extraCapacity)] += self.dumbScaleFactor
            except:
                 print(vehicle,end='')
                 print(extraCapacity)
                 
        return extraRequirements

    
    def getPsuedoOptimalProfile(self,pMax,baseLoad,nHours=36,scaleFactor=1,
                                returnIndividual=False,weighted=True,
                                allowOverCap=True,deadline=9):

        pointsPerHour = len(baseLoad)/nHours

        if weighted == True:
            loc = LocationPrediction(self.day,month=self.month,
                                         regionType=self.regionType,
                                         region=self.region)

            pHome = loc.getPFinished(nHours,pointsPerHour,deadline=deadline)

            weightings = [1.0]*len(pHome)

            for i in range(0,len(pHome)):
                weightings[i] = weightings[i]/pHome[i]

        if returnIndividual == True:
            individualProfiles = {}

        profile = [0.0]*len(baseLoad)

        # first calculate the target charging shape.
        target = [0.0]*len(baseLoad)
        lim = max(baseLoad)*1.0001
        
        # This is the unweighted version
        for i in range(0,len(baseLoad)):
            target[i] = lim-baseLoad[i]

        if weighted == True:
            # now apply the weightings
            for i in range(0,len(baseLoad)):
                target[i] = target[i]*weightings[i]

            
        self.getNextDayStartTimes()

        pMax = pMax*scaleFactor
        
        for vehicle in self.energy:
            if allowOverCap == False and self.energy[vehicle] > self.car.capacity:
                kWh = self.car.capacity*scaleFactor/self.chargingEfficiency
            else:
                kWh = self.energy[vehicle]*scaleFactor/self.chargingEfficiency
            chargeStart = int(self.endTimes[vehicle])
            chargeEnd = int(self.startTimes[vehicle]+24*pointsPerHour)

            if chargeEnd >= (24+deadline)*pointsPerHour:
                chargeEnd = int((24+deadline)*pointsPerHour-1)

            chargeProfile = copy.copy(target)
            
            try:
                chargeProfile = chargeProfile[chargeStart:chargeEnd]
            except:
                print(chargeStart)
                print(chargeEnd)
                continue

            try:
                energySF = kWh/(sum(chargeProfile)/pointsPerHour)
            except:
                print(chargeStart)
                print(chargeEnd)
                print(kWh)
                continue

            for i in range(0,len(chargeProfile)):
                chargeProfile[i] = chargeProfile[i]*energySF
                if chargeProfile[i] > pMax:
                    chargeProfile[i] = pMax

            if returnIndividual == True:
                if len(individualProfiles) < 4 and kWh > 0:
                    individualProfiles[vehicle] = [copy.copy(chargeProfile),
                                                   chargeStart]

            for i in range(chargeStart,chargeEnd):
                profile[i] += chargeProfile[i-chargeStart]*self.penetration

            del chargeProfile

        if returnIndividual == True:
            return profile, individualProfiles

        else:
            return profile

        
    def getOptimalChargingProfiles(self,pMax,baseLoad,baseScale=1,nHours=36,
                                   pointsPerHour=1,individuals=[],
                                   sampleScale=True,allowOverCap=True,
                                   deadline=None,perturbDeadline=False,
                                   chargeAtWork=False):
        # pMax is the maximum charging power allowed in kW
        
        # baseLoad is the non-ev demand that we're trying to valley fill
        
        # baseScale is the ratio of the population creating the baseLoad to
        #   the population creating the charging demand
        
        # nHours is the length in hours of the simulation
        
        # pointsPerHour is the number of charge bins per hour - ie. the number
        #   of different values a vehicles charge rate can take within an hour

        profiles = {}

        vehicles = []
        b = []

        unused = []

        # pick probability to cut down with:
        p_sample = float(150)/len(self.energy)

        # I'm going to need to downsample
        for vehicle in self.energy:
            if random.random() < p_sample or vehicle in individuals:
                
                
                if self.energy[vehicle] == 0.0:
                    unused += [vehicle]
                    continue
                if self.energy[vehicle] >= self.car.capacity:
                    print(self.energy[vehicle],end='')
                    print(' is higher than battery capacity')
                    if allowOverCap == True:
                        b.append(baseScale*self.energy[vehicle]/self.chargingEfficiency)
                    else:
                        b.append(baseScale*self.car.capacity/self.chargingEfficiency)
                else:
                    b.append(baseScale*self.energy[vehicle]/self.chargingEfficiency)

                vehicles.append(vehicle)               

        self.getNextDayStartTimes()

        if chargeAtWork == True:
            self.getCommuters()

        #n = self.nVehicles
        n = len(vehicles)
        
        if sampleScale == True:
            scale = float(self.nVehicles)*self.penetration/(len(unused)+len(vehicles)) # This accounts for downsampling
        else:
            scale = self.penetration
        pMax = pMax*scale*baseScale#added this
        
        for i in range(0,len(b)):
            b[i] = b[i]*scale#*0.000001
            
        t = nHours*pointsPerHour

        if len(baseLoad) > t:
            f = len(baseLoad)/t
            newBaseLoad = []
            
            for i in range(0,t):
                newBaseLoad.append(baseLoad[int(i*f)])
            baseLoad = newBaseLoad
            
        elif len(baseLoad) < t:
            raise Exception('i dont think you want this')

        A1 = matrix(0.0,(n,t*n)) # ensures right amount of energy provided
        A2 = matrix(0.0,(n,t*n)) # ensures vehicle only charges when avaliable

        b += [0.0]*n
        b = matrix(b)

        for j in range(0,n):
            arrival = int(float(self.endTimes[vehicles[j]])*pointsPerHour/60)
            departure = int(float(self.startTimes[vehicles[j]])*pointsPerHour/60)
            departure += 24*pointsPerHour

            if chargeAtWork == True:
                if vehicles[j] in self.commutes:
                    arriveWork = int(float(self.commutes[vehicles[j]][0])*pointsPerHour/60)
                    leaveWork = int(float(self.commutes[vehicles[j]][1])*pointsPerHour/60)
                else:
                    arriveWork = -1
                    leaveWork = -1

            if deadline != None:
                if departure > (24+deadline)*pointsPerHour:
                    departure = (24+deadline)*pointsPerHour

                    if perturbDeadline == True:
                        departure += int(pointsPerHour*2*(random.random()-1))

            # check if constraint is feasible
            if chargeAtWork == False:
                if (departure-arrival)*pMax/pointsPerHour < b[j]:
                    print('i have found an infeasible constraint')
                    b[j] = (departure-arrival)*pMax/pointsPerHour-0.1
                    
            else:
                if (departure-arrival+leaveWork-arriveWork)*pMax/pointsPerHour < b[j]:
                    print('i have found an infeasible constraint')
                    b[j] = (departure-arrival+leaveWork-arriveWork)*pMax/pointsPerHour-0.1
            
            for i in range(0,t):
                A1[n*(t*j+i)+j] = 1.0/float(pointsPerHour) # kWh -> kW
                if i < arrival or i > departure:
                    A2[n*(t*j+i)+j] = 1.0
                if chargeAtWork == True:
                    if i >= arriveWork and i <= leaveWork:
                        A2[n*(t*j+i)+j] = 0.0
                    elif i >= arriveWork+24*pointsPerHour and i <= leaveWork+24*pointsPerHour:
                        A2[n*(t*j+i)+j] = 0.0
                        

        A = sparse([A1,A2])

        A3 = spdiag([-1]*(t*n)) # ensures non-negative charging powers
        A4 = spdiag([1]*(t*n)) # ensures charging powers less than pMax
        G = sparse([A3,A4])
        
        h = []
        for i in range(0,t*n):
            h.append(0.0)
        for i in range(0,t*n):
            h.append(pMax)

        h = matrix(h)

        q = [] # incorporates base load into the objective function
        for i in range(0,n):
            for j in range(0,len(baseLoad)):
                q.append(baseLoad[j])

        q = matrix(q)

        I = spdiag([1]*t)
        P = sparse([[I]*n]*n)
 
        sol = solvers.qp(P,q,G,h,A,b) # solve quadratic program
        X = sol['x']

        for i in range(0,n):
            
            load = []
            for j in range(0,t):
                load.append(X[i*t+j]) # extract each vehicles load

            profiles[vehicles[i]] = load

        for i in range(0,len(unused)):
            profiles[unused[i]] = [0.0]*t

        return profiles
        
class AreaEnergyPrediction:

    def __init__(self,region,ucPopulation,utPopulation,rtPopulation,
                 rvPopulation,day,month,vehicle=None,penetration=1.0,
                 smoothTimes=False):

        # region:

        # xxPopulation: the number of people in the area living in places
        #               classified as xx

        # day: '1' = Mon, '2' = Tue etc.

        # month: '1' = Jan, '2' = 'Feb' etc.

        # vehicle: 'nissanLeaf', 'teslaS60D' and 'bmwI3' avaliable

        self.day = day
        self.month = month

        self.ucPopulation = float(ucPopulation)
        self.utPopulation = float(utPopulation)
        self.rtPopulation = float(rtPopulation)
        self.rvPopulation = float(rvPopulation)

        self.penetration = penetration

        self.totalPopulation = ucPopulation + utPopulation + rtPopulation +\
                               rvPopulation

        self.ucPer = float(ucPopulation)/self.totalPopulation
        self.utPer = float(utPopulation)/self.totalPopulation
        self.rtPer = float(rtPopulation)/self.totalPopulation
        self.rvPer = float(rvPopulation)/self.totalPopulation
        
        if vehicle == None or vehicle == 'nissanLeaf':
            vehicle = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)
        elif vehicle == 'teslaS60D':
            vehicle = Vehicle(2273.0,37.37,0.1842,0.01508,0.94957,60.0)
        elif vehicle == 'bmwI3':
            vehicle = Vehicle(1420.0,22.9,0.346,0.01626,0.87785,22.0)

        # run a simulation filtering for each of the region types
        if ucPopulation > 0:
            self.uc = EnergyPrediction(day,month,vehicle,region=region,
                                       regionType='1',penetration=penetration,
                                       smoothTimes=smoothTimes)
            #self.ucScale = float(ucPopulation)/self.uc.nPeople
            self.ucScale = float(self.totalPopulation)/self.uc.nPeople
        else:
            self.ucScale = 0.0
            self.uc = None

            
        if utPopulation > 0:
            self.ut = EnergyPrediction(day,month,vehicle,region=region,
                                       regionType='2',penetration=penetration,
                                       smoothTimes=smoothTimes)
            #self.utScale = float(utPopulation)/self.ut.nPeople
            self.utScale = float(self.totalPopulation)/self.ut.nPeople
        else:
            self.utScale = 0.0
            self.ut = None

            
        if rtPopulation > 0:
            self.rt = EnergyPrediction(day,month,vehicle,region=region,
                                       regionType='3',penetration=penetration,
                                       smoothTimes=smoothTimes)
            #self.rtScale = float(rtPopulation)/self.rt.nPeople
            self.rtScale = float(self.totalPopulation)/self.rt.nPeople
        else:
            self.rtScale = 0.0
            self.rt = None

            
        if rvPopulation > 0:
            self.rv = EnergyPrediction(day,month,vehicle,region=region,
                                       regionType='4',penetration=penetration,
                                       smoothTimes=smoothTimes)
            #self.rvScale = float(rvPopulation)/self.rv.nPeople
            self.rvScale = float(self.totalPopulation)/self.rv.nPeople
        else:
            self.rvScale = 0.0
            self.rv = None

    def getNumberOfVehicles(self):

        numberVehicles = 0

        if self.ucPopulation > 0:
            #numberVehicles += self.uc.nVehicles*self.ucScale
            ucVehicles = self.uc.nVehicles*self.ucScale
            numberVehicles += ucVehicles*self.ucPer

        if self.utPopulation > 0:
            #numberVehicles += self.ut.nVehicles*self.utScale
            utVehicles = self.ut.nVehicles*self.utScale
            numberVehicles += utVehicles*self.utPer

        if self.rtPopulation > 0:
            #numberVehicles += self.rt.nVehicles*self.rtScale
            rtVehicles = self.rt.nVehicles*self.rtScale
            numberVehicles += rtVehicles*self.rtPer

        if self.rvPopulation > 0:
            #numberVehicles += self.rv.nVehicles*self.rvScale
            rvVehicles = self.rv.nVehicles*self.rvScale
            numberVehicles += rvVehicles*self.rvPer

        return numberVehicles


    def getDumbChargingProfile(self,power,nHours,sCharge=True,extraCharge=True):

        self.nHours = nHours

        if self.ucPopulation > 0:
            ucProfile = self.uc.getDumbChargingProfile(power,nHours*60,
                                                       scaleFactor=self.ucScale,
                                                       superCharge=sCharge,
                                                       highUseHomeCharging=extraCharge,
                                                       highUseWorkCharging=extraCharge,
                                                       highUseShopCharging=extraCharge)
        else:
            ucProfile = [0.0]*nHours*60
            
        if self.utPopulation > 0:
            utProfile = self.ut.getDumbChargingProfile(power,nHours*60,
                                                       scaleFactor=self.utScale,
                                                       superCharge=sCharge,
                                                       highUseHomeCharging=extraCharge,
                                                       highUseWorkCharging=extraCharge,
                                                       highUseShopCharging=extraCharge)
        else:
            utProfile = [0.0]*nHours*60
            
        if self.rtPopulation > 0:
            rtProfile = self.rt.getDumbChargingProfile(power,nHours*60,
                                                       scaleFactor=self.rtScale,
                                                       superCharge=sCharge,
                                                       highUseHomeCharging=extraCharge,
                                                       highUseWorkCharging=extraCharge,
                                                       highUseShopCharging=extraCharge)
        else:
            rtProfile = [0.0]*nHours*60
            
        if self.rvPopulation > 0:
            rvProfile = self.rv.getDumbChargingProfile(power,nHours*60,
                                                       scaleFactor=self.rvScale,
                                                       superCharge=sCharge,
                                                       highUseHomeCharging=extraCharge,
                                                       highUseWorkCharging=extraCharge,
                                                       highUseShopCharging=extraCharge)
        else:
            rvProfile = [0.0]*nHours*60
            
        
        dumbProfile = []

        for i in range(0,nHours*60):
           dumbProfile.append(ucProfile[i]*self.ucPer+utProfile[i]*self.utPer+\
                              rtProfile[i]*self.rtPer+rvProfile[i]*self.rvPer)

        return dumbProfile

    def getPsuedoOptimalProfile(self,pMax,nHours=36,deadline=9,weighted=False):

        try:
            baseLoad = self.baseLoad
        except:                
            areaBase = BaseLoad(self.day,self.month,nHours,unit='k')
            baseLoad = areaBase.getLoad(population=self.totalPopulation)
            self.baseLoad = baseLoad

        pops = [self.ucPopulation,self.utPopulation,self.rtPopulation,
                self.rvPopulation,]
        objs = [self.uc,self.ut,self.rt,self.rv]
        scales = [self.ucScale,self.utScale,self.rvScale,self.rvScale]

        profiles = []

        for i in range(0,4):

            if pops[i] > 0:
                profiles.append(objs[i].getPsuedoOptimalProfile(pMax,baseLoad,
                                                                scaleFactor=scales[i],
                                                                weighted=weighted,
                                                                deadline=deadline))
            else:
                profiles.append([0.0]*len(baseLoad))
        '''            
        if self.utPopulation > 0:
            utProfile = self.ut.getPsuedoOptimalProfile(pMax,baseLoad,
                                                       scaleFactor=self.utScale,
                                                        weighted=weighted,
                                                        deadline=deadline,
                                                        returnIndividual=returnIndividual)
        else:
            utProfile = [0.0]*len(baseLoad)
            
        if self.rtPopulation > 0:
            rtProfile = self.rt.getPsuedoOptimalProfile(pMax,baseLoad,
                                                       scaleFactor=self.rtScale,
                                                        weighted=weighted,
                                                        deadline=deadline,
                                                        returnIndividual=returnIndividual)
        else:
            rtProfile = [0.0]*len(baseLoad)
            
        if self.rvPopulation < 0:
            rvProfile = self.rv.getPsuedoOptimalProfile(pMax,baseLoad,
                                                       scaleFactor=self.rvScale,
                                                        weighted=weighted,
                                                        deadline=deadline,
                                                        returnIndividual=returnIndividual)
        else:
            rvProfile = [0.0]*len(baseLoad)
        '''            
        profile = []

        for i in range(0,len(baseLoad)):
            profile.append(profiles[0][i]*self.ucPer+profiles[1][i]*self.utPer+\
                           profiles[1][i]*self.rtPer+profiles[1][i]*self.rvPer)

        return profile

    def getOptimalChargingProfiles(self,pMax,nHours=36,pointsPerHour=1,
                                   allowOverCap=True,deadline=None,
                                   perturbDeadline=False,
                                   solar=None,chargeAtWork=False):

        try:
            baseLoad = self.baseLoad
        except:                
            areaBase = BaseLoad(self.day,self.month,nHours,unit='k')
            baseLoad = areaBase.getLoad(population=self.totalPopulation)
            self.baseLoad = baseLoad

        # solar is a csvfile contain several ordered pv profiles
        if solar != None:
            allProfiles = []
            chosenProfiles = {}
            with open(solar,'rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    allProfiles.append(row)

            nProfiles = len(allProfiles)
            chosenProfiles['l'] = allProfiles[0]
            chosenProfiles['m'] = allProfiles[int(nProfiles/2)]
            chosenProfiles['h'] = allProfiles[-1]

            self.solar = {}

            for profile in chosenProfiles:
                for i in range(0,len(chosenProfiles[profile])):
                    chosenProfiles[profile][i] = float(chosenProfiles[profile][i])

                # first I need the right number of hours
                chosenProfiles[profile] = chosenProfiles[profile] +\
                                          chosenProfiles[profile][:int((nHours-24)*2)]
                # now I need the right number of points
                newProfile = [0.0]*nHours*60

                for i in range(0,len(newProfile)):
                    p1 = int(2*i/60)
                    if p1 == len(chosenProfiles[profile])-1:
                        p2 = p1
                    else:
                        p2 = p1 + 1

                    f2 = float(2*i)/60 - p1
                    f1 = 1.0-f2

                    newProfile[i] = f1*chosenProfiles[profile][p1]+\
                                    f2*chosenProfiles[profile][p2]
                        
                chosenProfiles[profile] = newProfile
                self.solar[profile] = copy.copy(newProfile)

            profiles = {'l':{},'m':{},'h':{}}
            
        else:
            profiles = {'':{}}

        for key in profiles:
            newBase = copy.copy(baseLoad)

            if solar != None:
                for i in range(0,len(newBase)):
                    newBase[i] -= chosenProfiles[key][i]

                    #if newBase[i] < 0:
                    #    newBase[i] = 0
                if min(newBase) < 0:
                    offset = -1*min(newBase)+0.01
                    print('I HAVE AN OFFSET')
                    print('it is: ',end='')
                    print(offset)
                    for i in range(0,len(newBase)):
                        newBase[i] + offset
                    
            scale = [self.ucScale,self.utScale,self.rtScale,self.rvScale]
            per = [self.ucPer,self.utPer,self.rtPer,self.rvPer]
            sim = [self.uc,self.ut,self.rt,self.rv]

            for i in range(0,4):
                if scale[i] > 0:
                    newProfiles = sim[i].getOptimalChargingProfiles(pMax,newBase,
                                                                    baseScale=scale[i],
                                                                    nHours=nHours,
                                                                    pointsPerHour=pointsPerHour,
                                                                    deadline=deadline,
                                                                    perturbDeadline=perturbDeadline,
                                                                    allowOverCap=allowOverCap,
                                                                    chargeAtWork=chargeAtWork)

                    for vehicle in newProfiles:
                        load = newProfiles[vehicle]
                        for j in range(0,len(load)):
                            load[j] = load[j]*per[i]
                        profiles[key][vehicle] = load

        return profiles
    
    def getMissingCapacity(self):

        try:
            nHours = self.nHours
        except:
            raise Exception('please run get DumbChargingProfile first')

        scale = [self.ucScale,self.utScale,self.rtScale,self.rvScale]
        per = [self.ucPer,self.utPer,self.rtPer,self.rvPer]
        sim = [self.uc,self.ut,self.rt,self.rv]

        missingCapacity = [0.0]*100

        for i in range(0,4):
            if scale[i] > 0:
                mc = sim[i].getMissingCapacity(nHours)

                for j in range(0,len(missingCapacity)):
                    try:
                        missingCapacity[j] += mc[j]*per[i]
                    except:
                        missingCapacity.append(mc[j]*per[i])


        return missingCapacity
                
class NationalEnergyPrediction(AreaEnergyPrediction):

    def __init__(self,day,month,vehicle=None,penetration=1.0,smoothTimes=False):
        AreaEnergyPrediction.__init__(self,None,24037000,29052000,5993000,
                                      6058000,day,month,vehicle=vehicle,
                                      penetration=penetration,
                                      smoothTimes=smoothTimes)
        
