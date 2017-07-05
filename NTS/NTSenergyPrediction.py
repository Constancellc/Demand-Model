# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
from cvxopt import matrix, spdiag, solvers, sparse
# my code
from vehicleModelCopy import Drivecycle, Vehicle

# these are the csv files containing the data
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

class EnergyPrediction:

    def __init__(self, day, month=None, car=None, regionType=None, region=None,
                 model='full'):
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

        # first getting the region types
        
        self.reg1 = {} # 1:urban, 2:rural, 3:scotland

        if regionType is not None:
            self.reg2 = {} # 1:uc, 2:ut, 3:rt, 4:rv, 5:scotland

        if region is not None:
            self.reg3 = {} # 1:NE, 2:NW, 3:Y+H, 4:EM, 5:WM, 6:E, 7:L, 8:SE, 9:SW,
                      # 10: Wales, 11: Scotland
                      
        # setting up counters whihc will be used to scale predictions
        self.nVehicles = 0 
        self.nHouseholds = 0
        self.nPeople = 0

        with open(households,'rU') as csvfile:
            reader = csv.reader(csvfile,delimiter='\t')
            reader.next()
            for row in reader:

                if month is not None:
                    if row[9] != month: # skip households from the wrong month
                        continue
                
                if row[0] not in self.reg1:

                    self.reg1[row[0]] = row[148]

                    # bug: can't currently specify BOTH regiontype and region

                    if regionType is not None:
                        self.reg2[row[0]] = row[149]
                        if row[149] == regionType:
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
            reader.next()
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
            reader.next()
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

                if vehicle not in self.startTimes:
                    self.startTimes[vehicle] = tripStart
                else:
                    if tripStart < self.startTimes[vehicle]:
                        self.startTimes[vehicle] = tripStart


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
            print 'please choose a simulation length greater than a day'
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
                prof = [0]*tmax
                for i in range(chargeStart, chargeStart+chargeTime):
                    try:
                        prof[i] = power
                    except:
                        continue

                individualProfiles[vehicle] = prof
                

            chargeEnd = chargeStart+chargeTime

            if chargeEnd >= tmax:
                chargeEnd = tmax-1
                uncharged += 1

            for i in range(chargeStart,chargeEnd):
                profile[i] += scaleFactor*power

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
                            profile[i] += scaleFactor*chargePower

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
                    profile[i] += scaleFactor*power
                                            

                if outOfCharge is True:
                    self.nOutOfCharge += 1
                    
            if superCharge == True:
                scPower = 72 # kW
                for vehicle in self.outOfChargeLog:
                    for log in self.outOfChargeLog[vehicle]:
                        timeReq = int(log[0]*60/scPower)
                        for i in range(log[1],log[1]+timeReq):
                            try:
                                profile[i] += scaleFactor*scPower
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

        print self.nOutOfCharge,
        print ' out of '
        print self.nVehicles
        print ' vehicles ran out of charge'

        if individuals != []:
            return profile, individualProfiles
        else:
            return profile

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
                 print vehicle,
                 print extraCapacity
                 
        return extraRequirements
    
    def getPsuedoOptimalProfile(self,pMax,baseLoad,scaleFactor=1,
                                returnIndividual=False):

        if returnIndividual == True:
            individualProfiles = {}

        pointsPerHour = len(baseLoad)/36
        profile = [0.0]*len(baseLoad)

        # first calculate the target charging shape.
        target = [0.0]*len(baseLoad)
        lim = max(baseLoad)+1

        for i in range(0,len(baseLoad)):
            target[i] = lim-baseLoad[i]
            
        self.getNextDayStartTimes()
        
        for vehicle in self.energy:
            kWh = self.energy[vehicle]/self.chargingEfficiency
            chargeStart = self.endTimes[vehicle]
            chargeEnd = self.startTimes[vehicle]+24*pointsPerHour

            if chargeEnd >= 36*pointsPerHour:
                chargeEnd = 36*pointsPerHour-1

            chargeProfile = copy.copy(target)
            
            chargeProfile = chargeProfile[chargeStart:chargeEnd]

            try:
                energySF = kWh/(sum(chargeProfile)/pointsPerHour)
            except:
                print chargeStart
                print chargeEnd
                print kWh
                continue

            for i in range(0,len(chargeProfile)):
                chargeProfile[i] = chargeProfile[i]*energySF
                if chargeProfile[i] > pMax:
                    chargeProfile[i] = pMax

            if returnIndividual == True:
                if len(individualProfiles) < 4:
                    individualProfiles[vehicle] = [copy.copy(chargeProfile),
                                                   chargeStart]

            for i in range(chargeStart,chargeEnd):
                profile[i] += chargeProfile[i-chargeStart]*scaleFactor


            del chargeProfile

        if returnIndividual == True:
            return profile, individualProfiles

        else:
            return profile

        
    def getOptimalChargingProfiles(self,pMax,baseLoad,baseScale=1,nHours=36,
                                   pointsPerHour=1,individuals=[],
                                   sampleScale=True):
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
        
        # I'm going to need to downsample
        for vehicle in self.energy:
            if random.random() < 0.02 or vehicle in individuals:
                
                
                if self.energy[vehicle] == 0.0:
                    unused += [vehicle]
                    continue
                if self.energy[vehicle] >= self.car.capacity:
                    print self.energy[vehicle],
                    print ' is higher than battery capacity'
                    b.append(baseScale*self.energy[vehicle]/self.chargingEfficiency)

                    #b.append(baseScale*self.car.capacity/self.chargingEfficiency)
                else:
                    b.append(baseScale*self.energy[vehicle]/self.chargingEfficiency)

                vehicles.append(vehicle)               

        self.getNextDayStartTimes()

        #n = self.nVehicles
        n = len(vehicles)

        if sampleScale == True:
            scale = float(self.nVehicles/(len(unused)+len(vehicles))) # This accounts for downsampling
        else:
            scale = 1.0
        pMax = pMax*scale

        for i in range(0,len(b)):
            b[i] = b[i]*scale#*0.000001
            
        t = nHours*pointsPerHour

        if len(baseLoad) > t:
            f = len(baseLoad)/t
            newBaseLoad = []
            
            for i in range(0,t):
                newBaseLoad.append(baseLoad[i*f])
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
            
            for i in range(0,t):
                A1[n*(t*j+i)+j] = 1.0/float(pointsPerHour) # kWh -> kW
                if i < arrival or i > departure:
                    A2[n*(t*j+i)+j] = 1.0

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

class NationalEnergyPrediction:

    def __init__(self,day,month,vehicle=None):

        if vehicle == None:
            nissanLeaf = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)
            vehicle = nissanLeaf

        self.ukPopulation = 64100000
        
        self.breakdown = [0.369,0.446,0.092,0.0093] # region type pdf

        # run a simulation filtering for each of the region types
        self.uc = EnergyPrediction(day,month,nissanLeaf,regionType='1')
        self.ut = EnergyPrediction(day,month,nissanLeaf,regionType='2')
        self.rt = EnergyPrediction(day,month,nissanLeaf,regionType='3')
        self.rv = EnergyPrediction(day,month,nissanLeaf,regionType='4')

        # find the scale required to get a representative population
        ucScale = float(self.ukPopulation)*self.breakdown[0]/self.uc.nPeople
        utScale = float(self.ukPopulation)*self.breakdown[1]/self.ut.nPeople
        rtScale = float(self.ukPopulation)*self.breakdown[2]/self.rt.nPeople
        rvScale = float(self.ukPopulation)*self.breakdown[3]/self.rv.nPeople

        self.ucScale = ucScale/1000000 # kW -> GW
        self.utScale = utScale/1000000 # kW -> GW
        self.rtScale = rtScale/1000000 # kW -> GW
        self.rvScale = rvScale/1000000 # kW -> GW

    def getNationalDumbChargingProfile(self,power,nHours):

        self.nHours = nHours

        # get the scaled dumb charging profiles
        ucProfile = self.uc.getDumbChargingProfile(power,nHours*60,
                                                   scaleFactor=self.ucScale,
                                                   superCharge=True)
        utProfile = self.ut.getDumbChargingProfile(power,nHours*60,
                                                   scaleFactor=self.utScale,
                                                   superCharge=True)
        rtProfile = self.rt.getDumbChargingProfile(power,nHours*60,
                                                   scaleFactor=self.rtScale,
                                                   superCharge=True)
        rvProfile = self.rv.getDumbChargingProfile(power,nHours*60,
                                                   scaleFactor=self.rvScale,
                                                   superCharge=True)

        dumbProfile = []

        for i in range(0,len(ucProfile)):
            dumbProfile.append(ucProfile[i]+utProfile[i]+rtProfile[i]+
                               rvProfile[i])

        return dumbProfile

    def getNationalMissingCapacity(self):

        try:
            nHours = self.nHours
        except:
            raise Exception('please run getNationalDumbChargingProfile first')

        ucMissingCapacity = self.uc.getMissingCapacity(nHours)
        utMissingCapacity = self.ut.getMissingCapacity(nHours)
        rtMissingCapacity = self.rt.getMissingCapacity(nHours)
        rvMissingCapacity = self.rv.getMissingCapacity(nHours)

        missingCapacity = []

        for i in range(0,len(ucMissingCapacity)):
            missingCapacity.append(ucMissingCapacity[i]*1000+
                                   utMissingCapacity[i]*1000+
                                   rtMissingCapacity[i]*1000+
                                   rvMissingCapacity[i]*1000)
            # unit of thousands of vehicles (I think)

        return missingCapacity

    def getNationalPsuedoOptimalProfile(self,pMax,baseLoad):

        # get the scaled charging profiles
        ucProfile = self.uc.getPsuedoOptimalProfile(pMax,baseLoad,
                                                   scaleFactor=self.ucScale)
        utProfile = self.ut.getPsuedoOptimalProfile(pMax,baseLoad,
                                                   scaleFactor=self.utScale)
        rtProfile = self.rt.getPsuedoOptimalProfile(pMax,baseLoad,
                                                   scaleFactor=self.rtScale)
        rvProfile = self.rv.getPsuedoOptimalProfile(pMax,baseLoad,
                                                   scaleFactor=self.rvScale)

        profile = []

        for i in range(0,len(ucProfile)):
            profile.append(ucProfile[i]+utProfile[i]+rtProfile[i]+
                               rvProfile[i])

        return profile

    def getNationalOptimalChargingProfiles(self,pMax,baseLoad,nHours=36,
                                           pointsPerHour=1):

        # baseLoad is in GW

        profiles = {}

        ucBaseScale = float(self.ukPopulation)/(self.uc.nPeople*1000000)
        utBaseScale = float(self.ukPopulation)/(self.ut.nPeople*1000000)
        rtBaseScale = float(self.ukPopulation)/(self.rt.nPeople*1000000)
        rvBaseScale = float(self.ukPopulation)/(self.rv.nPeople*1000000)

        ucProfiles = self.uc.getOptimalChargingProfiles(pMax,baseLoad,
                                                        baseScale=ucBaseScale,
                                                        nHours=nHours,
                                                        pointsPerHour=1)

        utProfiles = self.ut.getOptimalChargingProfiles(pMax,baseLoad,
                                                        baseScale=utBaseScale,
                                                        nHours=nHours,
                                                        pointsPerHour=1)

        rtProfiles = self.rt.getOptimalChargingProfiles(pMax,baseLoad,
                                                        baseScale=rtBaseScale,
                                                        nHours=nHours,
                                                        pointsPerHour=1)

        rvProfiles = self.rv.getOptimalChargingProfiles(pMax,baseLoad,
                                                        baseScale=rvBaseScale,
                                                        nHours=nHours,
                                                        pointsPerHour=1)

        for vehicle in ucProfiles:
            load = ucProfiles[vehicle]
            for i in range(0,len(load)):
                load[i] = load[i]*self.breakdown[0]
            profiles[vehicle] = load

            
        for vehicle in utProfiles:
            load = utProfiles[vehicle]
            for i in range(0,len(load)):
                load[i] = load[i]*self.breakdown[1]
            profiles[vehicle] = load

            
        for vehicle in rtProfiles:
            load = rtProfiles[vehicle]
            for i in range(0,len(load)):
                load[i] = load[i]*self.breakdown[2]
            profiles[vehicle] = load

            
        for vehicle in rvProfiles:
            load = rvProfiles[vehicle]
            for i in range(0,len(load)):
                load[i] = load[i]*self.breakdown[3]
            profiles[vehicle] = load
        
        return profiles
        
        
        

                
                
