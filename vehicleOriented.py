import matplotlib.pyplot as plt
import numpy as np
import csv
import random

from vehicleModel import Drivecycle, Vehicle

# ------------------------------------------------------------------------------
# CLASS DEFINITIONS SECTION
# ------------------------------------------------------------------------------

class JourneyPool:
    def __init__(self, day, month, regionType):
        self.day = day
        self.month = month
        self.regionType = regionType
        
        # initialising counters
        self.numCommute = 0
        self.numEducation = 0
        self.numBusiness = 0
        self.numShopping = 0
        self.numEscort = 0
        self.numEntertainment = 0
        self.numOther = 0

        self.morningCommutes = 0
        self.eveningCommutes = 0
        # and start times
        self.commute = [0]*60*24
        self.education = [0]*60*24
        self.business = [0]*60*24
        self.shopping = [0]*60*24
        self.escort = [0]*60*24
        self.entertainment = [0]*60*24
        self.other = [0]*60*24

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

        # we now have purpose, we now need time of day

        with open('nts-data/purposeStartHour.csv','rU') as csvfile:
            pdf = []
            reader = csv.reader(csvfile)
            hours = next(reader)
            hours.remove("")
            for row in reader:
                if row[0] == purpose:
                    pdf = row[1:]

        c = 0
        for value in pdf:
            c += float(value)

        normalised = []
        for value in pdf:
            normalised.append(float(value)/c)

        cdf = []
        c = 0

        for value in normalised:
            c += float(value)
            cdf.append(c)

        ran = random.random()
        i = 0
        while cdf[i]<=ran and i < len(hours):
            i = i+1

        startHour = int(hours[i])#-4
        
        #if startHour < 0:
        #    startHour += 24

        minutes = int(60*random.random())

        if purpose == 'Commute':
            if startHour <= 10 and startHour >= 4:
                self.morningCommutes += 1
            if startHour <= 21 and startHour >= 15:
                self.eveningCommutes += 1
            self.commute[startHour*60+minutes] += 1
            self.numCommute += 1
        elif purpose == 'Education':
            self.education[startHour*60+minutes] += 1
            self.numEducation += 1
        elif purpose == 'Business':
            self.business[startHour*60+minutes] += 1
            self.numBusiness += 1
        elif purpose == 'Shopping':
            self.shopping[startHour*60+minutes] += 1
            self.numShopping += 1
        elif purpose == 'Other escort + personal':
            self.escort[startHour*60+minutes] += 1
            self.numEscort += 1
        elif purpose == 'Entertainment':
            self.entertainment[startHour*60+minutes] += 1
            self.numEntertainment += 1
        elif purpose == 'Other':
            self.other[startHour*60+minutes] += 1
            self.numOther += 1
        else:
            raise Error('constance there is a bug in the add to dataset')

    def listTrips(self):

        for data in [self.commute, self.education, self.business, self.shopping,
                     self.escort, self.entertainment, self.other]:
            lst = []

            for i in range(0,len(data)):
                for j in range(0,data[i]):
                    lst.append()
    def pairTrips(self):

        lst = []
        
        for i in range(0,len(self.commute)):
            for j in range(0,self.commute[i]):
                lst.append(i)

        self.numCommute = int(self.numCommute/2)

        self.pairedCommutes = []
        for i in range(0,self.numCommute):
            self.pairedCommutes.append([lst[i],lst[i+self.numCommute]])

        lst = []
        
        for i in range(0,len(self.education)):
            for j in range(0,self.education[i]):
                lst.append(i)

        self.numEducation = int(self.numEducation/2)

        self.pairedEducation = []
        for i in range(0,self.numEducation):
            self.pairedEducation.append([lst[i],lst[i+self.numEducation]])

        lst = []
        
        for i in range(0,len(self.shopping)):
            for j in range(0,self.shopping[i]):
                lst.append(i)

        self.numShopping = int(self.numShopping/2)

        self.pairedShopping = []
        for i in range(0,self.numShopping):
            self.pairedShopping.append([lst[i],lst[i+self.numShopping]])

    def pickOutJourney(self,agent):
        # first select the purpose
        pdf = [float(self.numCommute),float(self.numEducation),
               float(self.numBusiness),float(self.numShopping),
               float(self.numEscort),float(self.numEntertainment),
               float(self.numOther)]

        sumPdf = sum(pdf)

        normalised = []
        for value in pdf:
            normalised.append(value/sumPdf)

        cdf = [normalised[0]]
        for j in range(1,len(normalised)):
            cdf.append(cdf[j-1]+normalised[j])

        ran = random.random()
        i = 0
        while cdf[i] <= ran and i < 6:
            i += 1

        purposes = ['Commute','Education','Business','Shopping',
                    'Other escort + personal','Entertainment','Other']

        if purposes[i] == 'Commute':
            # generate up to date distribution and sample

            # ok this is different now
            i = int(random.random()*len(self.pairedCommutes))
            agent.journeys.append(['Commute',self.pairedCommutes[i][0]])
            agent.journeys.append(['Commute',self.pairedCommutes[i][1]])

            self.pairedCommutes.remove(self.pairedCommutes[i])
            self.numCommute -= 1
            
        elif purposes[i] == 'Education':
            i = int(random.random()*len(self.pairedEducation))
            
            agent.journeys.append(['Education',self.pairedEducation[i][0]])
            agent.journeys.append(['Education',self.pairedEducation[i][1]])

            self.pairedEducation.remove(self.pairedEducation[i])
            self.numEducation -= 1

        elif purposes[i] == 'Business':
            sumPdf = sum(self.business)
            normalised = []
            for value in self.business:
                normalised.append(value/sumPdf)

            cdf = [normalised[0]]

            for j in range(1,len(normalised)):
                cdf.append(cdf[j-1]+normalised[j])

            ran = random.random()
            j = 0
            
            while cdf[j] <= ran and j < 1439:
                j += 1
                
            self.business[j] -= 1
            self.numBusiness -= 1

            agent.journeys.append([purposes[i],j])

        elif purposes[i] == 'Shopping':
            i = int(random.random()*len(self.pairedShopping))
            agent.journeys.append(['Shopping',self.pairedShopping[i][0]])
            agent.journeys.append(['Shopping',self.pairedShopping[i][1]])

            self.pairedShopping.remove(self.pairedShopping[i])
            self.numShopping -= 1

        elif purposes[i] == 'Other escort + personal':
            sumPdf = sum(self.escort)
            normalised = []
            for value in self.escort:
                normalised.append(value/sumPdf)

            cdf = [normalised[0]]

            for j in range(1,len(normalised)):
                cdf.append(cdf[j-1]+normalised[j])

            ran = random.random()
            j = 0
            
            while cdf[j] <= ran and j < 1439:
                j += 1

            agent.journeys.append([purposes[i],j])
            self.escort[j] -= 1
            self.numEscort -= 1

        elif purposes[i] == 'Entertainment':
            sumPdf = sum(self.entertainment)
            normalised = []
            for value in self.entertainment:
                normalised.append(value/sumPdf)

            cdf = [normalised[0]]

            for j in range(1,len(normalised)):
                cdf.append(cdf[j-1]+normalised[j])

            ran = random.random()
            j = 0
            
            while cdf[j] <= ran and j < 1439:
                j += 1

            agent.journeys.append([purposes[i],j])
            self.entertainment[j] -= 1
            self.numEntertainment -= 1

        elif purposes[i] == 'Other':
            sumPdf = sum(self.other)
            
            normalised = []
            for value in self.other:
                normalised.append(value/sumPdf)

            cdf = [normalised[0]]

            for j in range(1,len(normalised)):
                cdf.append(cdf[j-1]+normalised[j])

            ran = random.random()
            j = 0
            
            while cdf[j] <= ran and j < 1439:
                j += 1

            agent.journeys.append([purposes[i],j])
            self.other[j] -= 1
            self.numOther -= 1

        else:
            raise Error('purpose index bug')

        
    def displayCounters(self):
        print 'Commute:',
        print self.numCommute
        print 'Education:',
        print self.numEducation
        print 'Business:',
        print self.numBusiness
        print 'Shopping:',
        print self.numShopping
        print 'Escort:',
        print self.numEscort
        print 'Entertainment:',
        print self.numEntertainment
        print 'Other:',
        print self.numOther

    def getTotal(self):
        total = self.numCommute + self.numEducation + self.numBusiness + \
                self.numShopping + self.numEscort + self.numEntertainment + \
                self.numOther
        return total 
    
class Agent:
    def __init__(self, vehicle, regionType):
        # vehicle - a loaded instance of the Vehicle class, regionType - string
        self.vehicle = vehicle
        self.regionType = regionType
        self.journeys = []
        

# ------------------------------------------------------------------------------
# INITIALIZATION SECTION
# ------------------------------------------------------------------------------

regionType = 'Urban City and Town'
region = ''
month = 'July'
day = 'Monday'
population = 100

journeysPerPerson = 0
carsPerPerson = 0

with open('number.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['day'] == day:
            if row['month'] == month:
                if row['region'] == regionType:
                    journeysPerPerson = float(row['number'])
if journeysPerPerson == 0:
    raise Error('data for that region type / day / month not found')

numberJourneys = int(journeysPerPerson*population)

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

# first the pool
pool = JourneyPool(day, month, regionType)

#numberJourneys = int(numberJourneys*0.785) #roughly corrects 
for i in range(0,numberJourneys):
    pool.addJourney()
pool.displayCounters()

pool.pairTrips()


                                       
fleet = {}
nissanLeaf = Vehicle(1705,33.78,0.0618,0.02282,0.7)
nissanLeaf.loadEnergies()

print numberAgents
print numberJourneys

for i in range(0,numberAgents):
    fleet[i] = Agent(nissanLeaf,regionType)

N = pool.getTotal()
for i in range(0,N):
    n = int(random.random()*numberAgents)
    pool.pickOutJourney(fleet[n])
pool.displayCounters()
print fleet[4].journeys
#plt.plot(np.linspace(0,24,num=24*60),pool.commute)
#plt.show()
