# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
#from cvxopt import matrix, spdiag, solvers, sparse
#import sklearn.cluster as clst

# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSvehicleLocation import LocationPrediction

# these are the csv files containing the data
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'


class ValueAssesment:

    def __init__(self, month, fleetSize, car=None, region=None,average=True,
                 regionType=None, smoothTimes=False,model='full'):
        # month: string of integer 1-12 symbolising month
        # vehicle: vehicle object
        # regionType (opt): string filtering for a specific region type
        # region (opt): string filtering for a specific region

        if car == None or car == 'nissanLeafS':
            car = Vehicle(1647.7,29.97,0.0713,0.02206,0.84,24.0)
        elif car == 'nissanLeafSL':
            car = Vehicle(1647.7,0,29.61,0.0738,0.02195,0.86,30.0)
        elif car == 'nissanLeafSV':
            car = Vehicle(1704.5,29.92,0.076,0.02195,0.847,30.0)
        elif car == 'bmwI3':
            car = Vehicle(1420.4,22.9,0.346,0.01626,0.849,18.8)
        elif car == 'teslaS60D':
            car = Vehicle(2272.7,37.37,0.1842,0.01508,0.969,60.0)
        elif car == 'teslaS60R':
            car = Vehicle(2272.7,40.35,0.1324,0.01557,0.884,60.0)
        elif car == 'teslaS70D':
            car = Vehicle(2272.7,36.23,0.1906,0.01746,0.865,70.0)
        elif car == 'teslaS75D':
            car = Vehicle(2272.7,37.37,0.1842,0.01508,0.964,75.0)
        elif car == 'teslaS75R':
            car = Vehicle(2272.7,40.35,0.1324,0.01557,0.943,75.0)
        elif car == 'teslaS85D':
            car = Vehicle(2272.7,36.23,0.1906,0.01746,0.86,85.0)
        elif car == 'teslaS90D':
            car = Vehicle(2272.7,39.24,0.1493,0.01514,0.952,90.0)
        elif car == 'teslaSP100D':
            car = Vehicle(2386.4,41.35,0.267,0.0137,0.956,100.0)
        elif car == 'teslaP85D':
            car = Vehicle(2386.4,41.91,0.1389,0.0185,0.812,85.0)
        elif car == 'teslaSP90D':
            car = Vehicle(2386.4,41.51,0.2226,0.01403,0.939,90.0)
        elif car == 'teslaX60D':
            car = Vehicle(2500.0,37.68,0.0486,0.0214,0.953,60.0)
        elif car == 'teslaX75D':
            car = Vehicle(2500.0,37.68,0.0486,0.0214,0.957,75.0)
        elif car == 'teslaX90D':
            car = Vehicle(2500.0,37.68,0.0486,0.0214,0.931,90.0)
        elif car == 'teslaXP10D':
            car = Vehicle(2727.3,45.71,-0.0555,0.0216,0.928,100.0)
        elif car == 'BYDe6':
            car = Vehicle(2500,69.473,0.0697,0.02814,0.911,61.0)
        elif car == 'chevroletSpark':
            car = Vehicle(1420.45,21.96,0.1688,0.01806,0.78,19.0)
        elif car == 'fiat500e':
            car = Vehicle(1477.3,24.91,0.2365,0.01816,0.79,22.0)
        elif car == 'toyotaScionIQ':
            car = Vehicle(1250,15.993,0.56499,0.013095,0.844,12.0)
        elif car == 'toyotaRAV4':
            car = Vehicle(1931.8,32.246,0.27335,0.022058,0.721,41.8)
        elif car == 'VWeGolf':
            car = Vehicle(1647.7,39.36,0.5083,0.0125,0.942,24.2)
        elif car == 'kiaSoul':
            car = Vehicle(1647.7,22.058,0.25763,0.022168,0.881,27.0)
        elif car == 'coda':
            car = Vehicle(1818.2,39.18,0.2549,0.0199,0.635,31.0)
        elif car == 'mercedesBclass':
            car = Vehicle(1931.8,31.7,0.177,0.019,0.681,36.0)
        elif car == 'mercedesSmart':
            car = Vehicle(1079.5,32.869,-0.1639,0.028583,0.786,17.6)
        elif car == 'hondaFit':
            car = Vehicle(1647.7,19.06,0.407,0.01499,0.813,20.0)
        elif car == 'mitsubishiMiEV':
            car = Vehicle(1306.8,19.484,0.43515,0.016133,0.752,16.0)
        else:
            raise Exception('i do not recongnise that vehicle')

        self.month = month
        self.fleetSize = fleetSize
        self.car = car
        self.region = region
        self.regionType = regionType
        self.chargingEfficiency = 0.9

        self.nVehicles = 0

        # first getting the region types
        self.reg1 = {} # 1:urban, 2:rural, 3:scotland

        if regionType is not None:
            self.reg2 = {} # 1:uc, 2:ut, 3:rt, 4:rv, 5:scotland

        if region is not None:
            self.reg3 = {} # 1:NE, 2:NW, 3:Y+H, 4:EM, 5:WM, 6:E, 7:L, 8:SE, 9:SW,
                      # 10: Wales, 11: Scotland

        if average == False:
            vehicleList = []
                      
        # setting up counters which will be used to scale predictions
        self.nVehicles = 0 
        self.nHouseholds = 0
        self.journeyLogs = {}
        self.demand = [0.0]*1440*7

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

                    if region is not None:
                        self.reg3[row[0]] = row[28]

        
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

                if vehicle not in self.journeyLogs:
                    self.journeyLogs[vehicle] = []
                    self.nVehicles += 1

                    if average == False:
                        vehicleList.append(vehicle)

                day = int(row[5])-1

                try:
                    passengers = int(row[13]) # find the # people in the car
                except:
                    passengers = 1 # if missing assume only the driver

                try:
                    tripEnd = int(row[9])
                    tripStart = int(row[8])
                    tripDistance = float(row[10])*1609.34 # miles -> m
                    purposeTo = int(row[12])
                except:
                    continue # skip trips without a time or length

                if smoothTimes == True:
                    shift = 30*random.random()
                    tripEnd = int(30*int(tripEnd/30)+shift)
                    tripStart = int(30*int(tripStart/30)+shift)

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
                    energyConsumption = car.getEnergyExpenditure(cycle,
                                                                 accessoryLoad[row[6]])

                    car.load = 0
                    
                elif model == 'linear':
                    energyConsumption += tripDistance*0.23/1609.34

                if tripStart == tripEnd:
                    tripEnd += 30

                if tripStart > tripEnd:
                    tripEnd += 1440

                tripStart += day*1440
                tripEnd += day*1440

                self.journeyLogs[vehicle].append([tripStart,tripEnd,
                                                  energyConsumption,purposeTo])


        # now scale for fleetsize
        if average == True or fleetSize > self.nVehicles:
            self.sf = fleetSize/self.nVehicles

            for vehicle in self.journeyLogs:
                for journey in self.journeyLogs[vehicle]:
                    journey[2] = journey[2]*self.sf
                    
        else:
            if fleetSize < self.nVehicles:
                self.sf = 1
                chosenVehicles = []

                while len(chosenVehicles) < fleetSize:
                    ran = int(random.random()*len(vehicleList))
                    if vehicleList[ran] not in chosenVehicles:
                        chosenVehicles.append(vehicleList[ran])

                newLogs = {}

                for vehicle in chosenVehicles:
                    newLogs[vehicle] = self.journeyLogs[vehicle]

                self.journeyLogs = newLogs

        for vehicle in self.journeyLogs:
            self.journeyLogs[vehicle] = sorted(self.journeyLogs[vehicle])
                
    
    def chargeOpportunistically(self,power,time_threshold,chargeLocations=[23],
                                td_int=1):

        # time_threshold = min parked time to start charging
        # power = power in kW which vehicles charge at

        outOfCharge = []
        nOutOfCharge = 0

        self.total = [0]*1440*7
        self.turnDown = [0]*int(1440*7/td_int)
        self.chargeLogs = {}
        
        for vehicle in self.journeyLogs:
            self.chargeLogs[vehicle] = []
            log = self.journeyLogs[vehicle]
            battery = self.car.capacity*self.sf
            t_i = 0

            N = len(log)

            for i in range(N-1):
                parkStart = log[i][1]
                parkEnd = log[i+1][0]
                kWh = log[i][2]
                location = log[i][3]

                while t_i < parkStart:
                    self.total[t_i] += battery
                        
                    t_i += 1

                battery -= kWh
                if battery <= 0:
                    if vehicle not in outOfCharge:
                        outOfCharge.append(vehicle)

                if parkEnd-parkStart < time_threshold:
                    continue
                
                if chargeLocations != []:
                    if location not in chargeLocations:
                        continue

                for t in range(parkStart,parkEnd):
                    
                    if battery < self.car.capacity*self.sf:
                        self.demand[t] += power*self.sf
                        battery += power*self.sf*self.chargingEfficiency/60
                        chargeEnd = copy.copy(t)
                        
                    if battery > self.car.capacity*self.sf:
                        self.demand[t] -= (battery-self.car.capacity*self.sf)*60
                        battery = self.car.capacity*self.sf
                        
                    self.total[t] += battery

                t_i = parkEnd

                tdStart = int(parkStart/td_int)+1
                tdEnd = int(chargeEnd/td_int)

                floatTime = parkEnd-chargeEnd
                if floatTime > td_int:
                    # then we can shift by atleast one time interval
                    for i in range(tdStart,tdEnd):
                        self.turnDown[i] += power*self.sf
            try:
                parkStart = log[-1][1]
                chargeEnd = log[-1][1]
            except:
                continue # some logs are empty - WHY???
            
            # plug in if necessary
            while t_i < 1440*7:
                if battery < self.car.capacity*self.sf:
                    self.demand[t_i] += power*self.sf
                    battery += power*self.sf*self.chargingEfficiency/60
                    chargeEnd = copy.copy(t_i)
                
                if battery > self.car.capacity*self.sf:
                    self.demand[t_i] -= (battery-self.car.capacity*self.sf)*60
                    battery = self.car.capacity*self.sf

                self.total[t_i] += battery

                t_i += 1

            tdStart = int(parkStart/td_int)+1
            tdEnd = int(chargeEnd/td_int)

            floatTime = parkEnd-chargeEnd
            if floatTime > td_int:
                # then we can shift by atleast one time interval
                for i in range(tdStart,tdEnd):
                    self.turnDown[i] += power*self.sf

        print(nOutOfCharge)

        print(str(round(100*float(len(outOfCharge))/self.nVehicles,2))+'% vehicles out of charge')
                        
                
        

            
                

        
