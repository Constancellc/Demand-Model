# packages
import csv
import matplotlib.pyplot as plt
import numpy as np
# my code
from vehicleModelCopy import Drivecycle, Vehicle

# these are the csv files containing the data
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

class EnergyPrediction:

    def __init__(self, day, month, car, regionType=None, region=None):
        # day: string of integer 1-7 symbolising day of week
        # month: string of integer 1-12 symbolising month
        # car: vehicle object
        # regionType (opt): string filtering for a specific region type
        # region (opt): string filtering for a specific region
        self.car = car
        missingclass = 0
        ########################################################################
        # first getting the region types
        
        self.reg1 = {} # 1:urban, 2:rural, 3:scotland

        if regionType is not None:
            self.reg2 = {} # 1:uc, 2:ut, 3:rt, 4:rv, 5:scotland

        if region is not None:
            self.reg3 = {} # 1:NE, 2:NW, 3:Y+H, 4:EM, 5:WM, 6:E, 7:L, 8:SE, 9:SW,
                      # 10: Wales, 11: Scotland
        

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

                    if region is not None:
                        self.reg3[row[0]] = row[28]
        
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
                    
                if self.reg1[row[1]] == '1':
                    cycle = Drivecycle(tripDistance,'rural')
                elif self.reg1[row[1]] == '2':
                    cycle = Drivecycle(tripDistance,'urban')
                else:
                    # not really sure what to do here..?
                    missingclass += 1
                    continue
                    #cycle = Drivecycle(tripDistance,'rural')

                car.load = passengers*75 # add appropriate load to vehicle
                self.energy[vehicle] += car.getEnergyExpenditure(cycle,0.0)
                car.load = 0
        print missingclass,
        print ' trips were skipped due to missing classification'

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

    def getDumbChargingProfile(self,power,tmax):
        # power: the charging power in kW
        # tmax: the no. minutes past 00:00 the simulation is run for

        uncharged = 0

        if tmax < 24*60:
            print 'please choose a simulation length greater than a day'
            tmax = 24*60

        profile = [0.0]*tmax

        for vehicle in self.energy:
            kWh = self.energy[vehicle]
            chargeStart = self.endTimes[vehicle]
            chargeTime = int(kWh*60/power)

            chargeEnd = chargeStart+chargeTime

            if chargeEnd >= tmax:
                chargeEnd = tmax-1
                uncharged += 1

            for i in range(chargeStart,chargeEnd):
                profile[i] += power

        print uncharged,
        print ' vehicles did not reach full charge'

        return profile
        

                
                
