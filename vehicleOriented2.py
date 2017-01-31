# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# get the drivecycle class i wrote to run artemis for a given vehicle / distance
from vehicleModel import Drivecycle

# ------------------------------------------------------------------------------
# CLASS DEFINITIONS SECTION
# ------------------------------------------------------------------------------
class Vehicle:
    # Vehicle just stores the salient parameters of an individual agent
    def __init__(self,mass,Ta,Tb,Tc,eff,cap):
        self.mass = mass # kg
        self.load = 0 #kg
        self.Ta = Ta*4.44822 # convert lbf to N
        self.Tb = Tb*9.9503 # lbf/mph -> N/mps
        self.Tc = Tc*22.258 # lbf/mph2 -> N/(mps)^2 
        self.eff = eff
        self.capacity = cap # kWh

class JourneyPool:
    # Defines the 'pool' of randomly generated journeys in a given region
    def __init__(self, day, month, regionType):
        self.day = day
        self.month = month
        self.regionType = regionType
        
        self.journeys = {'Commute':[],'Education':[],'Business':[],
                         'Shopping':[],'Other escort + personal':[],
                         'Entertainment':[],'Other':[]}
        
    def addJourney(self):

        files = ['nts-data/purposeDay.csv','nts-data/purposeMonth.csv',
                 'nts-data/regionTypePurpose.csv']
        fixed = [self.day, self.month, self.regionType]
        
        out = []

        for j in range(0,3):
            # first, find the purpose given the regionType, or maybe day of week, or month... FUCK
            with open(files[j],'rU') as csvfile:
                reader = csv.reader(csvfile)
                variables = next(reader)
                for i in range(0,len(variables)):
                    if variables[i] == fixed[j]:
                        index = i

                if index is False:
                    raise Error('pdf problems')

                purposes = []
                pdf = []
                
                for row in reader:
                    if row == variables:
                        continue
                    else:
                        purposes.append(row[0])
                        pdf.append(row[index])
            sumPdf = 0

            for number in pdf:
               sumPdf += float(number)

            distribution = [0]*7

            for i in range(0,7):
               distribution[i] = float(pdf[i])/sumPdf

            out.append(distribution)

        purposeday = out[0]
        purposemonth = out[1]
        purposeregion = out[2]

        pdf = [0]*7

        for i in range(0,7):
            pdf[i] = purposeday[i]*purposemonth[i]*purposeregion[i]

        pdf[1] = 0.5*pdf[1] # Assume all education trips are round trips

        sumPdf = sum(pdf)

        # This should be the cdf of purpose given all of day, month and region
        cdf = [pdf[0]/sumPdf]

        for i in range(1,7):
            cdf.append(cdf[i-1]+pdf[i]/sumPdf)

        ran = random.random()

        j = 0

        while cdf[j] <= ran and j < 6:
            j += 1

        purpose = purposes[j]
       
        # we now have purpose, we now need time of day, ok this is where changes happen

        if purpose == 'Commute' or purpose == 'Education':
            with open('nts-data/purposeStartAMPM.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                pdf = []
                for row in reader:
                    if row[0] == (purpose+'AM'):
                        pdfAM = row[1:]
                    elif row[0] == (purpose+'PM'):
                        pdfPM = row[1:]

                # first get morning commmute
                ran = 0.5*random.random()
                i = 0
                c = float(pdfAM[0])
                while c <= ran:
                    i += 1
                    c += float(pdfAM[i])

                outStartHour = i

                ran = 0.5*random.random()
                i = 0
                c = float(pdfPM[0])
                while c <= ran:
                    i += 1
                    c += float(pdfPM[i])

                backStartHour = i
                
        else:
            with open('nts-data/purposeStartHour.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                pdf = []
                for row in reader:
                    if row[0] == purpose:
                        pdf = row[1:]

                times = []

                for j in range(0,2):
                    ran = random.random()
                    i = 0
                    c = float(pdf[0])
                    while c <= ran and i<23:
                        i += 1
                        c += float(pdf[i])

                    # hack for shifting time
                    if i > 3:
                        i -= 4
                    else:
                        i += 20
                    times.append(i)

                if times[0] < times[1]:
                    outStartHour = times[0]
                    backStartHour = times[1]

                else:
                    outStartHour = times[1]
                    backStartHour = times[0]



        with open('nts-data/regionTypePurposeLength.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            regions = next(reader)
            for i in range(0,len(regions)):
                if regions[i] == self.regionType:
                    regionIndex = i
                
            for row in reader:
                if row[0] == purpose:
                    # generate distance in miles
                    distance = np.random.normal(float(row[regionIndex]),1)

                    # assume all education journeys are round trips
                    if purpose == 'Education':
                        distance = distance*2

        if outStartHour == backStartHour:
            time1 = 0
            time2 = 0
            while (time1-time2)*(time1-time2) <= 400:
                time1 = outStartHour*60 + int(60*random.random())
                time2 = outStartHour*60 + int(60*random.random())

            if time1 < time2:
                outTime = time1
                backTime = time2
            else:
                outTime = time2
                backTime = time1

        else:        
            outTime = 60*outStartHour + int(60*random.random())
            backTime = 60*backStartHour + int(60*random.random())

        self.journeys[purpose].append([outTime,backTime,distance])


    def pickOutJourney(self):
        # ah shit, did we mean to do the commutes and education first?
        # first select the purpose
        purposes = ['Commute','Education','Business','Shopping',
                    'Other escort + personal','Entertainment','Other']
        
        pdf = []
        for key in purposes:
            pdf.append(len(self.journeys[key]))

        ran = random.random()*sum(pdf)

        c = pdf[0]
        i = 0
        while c <= ran:
            i += 1
            c += pdf[i]

        purpose = purposes[i]

        # now pick journey pair
        ran = int(len(self.journeys[purpose])*random.random())
        journey = self.journeys[purpose][ran]

        self.journeys[purpose].remove(journey)

        return [purpose,journey[0],journey[1],journey[2]]
    
class Agent:
    # This stores all of the agents dynamic parameters, unlike the 'vehicle'
    # class whose parameters do not change during the simulation
    def __init__(self, name, vehicle, regionType):
        self.name = name
        self.vehicle = vehicle
        self.regionType = regionType
        self.avaliability = [1]*(24*60)
        self.location = [0]*(24*60)
        self.journeysLog = []
        self.energyLog = []
        #self.mileage = 0
        self.battery = vehicle.capacity
        self.energySpent = [0]*(24*60)

    def addJourney(self,journey):
        purpose = journey[0]
        timeOut = journey[1]
        timeBack = journey[2]

        # hack to get around negative journey lengths - gaussian problems
        if journey[3] < 0:
            journey[3] = -journey[3]
        distance = journey[3]*1609.34 #convert from miles to m

        self.journeysLog.append(journey)

        #self.mileage += distance*2

        # calculate the energy expenditure
        if self.regionType[0] == 'U':
            cycle = Drivecycle(distance,'urban')
        elif self.regionType[0] == 'R':
            cycle = Drivecycle(distance,'rural')
        else:
            raise Exception('region not recognised')

        v = cycle.velocity # m/s
        a = cycle.acceleration # m/s2

        F = []
        for value in v:
            F.append(self.vehicle.Ta + self.vehicle.Tb*value +
                     self.vehicle.Tc*value*value)

        E = 0
        for i in range(0,len(a)):
            F[i] += (self.vehicle.mass+self.vehicle.load)*a[i]

            if a[i] >= 0:
                E += F[i]*v[i]/self.vehicle.eff
            else:
                E += F[i]*v[i]*self.vehicle.eff

        energy = E*2.77778e-7 # kWh
        length = int(float(len(v))/60) # minutes

        # first update details for outward journey

        p = 0
        for i in range(timeOut,timeOut+length):
            if i >= 24*60:
                i -= 24*60
            p += 1/float(length)
            self.avaliability[i] = 0
            self.location[i] = 1
            self.energySpent[i] += energy*p

        for i in range(timeOut+length,timeBack):
            if purpose == 'Commute':
                self.location[i] = 2
            elif purpose == 'Education':
                self.location[i] = 0  #PANIC, ok might be sorted
            else:
                self.location[i] = 3
            self.avaliability[i] = 0
            self.energySpent[i] += energy

        p = 0
        for i in range(timeBack,timeBack+length):
            if i >= 24*60:
                i -= 24*60
            p += 1/float(length)
            self.avaliability[i] = 0
            self.location[i] = 1
            self.energySpent[i] += energy*(1+p)

        if timeBack+length < 24*60:
            for i in range(timeBack+length,24*60):
                self.energySpent[i] += 2*energy

        self.energyLog.append([timeOut+length,energy])
        self.energyLog.append([timeBack+length,energy])

    def Charge(timeOn,timeOff,power):
        # put vehicle on charge
        for i in range(timeOn,timeOff):
            self.energySpent[i] -= power/60
    
class Fleet:
    def __init__(self):
        self.n = 0
        self.fleet = []

    def addAgent(self,agent):
        self.n += 1
        self.fleet.append(agent)

    def pickAvaliableAgent(self,timeA,timeB):
        avaliableAgents = []
        for i in range(0,self.n):
            j = timeA
            while self.fleet[i].avaliability[j] == 1 and j < timeB:
                j += 1
            if j == timeB:
                avaliableAgents.append(self.fleet[i])

        if avaliableAgents == []:
            print timeA
            print timeB
            raise Exception('no avaliable agents between times ' + str(timeA) +
                            ' and ' + str(timeB))
        else:
            ran = int(random.random()*len(avaliableAgents))
            return avaliableAgents[ran]

    def getFleetLocations(self,factor):
        home = [0]*(24*60)
        work = [0]*(24*60)
        driving = [0]*(24*60)
        other = [0]*(24*60)
        charging = [0]*(24*60)
        
        for i in range(0,self.n):
            for j in range(0,24*60):
                if self.fleet[i].location[j] == 0:
                    home[j] += factor
                elif self.fleet[i].location[j] == 1:
                    driving[j] += factor
                elif self.fleet[i].location[j] == 2:
                    work[j] += factor
                elif self.fleet[i].location[j] == 3:
                    other[j] += factor
                elif self.fleet[i].location[j] == 4:
                    charging[j] += factor
                else:
                    raise Exception('location problem')

        output = []
        output.append(home)
        output.append(work)
        output.append(driving)
        output.append(other)
        output.append(charging)
        
        return output

    def sortFleetEnergyLogs(self):

        for i in range(0,self.n):
            oldLog = self.fleet[i].energyLog
            newLog = []

            while len(oldLog) > 0:
                earliest = oldLog[0]
                for j in range(1,len(oldLog)):
                    if oldLog[j][0] < earliest[0]:
                        earliest = oldLog[j]

                newLog.append(earliest)
                oldLog.remove(earliest)

            self.fleet[i].energyLog = newLog
                    
                    
    def getFleetExpenditure(self):
        power = [0]*(24*60)

        for i in range(0,self.n):
            for j in range(0,24*60):
                power[j] += self.fleet[i].energySpent[j]

        return power

class ChargingScheme:

    def __init__(self, fleet):
        self.fleet = fleet
        self.n = fleet.n
        self.powerDemand = [0]*(24*60)

class HomeOnly(ChargingScheme):

    def allCharge(self,power,factor):
        for k in range(0,self.n):
            journeys = fleet.fleet[k].energyLog
            #battery = fleet.fleet[k].battery
            cap = fleet.fleet[k].vehicle.capacity
            battery = cap
            incomplete = []

            if len(journeys) != 0:
                
                for l in range(journeys[0][0],24*60):
                    # first check there isn't a journey 
                    if len(journeys) != 0:
                        if l == journeys[0][0]:
                            battery -= journeys[0][1]

                            # check you haven't run out of charge
                            if fleet.fleet[k].battery <= 0:
                                print 'agent #'+fleet.fleet[k].name+' has run out of charge'

                            # once you've dealt with the journey remove it
                            journeys.remove(journeys[0])

                    # now check if the vehicle needs to charge
                    if battery < cap:
                        # and if it's avaliable to charge
                        if fleet.fleet[k].location[l] == 0:
                            # then put it onto charge
                            
                            if battery + float(power)/60 > cap:
                                self.powerDemand[l] += (cap-battery)*60*factor
                                battery = cap
                            else:
                                battery += float(power)/60
                                fleet.fleet[k].location[l] = 4
                                self.powerDemand[l] += power*factor
            if battery < cap:
                incomplete.append([fleet.fleet[k].name,battery/cap])

        if incomplete == []:
            print 'all vehicles fully charged'
        else:
            print str(len(incomplete)) + ' of ' + str(self.n),
            print 'vehicles did not reach full charge'
            for row in incomplete:
                print 'agent#' + row[0] + ' is at ' + str(int(100*row[1])) + ' %'

        return self.powerDemand

                #print 'final battery: ' + str(fleet.fleet[k].battery),
                #print ' / ' + str(fleet.fleet[k].vehicle.capacity)
    
# ------------------------------------------------------------------------------
# INITIALIZATION SECTION
# ------------------------------------------------------------------------------
regionType = 'Urban City and Town'
region = ''
month = 'February'
day = 'Wednesday'
population = 150200

if population > 4000:
    i = 1
    while population > 4000:
        population = population/10
        i += 1
    factor = i*10

journeysPerPerson = 0
carsPerPerson = 0

# Based on region specific figures, determine the numbers of agents and journeys
with open('number.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['day'] == day:
            if row['month'] == month:
                if row['region'] == regionType:
                    journeysPerPerson = float(row['number'])
if journeysPerPerson == 0:
    raise Error('data for that region type / day / month not found')

numberJourneys = int(journeysPerPerson*population/2)
# added divisor as generating journes in pairs

if region == '':
    region = 'United Kingdom'

with open('vehiclesPerHead.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == region:
            carsPerPerson = float(row[1])

if carsPerPerson == 0:
    raise Error('are you sure that is a valid region?')

numberAgents = int(carsPerPerson*population)

# ok, now we know how much of everything we need let's start generating

nissanLeaf = Vehicle(1705,33.78,0.0618,0.02282,0.7,32)

# First we need to generate our fleet of vehicles
fleet = Fleet()
for k in range(0,numberAgents):
    agent = Agent(str(k), nissanLeaf, regionType)
    fleet.addAgent(agent)

print str(numberAgents) + ' agents were initialised'



# Then we need to generate the pool of journeys
pool = JourneyPool(day, month, regionType)
for k in range(0,numberJourneys):
    pool.addJourney()

print str(numberJourneys) + ' journeys were generated'

print 'now assigning journeys'
print 'PROGRESS:',
# Now we need to assign the journeys to vehicles in the fleet
for k in range(0,numberJourneys):
    if k%(numberJourneys/33) == 0:
        print 'X',
    journey = pool.pickOutJourney()
    agent = fleet.pickAvaliableAgent(journey[1],journey[2])
    agent.addJourney(journey)
print ''
print 'All journeys assigned!'


# Sort the energy logs into chronological order
fleet.sortFleetEnergyLogs()
print 'All logs sorted chronologically'

test = ChargingScheme(fleet)
homeOnly = HomeOnly(test)

homeOnly.allCharge(0.4,factor)


# ------------------------------------------------------------------------------
# PLOT FLEET LOCATION VARIATION WITH TIME
# ------------------------------------------------------------------------------
t = np.linspace(4,28,num=24*60)
n = fleet.getFleetLocations(factor)

# Generating figure and lines
plt.figure(1)
plt.plot(t,n[0],label='Home')
plt.plot(t,n[2],label='Work')
plt.plot(t,n[3],label='Other')
plt.plot(t,n[1],label='In Transit')
plt.plot(t,n[4],label='Charging')

# sort out the y axis
plt.ylim((0,fleet.n*factor+1))
plt.ylabel('number vehicles')

# and x axis
x = np.linspace(6,26,num=6)
my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
plt.xticks(x, my_xticks)
plt.xlim((4,28))
plt.xlabel('time')

# Finally, add legend
plt.legend(loc=1)
plt.show()

# For some reason i'm also plottong the total energy consumption with time
plt.figure(2)
plt.plot(t,homeOnly.powerDemand)

my_xticks = ['06:00','10:00','16:00','18:00','22:00','02:00']
plt.xticks(x, my_xticks)
plt.xlim((4,28))
plt.xlabel('time')
plt.ylabel('power demand /kW')

plt.show()
"""
plt.figure(1)
for i in range(0,10):
    plt.subplot(5,2,i+1)
    plt.plot(t,fleet.fleet[i].location,t,fleet.fleet[i].avaliability)
plt.show()
"""

#plt.plot(np.linspace(0,24,num=24*60),pool.commute)
#plt.show()
