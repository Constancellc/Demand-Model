# packages
import csv
import random
import matplotlib.pyplot as plt
import numpy as np
from cvxopt import matrix, spdiag, solvers, sparse
# my code
from vehicleModelCopy import Drivecycle, Vehicle

# these are the csv files containing the data
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

class EnergyPrediction:

    def __init__(self, day, month, car=None, regionType=None, region=None):
        # day: string of integer 1-7 symbolising day of week
        # month: string of integer 1-12 symbolising month
        # car: vehicle object
        # regionType (opt): string filtering for a specific region type
        # region (opt): string filtering for a specific region

        if car == None:
            nissanLeaf = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)
            car = nissanLeaf
            
        self.day = day
        self.month = month
        self.car = car
        self.regionType = regionType
        self.region = region


            
        missingclass = 0
        ########################################################################
        # first getting the region types
        
        self.reg1 = {} # 1:urban, 2:rural, 3:scotland

        if regionType is not None:
            self.reg2 = {} # 1:uc, 2:ut, 3:rt, 4:rv, 5:scotland

        if region is not None:
            self.reg3 = {} # 1:NE, 2:NW, 3:Y+H, 4:EM, 5:WM, 6:E, 7:L, 8:SE, 9:SW,
                      # 10: Wales, 11: Scotland
                      
        self.nVehicles = 0
        self.nHouseholds = 0
        self.nPeople = 0

        with open(households,'rU') as csvfile:
            reader = csv.reader(csvfile,delimiter='\t')
            reader.next()
            for row in reader:

                if row[9] != month: # skip households from the wrong month
                    continue
                
                if row[0] not in self.reg1:
                    
                    self.reg1[row[0]] = row[148]

                    if regionType is not None:
                        self.reg2[row[0]] = row[149]
                        if row[149] == regionType:
                            self.nHouseholds += 1
                            self.nPeople += int(row[32])

                    elif region is not None:
                        self.reg3[row[0]] = row[28]
                        if row[28] == region:
                            self.nHouesholds += 1
                            self.nPeople += int(row[32])

                    else:
                        self.nHouseholds += 1
                        self.nPeople += int(row[32])
        
        ########################################################################
        # now getting the trip data and running it through the vehicle model

        self.distance = {} # miles
        self.energy = {} # kWh
        self.endTimes = {} # mins past 00:00 of last journey end

        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            for row in reader:
                if row[5] != day:
                    continue
                if row[6] != month:
                    continue

                if regionType is not None:
                    if self.reg2[row[1]] != regionType:
                        continue

                if region is not None:
                    if self.reg3[row[1]] != region:
                        continue

                vehicle = row[2]

                if vehicle == ' ': # skip trips where the vehicle is missing
                    continue

                if vehicle not in self.energy:
                    self.energy[vehicle] = 0.0
                    self.distance[vehicle] = 0.0
                    self.endTimes[vehicle] = 0
                    self.nVehicles += 1
                    
                try:
                    passengers = int(row[13]) # find the # people in the car
                except:
                    passengers = 1 # if missing assume only the driver

                try:
                    tripEnd = int(row[9])
                    tripDistance = float(row[10])*1609.34 #convert miles to m
                except:
                    continue # skip trips without a time or length
                
                self.distance[vehicle] += int(tripDistance) # m

                if tripEnd > self.endTimes[vehicle]:
                    self.endTimes[vehicle] = tripEnd

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
                    missingclass += 1
                    continue
                    #cycle = Drivecycle(tripDistance,'rural')
                accessoryLoad = {'1':1.5,'2':1.3,'3':0.8,'4':0.4,'5':0.1,
                                 '6':0.0,'7':0.0,'8':0.0,'9':0.0,'10':0.2,
                                 '11':0.7,'12':1.3}

                car.load = passengers*75 # add appropriate load to vehicle
                self.energy[vehicle] += car.getEnergyExpenditure(cycle,
                                                                 accessoryLoad[month])
                car.load = 0
        #print missingclass,
        #print ' trips were skipped due to missing classification'

    def getNextDayStartTimes(self):

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
                              normalise=False,offset=0,width=1):
        dailyEnergy = [0]*60

        for vehicle in self.energy:
            kWh = int(self.energy[vehicle])

            try:
                dailyEnergy[kWh] += 1
            except:
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
            
        plt.bar(np.arange(offset,60+offset,1),dailyEnergy,width=width,label=label)
    

        if wait == False:
            plt.show()

    def getDumbChargingProfile(self,power,tmax,scaleFactor=1,
                               scalePerHousehold=False):
        # power: the charging power in kW
        # tmax: the no. minutes past 00:00 the simulation is run for

        uncharged = 0
        outOfCharge = 0

        if tmax < 24*60:
            print 'please choose a simulation length greater than a day'
            tmax = 24*60

        profile = [0.0]*tmax

        for vehicle in self.energy:
            
            kWh = self.energy[vehicle]
            if kWh > 24:
                outOfCharge += 1
                kWh = 24
            chargeStart = self.endTimes[vehicle]
            chargeTime = int(kWh*60/power)

            chargeEnd = chargeStart+chargeTime

            if chargeEnd >= tmax:
                chargeEnd = tmax-1
                uncharged += 1

            for i in range(chargeStart,chargeEnd):
                profile[i] += scaleFactor*power

        if scalePerHousehold == True:
            for i in range(0,tmax):
                profile[i] = profile[i]/self.nHouseholds

        print outOfCharge,
        print ' out of '
        print self.nVehicles
        print ' vehicles ran out of charge'

        return profile

    def getOptimalChargingProfiles(self,pMax,baseLoad,baseScale,nHours=36,
                                   pointsPerHour=1):
        # pMax is the maximum charging power allowed
        # baseLoad is the vector of non-ev demand that we're trying to valley fill
        # baseScale is the ratio of the population creating the baseLoad to
        #   the population creating the charging demand

        profiles = {}

        vehicles = []
        b = []
        
        # I'm going to need to downsample
        for vehicle in self.energy:
            if random.random() < 0.01:
                vehicles.append(vehicle)
                b.append(baseScale*self.energy[vehicle])

        self.getNextDayStartTimes()

        #n = self.nVehicles
        n = len(vehicles)

        scale = float(self.nVehicles/n) # This accounts for downsampling
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

        #vehicles = []

        A1 = matrix(0.0,(n,t*n)) # ensures right amount of energy provided
        A2 = matrix(0.0,(n,t*n)) # ensures vehicle only charges when avaliable

        #b = []

        #for vehicle in self.energy:
#            vehicles.append(vehicle)
#            b.append(self.energy[vehicle])

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

        A3 = spdiag([-1]*(t*n))
        A4 = spdiag([1]*(t*n))

        G = sparse([A3,A4])
        
        h = []

        for i in range(0,t*n):
            h.append(0.0)
        for i in range(0,t*n):
            h.append(pMax)

        h = matrix(h)

        q = []
        for i in range(0,n):
            for j in range(0,len(baseLoad)):
                q.append(baseLoad[j])

        q = matrix(q)

        I = spdiag([1]*t)
        P = sparse([[I]*n]*n)
 
        sol = solvers.qp(P,q,G,h,A,b)
        X = sol['x']

        for i in range(0,n):
            load = []
            for j in range(0,t):
                load.append(X[i*t+j])

            profiles[vehicles[i]] = load
            
        return profiles

class NationalEnergyPrediction:

    def __init__(self,day,month,vehicle=None):

        if vehicle == None:
            nissanLeaf = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)
            vehicle = nissanLeaf

        # run a simulation filtering for each of the region types
        self.uc = EnergyPrediction(day,month,nissanLeaf,regionType='1')
        self.ut = EnergyPrediction(day,month,nissanLeaf,regionType='2')
        self.rt = EnergyPrediction(day,month,nissanLeaf,regionType='3')
        self.rv = EnergyPrediction(day,month,nissanLeaf,regionType='4')

        # find the scale required to get a representative population
        ucScale = float(23650000)/self.uc.nPeople
        utScale = float(28590000)/self.ut.nPeople
        rtScale = float(5900000)/self.rt.nPeople
        rvScale = float(5960000)/self.rv.nPeople

        self.ucScale = ucScale/1000000 # kW -> GW
        self.utScale = utScale/1000000 # kW -> GW
        self.rtScale = rtScale/1000000 # kW -> GW
        self.rvScale = rvScale/1000000 # kW -> GW

    def getNationalDumbChargingProfile(self,power):

        nHours = 36

        # get the scaled dumb charging profiles
        ucProfile = self.uc.getDumbChargingProfile(power,nHours*60,
                                                   scaleFactor=self.ucScale)
        utProfile = self.ut.getDumbChargingProfile(power,nHours*60,
                                                   scaleFactor=self.utScale)
        rtProfile = self.rt.getDumbChargingProfile(power,nHours*60,
                                                   scaleFactor=self.rtScale)
        rvProfile = self.rv.getDumbChargingProfile(power,nHours*60,
                                                   scaleFactor=self.rvScale)

        dumbProfile = []

        for i in range(0,len(ucProfile)):
            dumbProfile.append(ucProfile[i]+utProfile[i]+rtProfile[i]+
                               rvProfile[i])

        return dumbProfile

    def getNationalOptimalChargingProfiles(self,pmax,baseLoad,nHours=36,
                                           pointsPerHour=1):

        profiles = {}

        nUc = self.uc.nVehicles
        nUt = self.ut.nVehicles
        nRt = self.rt.nVehicles
        nRv = self.rv.nVehicles

        # gather a list of all of the vehicles
        vehicles = []

        for vehicle in self.uc:
            vehicles.append(vehicle)
        for vehicle in self.ut:
            vehicles.append(vehicle)
        for vehicle in self.rt:
            vehicles.append(vehicle)
        for vehicle in self.rv:
            vehicles.append(vehicle)

        n = nUc+nUt+nRt+nRv

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

        b = []

        for vehicle in self.energy:
            vehicles.append(vehicle)
            b.append(self.energy[vehicle])

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

        A3 = spdiag([-1]*(t*n))
        A4 = spdiag([1]*(t*n))

        G = sparse([A3,A4])
        
        h = []

        for i in range(0,t*n):
            h.append(0.0)
        for i in range(0,t*n):
            h.append(pMax)

        h = matrix(h)

        q = []
        for i in range(0,n):
            for j in range(0,len(baseLoad)):
                q.append(baseLoad[j])

        q = matrix(q)

        I = spdiag([1]*t)
        P = sparse([[I]*n]*n)

        sol = solvers.qp(P,q,G,h,A,b)
        X = sol['x']
        
        return profiles
        
        
        

                
                
