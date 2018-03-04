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
# simiulation and journal paper - a two day simulation

# these are the csv files containing the data
trips = '../../Documents/UKDA-5340-tab/constance-trips.csv'
households = '../../Documents/UKDA-5340-tab/constance-households.csv'

nextDay = {'1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'1'}
units_scale = {'k':1,'M':1000,'G':1000000}

def getBaseLoad(day,month,nHours,unit='G',pointsPerHour=60):
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

    interpolatedLoad = [0.0]*nHours*pointsPerHour
    for i in range(0,len(interpolatedLoad)):
        p1 = int(2*i/pointsPerHour)
        p2 = p1+1

        f2 = 2*float(i)/pointsPerHour - p1
        f1 = 1.0-f2

        interpolatedLoad[i] = f1*float(profile[p1])+f2*float(profile[p2])

        # Change the units to the specified ones
        interpolatedLoad[i] = interpolatedLoad[i]*1000000/units_scale[unit]

    return interpolatedLoad
    
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
        self.nOutOfCharge = [0,0]
        
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
                if row[6] != day and row[6] != nextDay[day]:
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

                if row[6] == day:
                    dayNo = 0
                else:
                    dayNo = 1

                if rType > 3:
                    continue

                if end < start:
                    end += 1440

                if vehicle not in self.energy:
                    self.energy[vehicle] = [0.0,0.0]
                    self.endTimes[vehicle] = [0,0]
                    self.startTimes[vehicle] = [1440,1440]
                    self.vehicleRType[vehicle] = rType
                    self.nVehicles[rType] += 1

                if smoothTimes == True:
                    shift = 30*random.random()
                    end = int(30*int(end/30)+shift)
                    start = int(30*int(start/30)+shift)

                if start < self.startTimes[vehicle][dayNo]:
                    self.startTimes[vehicle][dayNo] = start
                if end > self.endTimes[vehicle][dayNo]:
                    self.endTimes[vehicle][dayNo] = end

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
                self.energy[vehicle][dayNo] += car.getEnergyExpenditure(cycle,
                                                                 acLoad[month])
                car.load = 0

    def getNextDayStartTimes(self):
        self.nextDayStartTimes = {}

        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row[6] != nextDay[nextDay[self.day]]:
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
            for day in range(2):
                if self.energy[vehicle][day] > self.car.capacity:
                            
                    self.missingEnergy += (self.energy[vehicle][day]-self.car.capacity)\
                                          *self.sf[self.vehicleRType[vehicle]]
                    self.energy[vehicle][day] = self.car.capacity

                    self.nOutOfCharge[day] += 1

    
    def getDumbCharging(self,power,nHours=60,allowOverCap=False,units='k'):
        profile = [0.0]*nHours*60

        if allowOverCap == False:
            self.removeOverCap()

        for vehicle in self.energy:
            for day in range(2):
                kWh = self.energy[vehicle][day]
                end = self.endTimes[vehicle][day]
                start = self.startTimes[vehicle][day]

                reqTime = int(60*kWh/power)+1

                if reqTime < 2:
                    continue

                for i in range(start+day*1440,start+reqTime+day*1440):
                    if i < 60*nHours:
                        profile[i] += power*self.sf[self.vehicleRType[vehicle]]\
                                      /units_scale[units]

        return profile

    def getOptimalLoadFlatteningProfile(self,baseLoad,pMax=3,
                                        pointsPerHour=60,deadline=12,
                                        storeIndividuals=False):

        # ok so in the new plan we cluster the two days seperately and optimise
        # considering them independantly

        '''

        however the time horizon defined will be different - we will set a
        deadline time - e.g. 12:00 and the vehicle will consider 24+deadline
        hours - in the example 36 hours

        However we load flatten over 48+deadline hours

        This is going to make the quadratic term slightly more complicated as
        not all vehicles entirely overlap

        the linear term will be fine - we will just use a time-shifted baseload
        for the day 2 vehicles

        '''
        # first cluster on arrival and departure times
        self.getNextDayStartTimes()
        sTimes = [self.startTimes,self.nextDayStartTimes]

        k = 4 # number of clusters
        
        T = (24+deadline)*pointsPerHour
        To = deadline*pointsPerHour # overlap time
        Ts = 24*pointsPerHour


        data = [[],[]]
        v = [[],[]]
        for vehicle in self.energy:
            for day in range(2):
                if self.energy[vehicle][day] == 0.0:
                    continue
                
                v[day].append(vehicle)

                a = self.endTimes[vehicle][day]
                try:
                    d = sTimes[day][vehicle]+1440
                except:
                    d = 1440+deadline*60
                if d > 1440+deadline*60:
                    d = 1440+deadline*60

                a = int(pointsPerHour*a/60)
                d = int(pointsPerHour*d/60)

                data[day].append([a,d])
                
        centroid = [[],[]]
        label = [[],[]]
        inertia = [[],[]]

        for day in range(2):
            centroid[day], label[day], inertia[day] = clst.k_means(data[day],k)
            
            # for visualisation of clusters
            '''
            x = {}
            y = {}
            for i in range(k):
                x[i] = []
                y[i] = []
                
            for i in range(len(data[day])):
                x[label[i]].append(data[day][i][0])
                y[label[i]].append(data[day][i][1])
            
            plt.figure(day+1)
            for i in range(k):
                plt.scatter(x[i],y[i],alpha=0.2)
        plt.show()
        '''
        print(centroid)

        # stack vehicles into units
        b = [0.0]*(3*k)
        h0 = [0.0]*(2*k)
        for day in range(2):
            for i in range(len(label[day])):
                vehicle = v[day][i]
                b[label[day][i]+day*k] += self.energy[vehicle][day]*\
                               self.sf[self.vehicleRType[vehicle]]
                h0[label[day][i]+day*k] += self.sf[self.vehicleRType[vehicle]]*pMax

        h = []
        for j in range(k):
            for t in range(Ts):
                h.append(h0[j])
        for j in range(2*k):
            for t in range(To):
                h.append(h0[j])
        for j in range(k,2*k):
            for t in range(Ts):
                h.append(h0[j])

        # now set up the optimization
        A1 = matrix(0.0,(k*2,T*k)) # ensures right amount of energy provided
        A2 = matrix(0.0,(k*2,T*k)) # ensures vehicle only charges when avaliable

        # new idea for the decision variable:
        # first k*Ts variables represent the day 1 vehicles first 24 hours
        # the next 2*k*To variables represent the fleet during the overlap time
        # the final k*Ts variables represent the day 2 vehicles at the horizon
        
        # I GOT TO HERE
        # day 1 
        for j in range(k):
            for t in range(Ts):
                A1[j,j*Ts+t] = 1.0/pointsPerHour
                if t < centroid[0][j][0] or t > centroid[0][j][1]:
                    A2[j,j*Ts+t] = 1.0
                    
            for t in range(To):
                A1[j,k*Ts+j*To+t] = 1.0/pointsPerHour
                
                if t < centroid[0][j][0] or t > centroid[0][j][1]:
                    A2[j,k*Ts+j*To+t] = 1.0
        # day 2                    
        for j in range(k):
            for t in range(To):
                A1[j+k,j*To+t] = 1.0/pointsPerHour
                if t < centroid[1][j][0] or t > centroid[1][j][1]:
                    A2[j+k,j*To+t] = 1.0
            for t in range(Ts):
                A1[j+k,j*Ts+k*To+t] = 1.0/pointsPerHour
                if t < centroid[1][j][0] or t > centroid[1][j][1]:
                    A2[j+k,j*Ts+k*To+t] = 1.0

        b = matrix(b)
        A = sparse([A1,A2])

        G = sparse([spdiag([-1]*(T*k)),spdiag([1]*(T*k))])
        h = matrix([0.0]*(2*T*k)+h)

        q = [] # incorporates base load into the objective function
        for i in range(k):
            for t in range(Ts):
                q.append(baseLoad[t])
        for i in range(2*k):
            for t in range(Ts,T):
                q.append(baseLoad[t])
        for i in range(k):
            for t in range(Ts):
                q.append(baseLoad[T+t])
                
        q = matrix(q)

        P = matrix(0.0,(2*k*T,2*k*T))
        # day 1 solo
        for i in range(k):
            for j in range(k):
                for t in range(Ts):
                    P[i*Ts+t,j*Ts+t] = 1
        # overlap
        for i in range(2*k):
            for j in range(2*k):
                for t in range(To):
                    P[k*Ts+i*To+t,k*Ts+j*To+t] = 1

        # day 2 solo
        for i in range(k,2*k):
            for j in range(k,2*k):
                for t in range(Ts):
                    P[2*k*To+i*Ts+t,2*k*To+j*Ts+t] = 1

        print(A.size)
        print(b.size)
        print(G.size)
        print(h.size)
        print(P.size)
        print(q.size)
        
        sol = solvers.qp(P,q,G,h,A,b) # solve quadratic program
        X = sol['x']

        profiles = []

        for i in range(k):
            profiles.append([0.0]*T)
            for t in range(Ts):
                profiles[i][t] = X[i*Ts+t]
            for t in range(Ts,T):
                profiles[i][t] = X[k*Ts+i*To+t]
                
        for i in range(k,2*k):
            profiles.append([0.0]*T)
            for t in range(To):
                profiles[i][t] = X[k*Ts+i*To+t]
            for t in range(To,T):
                profiles[i][t] = X[i*Ts+t+2*k*To]

        plt.figure(1)
        total = [0.0]*(T+Ts)
        for i in range(k*2):
            for t in range(T):
                if i < k:
                    total[t] += profiles[i][t]
                else:
                    total[t+Ts] += profiles[i][t]
                    
        plt.plot(total)
        # now individually apply chosen profiles

        total = [0.0]*T
        if storeIndividuals == True:
            self.individuals = {}

        for i in range(len(label)):
            vehicle = v[i]
            [a,d] = data[i]
            cluster = label[i]
            kWh = self.energy[vehicle]

            # copy standard cluster profile
            p = copy.copy(profiles[cluster])
            
            # set individual vehicle avaliability 
            for i in range(a):
                p[i] = 0
            for i in range(d+1440,T):
                p[i] = 0

            if sum(p) == 0:
                print(a)
                print(d)

            # scale to the right energy
            sf = kWh*60/sum(p)
            for i in range(T):
                p[i] = p[i]*sf
                if p[i] > pMax:
                    p[i] = pMax

            if storeIndividuals == True:
                self.inidividuals[vehicle] = p

            for i in range(T):
                total[i] += p[i]*self.sf[self.vehicleRType[vehicle]]

        plt.plot(total)
        plt.show()

            
                           
class TwoDayEnergyPrediction:
    def __init__(self,startDay,month,regionType,population,car=None,
                 smoothTimes=False):
        self.day1 = EnergyPrediction(startDay,month,regionType,population)
        self.day2 = EnergyPrediction(nextDay[startDay],month,regionType,
                                     population)
        
    def getDumbCharging(self,power,nHours=60,allowOverCap=False,units='k'):

        total = [0.0]*nHours*60

        dumb1 = self.day1.getDumbCharging(power,36,allowOverCap=allowOverCap,
                                          units=units)
        dumb2 = self.day2.getDumbCharging(power,36,allowOverCap=allowOverCap,
                                          units=units)

        for i in range(len(dumb1)):
            total[i] += dumb1[i]

            if i+1440 < nHours*60:
                total[i+1440] += dumb2[i]

        return total

    def getOptimalLoadFlatteningProfile(self,pMax,nHours=60):

        base1 = None
        base2 = None

        smart1 = sellf.day1.getOptimalLoadFlatteningProfile(self,base1,
                                                            pMax=pMax,nHours=36,
                                                            pointsPerHour=60,
                                                            deadline=None,
                                                            storeIndividuals=False)
        return ''
        
class NationalEnergyPrediction(EnergyPrediction):

    def __init__(self,day,month,car=None,smoothTimes=False,yearsLower=2002):
        EnergyPrediction.__init__(self,day,month,[0.369,0.446,0.092,0.093],
                                  65640000,car=car,smoothTimes=smoothTimes,
                                  yearsLower=yearsLower)

    def getOptimalLoadFlattening(self,pMax,pointsPerHour=60,
                                  deadline=12):
        self.baseload = getBaseLoad(self.day,self.month,48+deadline,unit='k',
                                    pointsPerHour=60)
        EnergyPrediction.getOptimalLoadFlatteningProfile(self,self.baseload,
                                                         pMax=pMax,
                                                         pointsPerHour=pointsPerHour,
                                                         deadline=deadline)
