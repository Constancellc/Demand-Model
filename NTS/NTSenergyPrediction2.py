# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
from cvxopt import matrix, spdiag, solvers, sparse
import sklearn.cluster as clst
import sys

# my code
sys.path.append('../')
from vehicleModel import Drivecycle, Vehicle

# This version is going to be more geared explicitly towards the national
# simiulation and journal paper

# these are the csv files containing the data
trips = '../../Documents/UKDA-5340-tab/constance-trips.csv'
households = '../../Documents/UKDA-5340-tab/constance-households.csv'

nextDay = {'1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'1'}
class EnergyPrediction:

    def __init__(self,day,month,regionType,population,car=None,region=None,
                 smoothTimes=False,yearsLower=2002):

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
        elif car == 'teslaXP100D':
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
        elif type(car) == str:
            raise Exception('i do not recongnise that vehicle')
            
        self.day = day
        self.month = month
        self.car = car
        self.regionType = regionType # a vector of % in each regionType
        self.region = region # the region of interest
        self.chargingEfficiency = 0.9
        self.smoothTimes = smoothTimes
        self.population = population
                      
        # setting up counters which will be used to scale predictions
        self.nPeople = [0]*4
        self.nVehicles = [0]*4
        self.nOutOfCharge = 0
        
        # getting the number of people represented to calculate the sf
        with open(households,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row[1] != month: # skip households from the wrong month
                    continue

                if self.region != None:
                    if row[3] != self.region:
                        continue
                    
                if int(row[5]) < yearsLower:
                    continue
                try:
                    rt = int(row[2]) # region type
                except:
                    continue
                if rt > 4:
                    continue

                self.nPeople[rt-1] += int(row[4])

        # now calculating the required sf
        self.sf = [0.0]*4
        for i in range(4):
            self.sf[i] = self.population*self.regionType[i]/self.nPeople[i]

        self.energy = {}
        self.vehicleRType = {}
        self.startTimes = {}
        self.endTimes = {}
        
        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row[6] != day:
                    continue
                if row[7] != month:
                    continue
                if int(row[8]) < yearsLower:
                    continue
                if self.region != None:
                    if row[5] != self.region:
                        continue
                try:
                    vehicle = row[2]
                    distance = float(row[11])*1609.34 # miles -> m
                    start = int(row[9])
                    end = int(row[10])
                    rType = int(row[4])-1
                    numParty = int(row[14])
                except:
                    continue

                if rType > 3:
                    continue

                if end < start:
                    end += 1440

                if vehicle not in self.energy:
                    self.energy[vehicle] = 0.0
                    self.endTimes[vehicle] = 0
                    self.startTimes[vehicle] = 1440
                    self.vehicleRType[vehicle] = rType
                    self.nVehicles[rType] += 1

                if smoothTimes == True:
                    shift = 30*random.random()
                    end = int(30*int(end/30)+shift)
                    start = int(30*int(start/30)+shift)

                if start < self.startTimes[vehicle]:
                    self.startTimes[vehicle] = start
                if end > self.endTimes[vehicle]:
                    self.endTimes[vehicle] = end

                # if the trip is really long, run the motorway artemis
                if distance > 30000:
                    cycle = Drivecycle(distance,'motorway')

                # otherwise run the rural/urban depending on the location
                elif rType > 1:
                    cycle = Drivecycle(distance,'rural')
                else:
                    cycle = Drivecycle(distance,'urban')

                acLoad = {'1':1.5,'2':1.3,'3':0.8,'4':0.4,'5':0.1,
                                 '6':0.0,'7':0.0,'8':0.0,'9':0.0,'10':0.2,
                                 '11':0.7,'12':1.3}

                car.load = numParty*75 # add appropriate load to vehicle
                self.energy[vehicle] += car.getEnergyExpenditure(cycle,
                                                                 acLoad[month])
                car.load = 0

    def getNextDayStartTimes(self):
        self.nextDayStartTimes = {}

        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row[6] != nextDay[self.day]:
                    continue
                
                if row[2] not in self.energy:
                    continue

                try:
                    start = int(row[9])
                except:
                    continue

                if self.smoothTimes == True:
                    start = int(30*int(start/30)+30*random.random())

                if row[2] not in self.nextDayStartTimes:
                    self.nextDayStartTimes[row[2]] = start
                elif start < self.nextDayStartTimes[row[2]]:
                    self.nextDayStartTimes[row[2]] = start
                
    def removeOverCap(self):
        self.missingEnergy = 0
        
        for vehicle in self.energy:
            if self.energy[vehicle] > self.car.capacity:
                        
                self.missingEnergy += (self.energy[vehicle]-self.car.capacity)\
                                      *self.sf[self.vehicleRType[vehicle]]
                self.energy[vehicle] = self.car.capacity

                self.nOutOfCharge += 1

    
    def getDumbCharging(self,power,nHours=36,allowOverCap=False,units='k'):
        units_scale = {'k':1,'M':1000,'G':1000000}
        profile = [0.0]*nHours*60

        if allowOverCap == False:
            self.removeOverCap()

        for vehicle in self.energy:
            kWh = self.energy[vehicle]
            end = self.endTimes[vehicle]
            start = self.startTimes[vehicle]

            reqTime = int(60*kWh/power)+1

            for i in range(start,start+reqTime):
                if i < 60*nHours:
                    profile[i] += power*self.sf[self.vehicleRType[vehicle]]\
                                  /units_scale[units]

        return profile

    def getOptimalLoadFlatteningProfile(self,baseLoad,pMax=3,nHours=36,
                                        pointsPerHour=60,deadline=None):

        # first cluster on arrival and departure times

        self.getNextDayStartTimes()

        k = 10 # number of clusters
        T = nHours*pointsPerHour

        if deadline == None:
            deadline = pointsPerHour*(nHours-24)

        data = []
        v = []
        for vehicle in self.energy:
            v.append(vehicle)
            a = self.endTimes[vehicle]
            try:
                d = self.nextDayStartTimes[vehicle]
            except:
                d = 1440
            if d > deadline:
                d = deadline
            data.append([a,d])

        centroid, label, inertia = clst.k_means(data,k)
        
        # for visualisation of clusters
        '''
        x = {}
        y = {}
        for i in range(3):
            x[i] = []
            y[i] = []
            
        for i in range(len(data)):
            x[label[i]].append(data[i][0])
            y[label[i]].append(data[i][1])
        
        plt.figure(1)
        for i in range(3):
            plt.scatter(x[i],y[i],alpha=0.2)
        plt.show()
        '''
        print(centroid)

        # stack vehicles into units
        b = [0.0]*(2*k)
        h = [0.0]*k
        for i in range(len(label)):
            vehicle = v[i]
            b[label[i]] += self.energy[vehicle]*\
                           self.sf[self.vehicleRType[vehicle]]
            h[label[i]] += self.sf[self.vehicleRType[vehicle]]*pMax

        # now set up the optimization
        A1 = matrix(0.0,(k,T*k)) # ensures right amount of energy provided
        A2 = matrix(0.0,(k,T*k)) # ensures vehicle only charges when avaliable

        for j in range(k):
            for t in range(T):
                A1[k*(T*j+t)+j] = 1.0/pointsPerHour
                if t<centroid[j][0] or t>(centroid[j][1]+24*pointsPerHour):
                    A2[k*(T*j+t)+j] = 1.0

        b = matrix(b)
        A = sparse([A1,A2])

        G = sparse([spdiag([-1]*(T*k)),spdiag([1]*(T*k))])
        print(G.size)
        h = matrix([0.0]*(T*k)+h*T)

        q = [] # incorporates base load into the objective function
        for i in range(0,k):
            for t in range(0,T):
                q.append(baseLoad[t])

        q = matrix(q)

        I = spdiag([1]*T)
        P = sparse([[I]*k]*k)
 
        sol = solvers.qp(P,q,G,h,A,b) # solve quadratic program
        X = sol['x']

        profiles = [[0.0]*T]*k

        for i in range(k):
            for t in range(T):
                profiles[i][t] = X[i*T+t]

        plt.figure(1)
        plt.plot(profiles)
        plt.show()
        # now individually apply chosen profiles

        
class NationalEnergyPrediction(EnergyPrediction):

    def __init__(self,day,month,car=None,smoothTimes=False,yearsLower=2002):
        EnergyPrediction.__init__(self,day,month,[0.4,0.4,0.1,0.1],
                                  65640000,car=car,smoothTimes=smoothTimes,
                                  yearsLower=yearsLower)

        
        

