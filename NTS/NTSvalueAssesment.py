# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
from cvxopt import matrix, spdiag, solvers, sparse
import sklearn.cluster as clst
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSvehicleLocation import LocationPrediction

# these are the csv files containing the data
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'


class ValueAssesment:

    def __init__(self, month, fleetSize, vehicle=None, region=None,
                 regionType=None):
        # month: string of integer 1-12 symbolising month
        # vehicle: vehicle object
        # regionType (opt): string filtering for a specific region type
        # region (opt): string filtering for a specific region

        if car == None:
            nissanLeaf = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)
            car = nissanLeaf
        elif car == 'tesla':
            car = Vehicle(2273.0,37.37,0.1842,0.01508,0.94957,60.0)
        elif car == 'bmw':
            car = Vehicle(1420.0,22.9,0.346,0.01626,0.87785,22.0)

        self.month = month
        self.fleetSize = fleetSize
        self.vehicle = vehicle
        self.region = region
        self.regionType = regionType

        self.nVehicles = 0

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

                    if region is not None:
                        self.reg3[row[0]] = row[28]
        
        

class EnergyPrediction:

    def __init__(self, day, month=None, car=None, regionType=None, region=None,
                 model='full',penetration=1.0,smoothTimes=False,
                 recordUsage=False):
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

        if recordUsage == True:
            self.rtDemand = [0.0]*1440

        # first getting the region types
        self.reg1 = {} # 1:urban, 2:rural, 3:scotland

        if regionType is not None:
            self.reg2 = {} # 1:uc, 2:ut, 3:rt, 4:rv, 5:scotland

        if region is not None:
            self.reg3 = {} # 1:NE, 2:NW, 3:Y+H, 4:EM, 5:WM, 6:E, 7:L, 8:SE, 9:SW,
                      # 10: Wales, 11: Scotland

        self.profiles = {} # miles
        self.nVehicles = 0 

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

                if vehicle not in self.profiles:
                    self.profiles[vehicle] = [self.vehicle.cap]*(48*7)
                    self.nVehicles += 1

                day = int(row[5])
                
                try:
                    passengers = int(row[13]) # find the # people in the car
                except:
                    passengers = 1 # if missing assume only the driver

                try:
                    tripEnd = int(row[9])
                    tripStart = int(row[8])
                    tripDistance = float(row[10])*1609.34 # miles -> m
                except:
                    continue # skip trips without a time or length

                if smoothTimes == True:
                    shift = 30*random.random()
                    tripEnd = int(30*int(tripEnd/30)+shift)
                    tripStart = int(30*int(tripStart/30)+shift)
                
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
                    energyConsumption = car.getEnergyExpenditure(cycle,
                                                                 accessoryLoad[row[6]])

                    car.load = 0
                    
                elif model == 'linear':
                    energyConsumption += tripDistance*0.23/1609.34 
