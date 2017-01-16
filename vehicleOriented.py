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
            raise Error('constance there is a bug! (add to dataset)')

    def pickOutJourney(self):
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
            sumPdf = sum(self.commute)
            normalised = []
            for value in self.commute:
                normalised.append(value/sumPdf)

            cdf = [normalised[0]]

            for j in range(1,len(normalised)):
                cdf.append(cdf[j-1]+normalised[j])

            ran = random.random()
            j = 0
            
            while cdf[j] <= ran and j < 1439:
                j += 1

            self.commute[j] -= 1
            self.numCommute -= 1
            
        elif purposes[i] == 'Education':
            sumPdf = sum(self.education)
            normalised = []
            for value in self.education:
                normalised.append(value/sumPdf)

            cdf = [normalised[0]]

            for j in range(1,len(normalised)):
                cdf.append(cdf[j-1]+normalised[j])

            ran = random.random()
            j = 0
            
            while cdf[j] <= ran and j < 1439:
                j += 1
                
            self.education[j] -= 1
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

        elif purposes[i] == 'Shopping':
            sumPdf = sum(self.shopping)
            normalised = []
            for value in self.shopping:
                normalised.append(value/sumPdf)

            cdf = [normalised[0]]

            for j in range(1,len(normalised)):
                cdf.append(cdf[j-1]+normalised[j])

            ran = random.random()
            j = 0
            
            while cdf[j] <= ran and j < 1439:
                j += 1
                
            self.shopping[j] -= 1
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
                
            self.other[j] -= 1
            self.numOther -= 1

        else:
            raise Error('purpose index bug')

        startTime = j
        
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
    
class Agent:
    def __init__(vehicle, regionType):
        # vehicle - a loaded instance of the Vehicle class, regionType - string
        return 'please finish this'

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

numberJourneys = journeysPerPerson*population

if region == '':
    region = 'United Kingdom'

with open('vehiclesPerHead.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == region:
            carsPerPerson = row[1]

if carsPerPerson == 0:
    raise Error('are you sure that is a valid region?')

numberAgents = carsPerPerson*population

# ok, now we know how much of everything we need let's start generating

# first the pool
pool = JourneyPool(day, month, regionType)

for i in range(0,100):
    pool.addJourney()
pool.displayCounters()

for i in range(0,100):
    pool.pickOutJourney()
pool.displayCounters()

#plt.plot(np.linspace(0,24,num=24*60),pool.commute)
#plt.show()
