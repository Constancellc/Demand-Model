8# packages
import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import sklearn.cluster as clst
import sys
from cvxopt import matrix, spdiag, solvers, sparse

# my code
sys.path.append('../')
from vehicleModel import Drivecycle, Vehicle
from fitDistributions import Inference

# This version is going to be more geared explicitly towards the national
# simiulation and journal paper - a two day simulation

# these are the csv files containing the data
trips = '../../Documents/UKDA-5340-tab/constance-trips.csv'
households = '../../Documents/UKDA-5340-tab/constance-households.csv'

nextDay = {'1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'1'}
units_scale = {'k':1,'M':1000,'G':1000000}

def getBaseLoad(day,month,nHours,unit='G',pointsPerHour=60,scale=1):
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
        interpolatedLoad[i] = interpolatedLoad[i]*1000*scale/units_scale[unit]

    return interpolatedLoad

def getBaseLoad2(day,month,nHours,unit='G',pointsPerHour=60,scale=1,
                 returnSingle=True):
    titles = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',
              9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    l = []
    m = []
    h = []

    nDays = int(nHours/24)+1
    while nDays > 0:
        with open('../ng-data/'+titles[int(month)]+str(day)+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                l.append(float(row[1])*1000000*scale/units_scale[unit])
                m.append(float(row[2])*1000000*scale/units_scale[unit])
                h.append(float(row[3])*1000000*scale/units_scale[unit])
        day = nextDay[day]
        nDays -= 1
    
    interpolatedL = [0.0]*nHours*pointsPerHour
    interpolatedM = [0.0]*nHours*pointsPerHour
    interpolatedH = [0.0]*nHours*pointsPerHour
    for i in range(0,len(interpolatedL)):
        p1 = int(12*i/pointsPerHour)
        p2 = p1+1

        f2 = 12*float(i)/pointsPerHour - p1
        f1 = 1.0-f2

        interpolatedL[i] = f1*l[p1]+f2*l[p2]
        interpolatedM[i] = f1*m[p1]+f2*m[p2]
        interpolatedH[i] = f1*h[p1]+f2*h[p2]

    if returnSingle == True:
        return interpolatedM
    else:
        return [interpolatedL,interpolatedM,interpolatedH]

        
class EnergyPrediction:

    def __init__(self,day,month,regionType,population,car=None,region=None,
                 smoothTimes=False,yearsLower=2002,recordVehicles=False):

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
            self.sf[i] = self.population*self.regionType[i]/\
                         (self.nPeople[i]*self.chargingEfficiency)

        self.energy = {}
        self.vehicleRType = {}
        self.startTimes = {}
        self.endTimes = {}
        if recordVehicles == True:
            self.vehicles = []
        
        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
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
                
                if recordVehicles == True:
                    if vehicle not in self.vehicles:
                        self.vehicles.append(vehicle)

                if row[6] != day and row[6] != nextDay[day]:
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

    def get_vehicle_requirements(self,nProfiles):
        self.removeOverCap()
        results = []
        if nProfiles < sum(self.nVehicles):
            nProfiles = sum(self.nVehicles)

        chosen = []
        while len(chosen) < nProfiles:
            ran = int(random.random()*len(self.vehicles))
            if ran not in chosen:
                vehicle = self.vehicles[ran]
                chosen.append(ran)
                try:
                    kWh = self.energy[vehicle][0]
                    d = self.startTimes[vehicle][1]
                    a = self.endTimes[vehicle][0]
                except:
                    kWh = 0.0
                    d = 0
                    a = 0
                results.append([kWh,d,a])

        return results

    
    def getDumbCharging(self,power,nHours=60,allowOverCap=False,units='k'):
        profile = [0.0]*nHours*60

        if allowOverCap == False:
            self.removeOverCap()

        for vehicle in self.energy:
            for day in range(2):
                kWh = self.energy[vehicle][day]
                start = self.endTimes[vehicle][day]

                reqTime = int(60*kWh/power)+1

                if reqTime < 2:
                    continue

                for i in range(start+day*1440,start+reqTime+day*1440):
                    if i < 60*nHours:
                        profile[i] += power*self.sf[self.vehicleRType[vehicle]]\
                                      /units_scale[units]

        return profile

    def approximateApply(self,profile,vehicle,day,a,d,pMax,pointsPerHour):

        kWh = self.energy[vehicle][day]
        p = copy.copy(profile)

        # set individual vehicle avaliability
        for i in range(int(a)):
            p[i] = 0
        for i in range(int(d),len(p)):
            p[i] = 0

        if sum(p) == 0:
            return [0.0]*len(p)
        
        # scale to the right energy
        sf = kWh*pointsPerHour/sum(p)
        for i in range(len(p)):
            p[i] = p[i]*sf
            if p[i] > pMax:
                p[i] = pMax

        return p


    def getOptimalLoadFlatteningProfile(self,baseLoad,pMax=3.5,
                                        pointsPerHour=60,deadline=16,
                                        storeIndividuals=False):
        '''
        This function finds the optimal load flattening vehicle charging profile

        Vehicles are first clustered to reduce complexity, then a quadratic
        program is set up using avaliability from the cluster centroids.

        Finally the optimal profiles are adjusted to fit each individual
        vehicle in the cluster.
        '''

        # ok so in the new plan we cluster the two days seperately and optimise
        # considering them independantly

        # first cluster on arrival and departure times
        self.getNextDayStartTimes()

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
                if day == 0:
                    d = self.startTimes[vehicle][1]+1440
                else:
                    try:
                        d = self.nextDayStartTimes[vehicle]+1440
                    except:
                        d = 1440+deadline*60
                    
                if d > 1440+deadline*60:
                    d = 1440+deadline*60

                a = float(pointsPerHour*a/60)
                d = float(pointsPerHour*d/60)

                data[day].append([a,d])
                
        centroid = [[],[]]
        label = [[],[]]
        inertia = [[],[]]

        for day in range(2):
            centroid[day], label[day], inertia[day] = clst.k_means(data[day],k)

        # stack vehicles into units
        b = [0.0]*(2*k)
        h0 = [0.0]*(2*k)
        for day in range(2):
            for i in range(len(label[day])):
                vehicle = v[day][i]
                b[label[day][i]+day*k] += self.energy[vehicle][day]*\
                               self.sf[self.vehicleRType[vehicle]]
                h0[label[day][i]+day*k] += self.sf[self.vehicleRType[vehicle]]*pMax

        # Sometimes clusters are empty and this fucks things up, we need to
        # remove them from the optimization
        day1Skip = []
        day2Skip = []
        for i in range(k):
            if b[i] <= 0.1:
                day1Skip.append(i)
            if b[i+k] <= 0.1:
                day2Skip.append(i)
                
        b2 = []
        centroid2 = [[],[]]
        for i in range(k):
            if i not in day1Skip:
                b2.append(b[i])
                centroid2[0].append(centroid[0][i])
        for i in range(k):
            if i not in day2Skip:
                b2.append(b[i+k])
                centroid2[1].append(centroid[1][i])
        centroid[0] = np.array(centroid2[0])
        centroid[1] = np.array(centroid2[1])

        b = b2

        # updated number of vehicles in optimization
        v1 = k-len(day1Skip)
        v2 = k-len(day2Skip)
        nV = v1+v2
        print(nV)

        b += [0.0]*nV
        h = []
        for j in range(k):
            if j in day1Skip:
                continue
            for t in range(Ts):
                h.append(h0[j])
        for j in range(2*k):
            if j in day1Skip:
                continue
            if j-k in day2Skip:
                continue
            for t in range(To):
                h.append(h0[j])
        for j in range(k,2*k):
            if j-k in day2Skip:
                continue
            for t in range(Ts):
                h.append(h0[j])

        # now set up the optimization
        A1 = matrix(0.0,(nV,T*nV)) # ensures right amount of energy provided
        A2 = matrix(0.0,(nV,T*nV)) # ensures vehicle only charges when avaliable

        # new idea for the decision variable:
        # first k*Ts variables represent the day 1 vehicles first 24 hours
        # the next 2*k*To variables represent the fleet during the overlap time
        # the final k*Ts variables represent the day 2 vehicles at the horizon
        
        # day 1 
        for j in range(v1):
            for t in range(Ts):
                A1[j,j*Ts+t] = 1.0/pointsPerHour
                if t < centroid[0][j][0] or t > centroid[0][j][1]:
                    A2[j,j*Ts+t] = 1.0
                    
            for t in range(To):
                A1[j,v1*Ts+j*To+t] = 1.0/pointsPerHour
                
                if t+Ts < centroid[0][j][0] or t+Ts > centroid[0][j][1]:
                    A2[j,v1*Ts+j*To+t] = 1.0
        # day 2                    
        for j in range(v1,nV):
            for t in range(To):
                A1[j,v1*Ts+j*To+t] = 1.0/pointsPerHour
                if t < centroid[1][j-v1][0] or t > centroid[1][j-v1][1]:
                    A2[j,v1*Ts+j*To+t] = 1.0
            for t in range(Ts):
                A1[j,j*Ts+nV*To+t] = 1.0/pointsPerHour
                if t+To < centroid[1][j-v1][0] or t+To > centroid[1][j-v1][1]:
                    A2[j,j*Ts+nV*To+t] = 1.0

        b = matrix(b)
        A = sparse([A1,A2])

        G = sparse([spdiag([-1]*(T*nV)),spdiag([1]*(T*nV))])
        h = matrix([0.0]*(T*nV)+h)

        q = [] # incorporates base load into the objective function
        for i in range(v1):
            for t in range(Ts):
                q.append(baseLoad[int(t*60/pointsPerHour)])
        for i in range(nV):
            for t in range(Ts,T):
                q.append(baseLoad[int(t*60/pointsPerHour)])
        for i in range(v2):
            for t in range(Ts):
                q.append(baseLoad[int((t+T)*60/pointsPerHour)])
                
        q = matrix(q)

        P = matrix(0.0,(nV*T,nV*T))
        # day 1 solo
        for i in range(v1):
            for j in range(v1):
                for t in range(Ts):
                    P[i*Ts+t,j*Ts+t] = 1
        # overlap
        for i in range(nV):
            for j in range(nV):
                for t in range(To):
                    P[v1*Ts+i*To+t,v1*Ts+j*To+t] = 1

        # day 2 solo
        for i in range(v1,nV):
            for j in range(v1,nV):
                for t in range(Ts):
                    P[nV*To+i*Ts+t,nV*To+j*Ts+t] = 1
        
        sol = solvers.qp(P,q,G,h,A,b) # solve quadratic program
        X = sol['x']

        profiles = []
        j = 0
        for i in range(k):
            profiles.append([0.0]*T)
            if i in day1Skip:
                continue
            for t in range(Ts):
                profiles[i][t] = X[j*Ts+t]
            for t in range(To):
                profiles[i][t+Ts] = X[v1*Ts+j*To+t]
            j += 1
            
        for i in range(k,2*k):
            profiles.append([0.0]*T)
            if i-k in day2Skip:
                continue
            for t in range(To):
                profiles[i][t] = X[v1*Ts+j*To+t]
            for t in range(Ts):
                profiles[i][t+To] = X[j*Ts+t+nV*To]
            j += 1
            
        total = [0.0]*(T+Ts)
        for i in range(2*k):
            for t in range(T):
                if i < k:
                    total[t] += profiles[i][t]
                else:
                    total[t+Ts] += profiles[i][t]
                    
        ideal = total

        # now individually apply chosen profiles

        total = [0.0]*(T+Ts)
        if storeIndividuals == True:
            self.individuals = {}

        for day in range(2):
            for i in range(len(label[day])):
                vehicle = v[day][i]
                [a,d] = data[day][i][:2]
                cluster = label[day][i]
                
                if storeIndividuals == True:
                    if vehicle not in self.individuals:
                        self.individuals[vehicle] = {}

                # copy standard cluster profile
                p = copy.copy(profiles[cluster+k*day])

                p = self.approximateApply(p,vehicle,day,a,d,pMax,
                                          pointsPerHour)

                if storeIndividuals == True:
                    self.inidividuals[vehicle][day] = p

                for i in range(T):
                    total[i+day*Ts] += p[i]*self.sf[self.vehicleRType[vehicle]]

        return [ideal,total]

    def getApproximateLoadFlatteningProfile(self,baseLoad,pMax,deadline=16,
                                            storeIndividuals=False):

        total = [0.0]*len(baseLoad)

        if storeIndividuals == True:
            self.individuals = {}

        # get inverse shape
        ibase = [0.0]*len(baseLoad)
        for i in range(len(baseLoad)):
            ibase[i] = max(baseLoad)+0.01-baseLoad[i]
            
        for vehicle in self.energy:
            for day in range(2):
                if self.energy[vehicle][day] == 0.0:
                    continue

                a = self.endTimes[vehicle][day]+day*1440
                if day == 0:
                    d = self.startTimes[vehicle][1]+1440
                else:
                    try:
                        d = self.nextDayStartTimes[vehicle]+1440*2
                    except:
                        d = 1440*2+deadline*60

                if a > d: # hack, shouldn't happen often
                    d += 1440
                    
                if d > 1440*(day+1)+deadline*60:
                    d = 1440*(day+1)+deadline*60
                    
                p = copy.copy(ibase)
                p = self.approximateApply(p,vehicle,day,a,d,pMax,
                                          60)
                
                if storeIndividuals == True:
                    if vehicle in self.individuals:
                        for t in range(len(p)):
                            self.individuals[vehicle][t] += p[t]
                    else:
                        self.individuals[vehicle] = p

                for i in range(len(p)):
                    total[i] += p[i]*self.sf[self.vehicleRType[vehicle]]

        return total

    def getStochasticOptimalLoadFlatteningProfile4(self,baseLoads,thresholds,
                                                   pDist,pMax=7.0,
                                                   pointsPerHour=60,
                                                   deadline=16):
        
        '''
        FUCK. This is going to be variation in both. God help me.

        pDist should be a matrix not a vector, its elements should sum to 1

        baseLoads should be a vector

        so should thresholds

        
        '''
        nB = len(baseLoads)
        nT = len(thresholds)
        nS = int(nB*nT)

        # chek that pDist is a valid pdf
        if len(pDist) != nB or len(pDist[0]) != nT:
            raise Exception('pDist must be '+str(nB)+' x '+str(nT))
        total = 0
        for i in range(nB):
            for j in range(nT):
                total += pDist[i][j]
        if total != 1:
            raise Exception('pDist must sum to 1 not '+str(total))

        # ok so in the new plan we cluster the two days seperately and optimise
        # considering them independantly

        # first cluster on arrival and departure times
        self.getNextDayStartTimes()

        k = 3 # number of clusters
        nV = k*nS*2
        
        T = (24+deadline)*pointsPerHour
        To = deadline*pointsPerHour # overlap time
        Ts = 24*pointsPerHour

        data = []
        v = []
        label = []
        centroid = []

        b = [0.0]*(k*2*nT)
        h0 = [0.0]*(k*2*nT)
        
        for s in range(nT):
            data.append([[],[]])
            v.append([[],[]])
            label.append([[],[]])
            centroid.append([[],[]])

        for s in range(nT):
            threshold_energy = thresholds[s]
            for vehicle in self.energy:
                for day in range(2):
                    if self.energy[vehicle][day] == 0.0:
                        continue

                    if self.energy[vehicle][day] < threshold_energy:
                        nDays = int(threshold_energy/self.energy[vehicle][day])+1
                        if random.random() > 1/float(nDays):
                            continue

                    v[s][day].append(vehicle)

                    a = self.endTimes[vehicle][day]
                    if day == 0:
                        d = self.startTimes[vehicle][1]+1440
                    else:
                        try:
                            d = self.nextDayStartTimes[vehicle]+1440
                        except:
                            d = 1440+deadline*60
                        
                    if d > 1440+deadline*60:
                        d = 1440+deadline*60

                    a = float(pointsPerHour*a/60)
                    d = float(pointsPerHour*d/60)

                    data[s][day].append([a,d])
                
        for s in range(nT):
            for day in range(2):
                centroid[s][day], label[s][day], inertia = clst.k_means(data[s][day],k)
                for i in range(k):
                    for j in range(len(label[s][day])):
                        if label[s][day][j] != i:
                            continue
                        vehicle = v[s][day][j]
                        en = self.energy[vehicle][day]

                        if en < thresholds[s]:
                            en = en*(int(thresholds[s]/en)+1)
                        elif en >= 60:
                            en = 60
                            
                        b[s*2*k+day*k+i] += en*self.sf[self.vehicleRType[vehicle]]
                        h0[s*2*k+day*k+i] += pMax*self.sf[self.vehicleRType[vehicle]]
        
        # now set up the optimization 
        b = b*nB                  
        b += [0.0]*len(b)
        
        h = [0.0]*(nV*T)
        
        A1 = matrix(0.0,(nV,T*nV)) # ensures right amount of energy provided
        A2 = matrix(0.0,(nV,T*nV)) # ensures vehicle only charges when avaliable

        # for scenario
        for si in range(nB):
            for sj in range(nT):
                s = int(si*nT+sj)
                # day 1
                for j in range(k):
                    for t in range(Ts):
                        h[(2*k*s*T)+j*Ts+t] = h0[sj*2*k+j]
                        A1[(2*k*s)+j,(2*k*s*T)+j*Ts+t] = 1.0/pointsPerHour
                        if t < centroid[sj][0][j][0] or t > centroid[sj][0][j][1]:
                            A2[(2*k*s)+j,(2*k*T*s)+j*Ts+t] = 1.0
                            
                    for t in range(To):
                        h[(2*k*T*s)+k*Ts+j*To+t] = h0[sj*2*k+j]
                        A1[(2*k*s)+j,(2*k*T*s)+k*Ts+j*To+t] = 1.0/pointsPerHour
                        if t+Ts < centroid[sj][0][j][0] or t+Ts > centroid[sj][0][j][1]:
                            A2[(2*k*s)+j,(2*k*T*s)+k*Ts+j*To+t] = 1.0
                # day 2                    
                for j in range(k,2*k):
                    for t in range(To):
                        h[(2*k*T*s)+k*Ts+j*To+t] = h0[sj*2*k+j]
                        A1[(2*k*s)+j,(2*k*T*s)+k*Ts+j*To+t] = 1.0/pointsPerHour
                        if t < centroid[sj][1][j-k][0] or t > centroid[sj][1][j-k][1]:
                            A2[(2*k*s)+j,(2*T*k*s)+k*Ts+j*To+t] = 1.0
                            
                    for t in range(Ts):
                        h[(2*k*T*s)+j*Ts+2*k*To+t] = h0[sj*2*k+j]
                        A1[(2*k*s)+j,(2*k*T*s)+j*Ts+2*k*To+t] = 1.0/pointsPerHour
                        if t+To < centroid[sj][1][j-k][0] or t+To > centroid[sj][1][j-k][1]:
                            A2[(2*k*s)+j,(2*k*T*s)+j*Ts+2*k*To+t] = 1.0

        b = matrix(b)
        A = sparse([A1,A2])
        G = sparse([spdiag([-1]*(T*nV)),spdiag([1]*(T*nV))])
        h = matrix([0.0]*(T*nV)+h)

        q = [] # incorporates base load into the objective function
        for si in range(nB):
            for sj in range(nT):
                #s = int(si*nT+sj)
                for i in range(k):
                    for t in range(Ts):
                        q.append(pDist[si][sj]*baseLoads[si][int(t*60/pointsPerHour)])
                for i in range(2*k):
                    for t in range(Ts,T):
                        q.append(pDist[si][sj]*baseLoads[si][int(t*60/pointsPerHour)])
                for i in range(k):
                    for t in range(Ts):
                        q.append(pDist[si][sj]*baseLoads[si][int((t+T)*60/pointsPerHour)])
                    
        q = matrix(q)
        P = matrix(0.0,(nV*T,nV*T))
        
        # for each scenario
        for si in range(nB):
            for sj in range(nT):
                s = int(si*nT+sj)
                # day 1 solo
                for i in range(k):
                    for j in range(k):
                        for t in range(Ts):
                            P[(2*k*s*T)+i*Ts+t,(2*k*s*T)+j*Ts+t] = pDist[si][sj]
                # overlap
                for i in range(2*k):
                    for j in range(2*k):
                        for t in range(To):
                            P[(2*k*s*T)+k*Ts+i*To+t,(2*k*s*T)+k*Ts+j*To+t] = pDist[si][sj]

                # day 2 solo
                for i in range(k,2*k):
                    for j in range(k,2*k):
                        for t in range(Ts):
                            P[(2*k*s*T)+2*k*To+i*Ts+t,(2*k*s*T)+2*k*To+j*Ts+t] = pDist[si][sj]
            
        sol = solvers.qp(P,q,G,h,A,b) # solve quadratic program
        X = sol['x']

        profiles = []
        for s in range(nS):
            profiles.append([])
            for i in range(k):
                profiles[s].append([0.0]*T)
                for t in range(Ts):
                    profiles[s][i][t] = X[(2*k*s*T)+i*Ts+t]
                for t in range(To):
                    profiles[s][i][t+Ts] = X[(2*k*T*s)+k*Ts+i*To+t]

            for i in range(k,2*k):
                profiles[s].append([0.0]*T)
                for t in range(To):
                    profiles[s][i][t] = X[(2*T*k*s)+k*Ts+i*To+t]
                for t in range(Ts):
                    profiles[s][i][t+To] = X[(2*T*k*s)+i*Ts+t+2*k*To]

        totals = []

        for s in range(nS):
            totals.append([0.0]*(T+Ts))
            for i in range(2*k):
                for t in range(T):
                    if i < k:
                        totals[s][t] += profiles[s][i][t]
                    else:
                        totals[s][t+Ts] += profiles[s][i][t]
        base = []
        for s in range(nB):
            base.append([])
        for t in range(T+Ts):
            for si in range(nB):
                base[si].append(baseLoads[si][int(t*60/pointsPerHour)])
                for sj in range(nT):
                    s = int(si*nT+sj)
                    totals[s][t] += baseLoads[si][int(t*60/pointsPerHour)]
                                 
        ideal = totals

        # now individually apply chosen profiles
        totals = []
        for s in range(nS):
            totals.append([0.0]*(Ts+T))
        for sj in range(nT):
            for day in range(2):
                for i in range(k):
                    for j in range(len(label[sj][day])):
                        if label[sj][day][j] != i:
                            continue
                        vehicle = v[sj][day][j]
                        en = self.energy[vehicle][day]

                        if en < thresholds[sj]:
                            en = en*(int(thresholds[sj]/en)+1)
                        elif en >= 60:
                            en = 60

                        en = en*self.sf[self.vehicleRType[vehicle]]

                        [a,d] = data[sj][day][j]

                        for si in range(nB):
                            s = int(si*nT+sj)
                            p = copy.copy(profiles[s][i+k*day])

                            for t in range(int(a)):
                                p[t] = 0.0
                            for t in range(int(d),T):
                                p[t] = 0.0

                            if sum(p) == 0:
                                continue

                            sf = en*pointsPerHour/sum(p)
                            for t in range(T):
                                p[t] = p[t]*sf
                                totals[s][t+Ts*day] += p[t]                            

        for si in range(nB):
            for sj in range(nT):
                s = int(si*nT+sj)
                for t in range(T+Ts):
                    totals[s][t] += baseLoads[si][int(t*60/pointsPerHour)]

        return [ideal, totals, base]
        '''
        return totals
        '''

    def getStochasticOptimalLoadFlatteningProfile(self,baseLoads,thresholds,
                                                  bDist,tDist,pMax=7.0,
                                                  pointsPerHour=60,deadline=16):
        
        '''
        DEAR GOD. OKAY. single stage baseload, multistage charging.

        I'm going to assume independance. 
        
        '''
        nB = len(baseLoads)
        nT = len(thresholds)
        nS = int(nB*nT)

        # chek that distributions are valid pdfs
        if len(bDist) != nB or len(tDist) != nT:
            raise Exception('bDist must be '+str(nB)+' long and tDist muct be'+
                            str(nT)+' long.')
        total = 0
        for i in range(nB):
            total += bDist[i]
        if total != 1:
            raise Exception('bDist must sum to 1 not '+str(total))
        
        total = 0
        for i in range(nT):
            total += tDist[i]
        if total != 1:
            raise Exception('tDist must sum to 1 not '+str(total))

        # ok so in the new plan we cluster the two days seperately and optimise
        # considering them independantly

        # first cluster on arrival and departure times
        self.getNextDayStartTimes()

        k = 3 # number of clusters
        nV = k*nT*2
        
        T = (24+deadline)*pointsPerHour
        To = deadline*pointsPerHour # overlap time
        Ts = 24*pointsPerHour

        data = []
        v = []
        label = []
        centroid = []

        b = [0.0]*(k*2*nT)
        h0 = [0.0]*(k*2*nT)
        
        for s in range(nT):
            data.append([[],[]])
            v.append([[],[]])
            label.append([[],[]])
            centroid.append([[],[]])

        for s in range(nT):
            threshold_energy = thresholds[s]
            for vehicle in self.energy:
                for day in range(2):
                    if self.energy[vehicle][day] == 0.0:
                        continue

                    if self.energy[vehicle][day] < threshold_energy:
                        nDays = int(threshold_energy/self.energy[vehicle][day])+1
                        if random.random() > 1/float(nDays):
                            continue

                    v[s][day].append(vehicle)

                    a = self.endTimes[vehicle][day]
                    if day == 0:
                        d = self.startTimes[vehicle][1]+1440
                    else:
                        try:
                            d = self.nextDayStartTimes[vehicle]+1440
                        except:
                            d = 1440+deadline*60
                        
                    if d > 1440+deadline*60:
                        d = 1440+deadline*60

                    a = float(pointsPerHour*a/60)
                    d = float(pointsPerHour*d/60)

                    data[s][day].append([a,d])
                
        for s in range(nT):
            for day in range(2):
                centroid[s][day], label[s][day], inertia = clst.k_means(data[s][day],k)
                for i in range(k):
                    for j in range(len(label[s][day])):
                        if label[s][day][j] != i:
                            continue
                        vehicle = v[s][day][j]
                        en = self.energy[vehicle][day]

                        if en < thresholds[s]:
                            en = en*(int(thresholds[s]/en)+1)
                        elif en >= 60:
                            en = 60
                            
                        b[s*2*k+day*k+i] += en*self.sf[self.vehicleRType[vehicle]]
                        h0[s*2*k+day*k+i] += pMax*self.sf[self.vehicleRType[vehicle]]
        
        # now set up the optimization 
        #b = b*nB                  
        b += [0.0]*len(b)
        
        h = [0.0]*(nV*T)
        
        A1 = matrix(0.0,(nV,T*nV)) # ensures right amount of energy provided
        A2 = matrix(0.0,(nV,T*nV)) # ensures vehicle only charges when avaliable

        # for scenario
        for s in range(nT):
            # day 1
            for j in range(k):
                for t in range(Ts):
                    h[(2*k*s*T)+j*Ts+t] = h0[s*2*k+j]
                    A1[(2*k*s)+j,(2*k*s*T)+j*Ts+t] = 1.0/pointsPerHour
                    if t < centroid[s][0][j][0] or t > centroid[s][0][j][1]:
                        A2[(2*k*s)+j,(2*k*T*s)+j*Ts+t] = 1.0
                            
                for t in range(To):
                    h[(2*k*T*s)+k*Ts+j*To+t] = h0[s*2*k+j]
                    A1[(2*k*s)+j,(2*k*T*s)+k*Ts+j*To+t] = 1.0/pointsPerHour
                    if t+Ts < centroid[s][0][j][0] or t+Ts > centroid[s][0][j][1]:
                        A2[(2*k*s)+j,(2*k*T*s)+k*Ts+j*To+t] = 1.0
            # day 2
            for j in range(k,2*k):
                for t in range(To):
                    h[(2*k*T*s)+k*Ts+j*To+t] = h0[s*2*k+j]
                    A1[(2*k*s)+j,(2*k*T*s)+k*Ts+j*To+t] = 1.0/pointsPerHour
                    if t < centroid[s][1][j-k][0] or t > centroid[s][1][j-k][1]:
                        A2[(2*k*s)+j,(2*T*k*s)+k*Ts+j*To+t] = 1.0
                            
                for t in range(Ts):
                    h[(2*k*T*s)+j*Ts+2*k*To+t] = h0[s*2*k+j]
                    A1[(2*k*s)+j,(2*k*T*s)+j*Ts+2*k*To+t] = 1.0/pointsPerHour
                    if t+To < centroid[s][1][j-k][0] or t+To > centroid[s][1][j-k][1]:
                        A2[(2*k*s)+j,(2*k*T*s)+j*Ts+2*k*To+t] = 1.0


        b = matrix(b)
        A = sparse([A1,A2])
        G = sparse([spdiag([-1]*(T*nV)),spdiag([1]*(T*nV))])
        h = matrix([0.0]*(T*nV)+h)
        
        q0 = [0.0]*(2*k*T)
        for s in range(nB):
            for i in range(k):
                for t in range(Ts):
                    q0[i*Ts+t] += baseLoads[s][int(t*60/pointsPerHour)]*bDist[s]
                for t in range(To):
                    q0[k*Ts+i*To+t] += baseLoads[s][\
                        int((t+Ts)*60/pointsPerHour)]*bDist[s]
            for i in range(k,2*k):
                for t in range(To):
                    q0[k*Ts+i*To+t] += baseLoads[s][\
                        int((t+Ts)*60/pointsPerHour)]*bDist[s]
                for t in range(Ts):
                    q0[i*Ts+2*k*To+t] += baseLoads[s][\
                        int((t+T)*60/pointsPerHour)]*bDist[s]
        q = []
        for s in range(nT):
            for i in range(len(q0)):
                q.append(q0[i]*tDist[s])

        '''

        q = [] # incorporates base load into the objective function

        q = [0.0]*(nV*T)
        for si in range(nT):
            for sj in range(nB):
                for i in range(k):
                    for t in range(Ts):
                        q[(si*2*k*T)+i*Ts+t] += baseLoads[sj][\
                            int(t*60/pointsPerHour)]*bDist[sj]*tDist[si]

                    for t in range(To):
                        q[(2*k*T*si)+k*Ts+i*To+t] += baseLoads[sj][\
                            int((t+Ts)*60/pointsPerHour)]*bDist[sj]*tDist[si]
                        
                for i in range(k,2*k):
                    for t in range(To):
                        q[(2*k*T*si)+k*Ts+i*To+t] += baseLoads[sj][\
                            int((t+Ts)*60/pointsPerHour)]*bDist[sj]*tDist[si]
                        
                    for t in range(Ts):
                        q[(2*k*T*si)+i*Ts+2*k*To+t] += baseLoads[sj][\
                            int((t+T)*60/pointsPerHour)]*bDist[sj]*tDist[si]
        '''

        q = matrix(q)
        P = matrix(0.0,(nV*T,nV*T))
        
        # for each scenario
        for si in range(nB):
            for sj in range(nT):
                # day 1 solo
                for i in range(k):
                    for j in range(k):
                        for t in range(Ts):
                            P[(2*k*sj*T)+i*Ts+t,
                              (2*k*sj*T)+j*Ts+t] = tDist[sj]
                # overlap
                for i in range(2*k):
                    for j in range(2*k):
                        for t in range(To):
                            P[(2*k*sj*T)+k*Ts+i*To+t,
                              (2*k*sj*T)+k*Ts+j*To+t] = tDist[sj]

                # day 2 solo
                for i in range(k,2*k):
                    for j in range(k,2*k):
                        for t in range(Ts):
                            P[(2*k*sj*T)+2*k*To+i*Ts+t,
                              (2*k*sj*T)+2*k*To+j*Ts+t] = tDist[sj]
            
        sol = solvers.qp(P,q,G,h,A,b) # solve quadratic program
        X = sol['x']

        profiles = []
        for s in range(nT):
            profiles.append([])
            for i in range(k):
                profiles[s].append([0.0]*T)
                for t in range(Ts):
                    profiles[s][i][t] = X[(2*k*s*T)+i*Ts+t]
                for t in range(To):
                    profiles[s][i][t+Ts] = X[(2*k*T*s)+k*Ts+i*To+t]

            for i in range(k,2*k):
                profiles[s].append([0.0]*T)
                for t in range(To):
                    profiles[s][i][t] = X[(2*T*k*s)+k*Ts+i*To+t]
                for t in range(Ts):
                    profiles[s][i][t+To] = X[(2*T*k*s)+i*Ts+t+2*k*To]

        totals = []

        for s in range(nS):
            totals.append([0.0]*(T+Ts))
            for i in range(2*k):
                for t in range(T):
                    if i < k:
                        totals[s][t] += profiles[int(s/nB)][i][t]
                    else:
                        totals[s][t+Ts] += profiles[int(s/nB)][i][t]
        base = []
        for s in range(nB):
            base.append([])
        for t in range(T+Ts):
            for si in range(nB):
                base[si].append(baseLoads[si][int(t*60/pointsPerHour)])
                for sj in range(nT):
                    s = int(sj*nB+si)
                    totals[s][t] += baseLoads[si][int(t*60/pointsPerHour)]
                                 
        ideal = totals

        # now individually apply chosen profiles
        totals = []
        for s in range(nS):
            totals.append([0.0]*(Ts+T))
        for sj in range(nT):
            for day in range(2):
                for i in range(k):
                    for j in range(len(label[sj][day])):
                        if label[sj][day][j] != i:
                            continue
                        vehicle = v[sj][day][j]
                        en = self.energy[vehicle][day]

                        if en < thresholds[sj]:
                            en = en*(int(thresholds[sj]/en)+1)
                        elif en >= 60:
                            en = 60

                        en = en*self.sf[self.vehicleRType[vehicle]]

                        [a,d] = data[sj][day][j]
                        
                        p = copy.copy(profiles[sj][i+k*day])

                        for t in range(int(a)):
                            p[t] = 0.0
                        for t in range(int(d),T):
                            p[t] = 0.0

                        if sum(p) == 0:
                            continue

                        sf = en*pointsPerHour/sum(p)
                        for t in range(T):
                            p[t] = p[t]*sf
                            for si in range(nB):
                                s = int(si*nT+sj)
                                totals[s][t+Ts*day] += p[t]                            

        for si in range(nB):
            for sj in range(nT):
                s = int(si*nT+sj)
                for t in range(T+Ts):
                    totals[s][t] += baseLoads[si][int(t*60/pointsPerHour)]

        return [ideal, totals, base]
        '''
        return totals
        '''


    def testDemandTurnUp(self,pMax,baseLoad,upTime):

        upTime = upTime+1440 # assume we are considering day two of simulation
        
        approx = self.getApproximateLoadFlatteningProfile(baseLoad,
                                                          pMax,
                                                          storeIndividuals=True)
        total = [0.0]*len(approx)
        for i in range(upTime):
            total[i] = approx[i]
            
        for vehicle in self.individuals:
            p = self.individuals[vehicle][upTime:]
            i = 0
            while p[i] == 0 and i < len(p)-1:
                i += 1
            start = i
            while p[i] > 0 and i < len(p)-1:
                i += 1
            #end = i
            end = len(p)
            
            if sum(p[start:end]) > 0.1:
                tot = 0
                for t in range(start,end):
                    tot += p[t]
                    p[t] = 0

                for t in range(start,int(start+tot/pMax)):
                    if t < len(p):
                        p[t] = pMax

            for i in range(len(p)):
                total[upTime+i] += p[i]*self.sf[self.vehicleRType[vehicle]]

        return [approx,total]
        
            
         
class NationalEnergyPrediction(EnergyPrediction):

    def __init__(self,day,month,deadline=16,car='teslaS60D',smoothTimes=True,
                 yearsLower=2002):
        EnergyPrediction.__init__(self,day,month,[0.369,0.446,0.092,0.093],
                                  65640000,car=car,smoothTimes=smoothTimes,
                                  yearsLower=yearsLower)

        self.baseLoad = getBaseLoad2(self.day,self.month,48+deadline,unit='k',
                                pointsPerHour=60,returnSingle=True)

    def getOptimalLoadFlattening(self,pMax,pointsPerHour=10,deadline=16):
        [ideal,total] = EnergyPrediction.getOptimalLoadFlatteningProfile(self,
                        self.baseLoad,pMax=pMax,pointsPerHour=pointsPerHour,
                        deadline=deadline)
        
        return [ideal,total]
    
    
    def getStochasticOptimalLoadFlatteningProfile(self,deadline=16,pointsPerHour=6):

        baseLoads = getBaseLoad2(self.day,self.month,48+deadline,unit='k',
                                pointsPerHour=60,returnSingle=False)

        thresholds = thresholds = [54.2,46.4,31.4,14.8,7.6]#[27.1,23.2,15.7,7.4,3.8]
        tDist = [0.05,0.2,0.5,0.2,0.05]
        
        bDist = [0.25,0.5,0.25]

        x = EnergyPrediction.getStochasticOptimalLoadFlatteningProfile(self,
                                                                       baseLoads,
                                                                       thresholds,
                                                                       bDist,
                                                                       tDist,
                                                                       pointsPerHour=pointsPerHour)
        return x

    def getApproximateLoadFlattening(self,deadline=16,storeIndividuals=False):
        total = EnergyPrediction.getApproximateLoadFlatteningProfile(self,
                self.baseLoad,7,deadline=deadline,storeIndividuals=storeIndividuals)

        return total

class CornwallEnergyPrediction(EnergyPrediction):

    def __init__(self,day,month,deadline=16,car='teslaS60D',smoothTimes=True,
                 yearsLower=2002,solar=False):
        EnergyPrediction.__init__(self,day,month,[0.0,0.386,0.274,0.340],
                                  532273,car=car,smoothTimes=smoothTimes,
                                  region='9',yearsLower=yearsLower)
        self.solar = solar

        self.baseLoad = getBaseLoad2(self.day,self.month,48+deadline,unit='k',
                                     pointsPerHour=60,returnSingle=True,
                                     scale=1349.8/116997.9)
        if solar == True:
            ms = {'1':'jan','2':'feb','3':'mar','4':'apr','5':'may','6':'jun',
                  '7':'jul','8':'aug','9':'sep','10':'oct','11':'nov','12':'dec'}
            self.allProfiles = [] 
            with open('../../Documents/cornwall-pv-predictions/av-'+ms[month]+
                      '-net.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.allProfiles.append(row)
                    
            t_int = 30 # data half hourly

            for j in range(len(self.allProfiles)):
                profile = self.allProfiles[j]
                # repeat profile as necessary
                profile = profile*3

                new = [0.0]*len(self.baseLoad)
                # interpolate and remove from base load
                for i in range(len(self.baseLoad)):
                    p = int(i/t_int)
                    if i % t_int == 0:
                        new[i] = float(profile[p])
                    else:
                        f = float(i%t_int)/t_int
                        new[i] = (1-f)*float(profile[p])+f*float(profile[p+1])

                self.allProfiles[j] = new

            self.baseLoad = self.allProfiles[2]
                

    def getOptimalLoadFlattening(self,pMax,pointsPerHour=10,deadline=16):
        [ideal,total] = EnergyPrediction.getOptimalLoadFlatteningProfile(self,
                        self.baseLoad,pMax=pMax,pointsPerHour=pointsPerHour,
                        deadline=deadline)
        
        return [ideal,total]
            
    def getStochasticOptimalLoadFlatteningProfile(self,deadline=16,solar=True,
                                                  pointsPerHour=6):
        if self.solar == False:
            baseLoads = getBaseLoad2(self.day,self.month,48+deadline,unit='k',
                                     pointsPerHour=60,returnSingle=False,
                                     scale=1349.8/116997.9)
            bDist = [0.25,0.5,0.25]
            
            thresholds = [54.2,46.4,31.4,14.8,7.6]
            tDist = [0.05,0.2,0.5,0.2,0.05]
        else:
            baseLoads = self.allProfiles
            bDist = [0.05,0.2,0.5,0.2,0.05]

            thresholds = [23.9,15.7,6.6]
            tDist = [0.25,0.5,0.25]

        x = EnergyPrediction.getStochasticOptimalLoadFlatteningProfile(self,
                                                                       baseLoads,
                                                                       thresholds,
                                                                       bDist,
                                                                       tDist,
                                                                       pointsPerHour=pointsPerHour)
        return x

