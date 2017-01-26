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
                c = pdfPM[0]
                while c <= ran:
                    i += 1
                    c += pdfPM[i]

                backStartHour = i
                
        else:
            with open('nts-data/purposeStartHour.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                pdf = []
                for row in reader:
                    if row[0] == purpose:
                        pdf = row[1:]

                times = []

                for i in range(0,2):
                    ran = random.random()
                    i = 0
                    c = float(pdf[0])
                    while c <= ran:
                        i += 1
                        c += float(pdf[i])

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

        return journey[0]
    
class Agent:
    def __init__(self, vehicle, regionType):
        # vehicle - a loaded instance of the Vehicle class, regionType - string
        self.vehicle = vehicle
        self.regionType = regionType
        self.avaliability = [1]*(24*60)
        self.location = [0]*(24*60)
        self.journeys = []
        

# ------------------------------------------------------------------------------
# INITIALIZATION SECTION
# ------------------------------------------------------------------------------

regionType = 'Urban City and Town'
region = ''
month = 'May'
day = 'Wednesday'
population = 1500

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

# first the pool
pool = JourneyPool(day, month, regionType)

for i in range(0,10):
    pool.addJourney()

for i in range(0,10):
    print pool.pickOutJourney()


fleet = {}
nissanLeaf = Vehicle(1705,33.78,0.0618,0.02282,0.7)
nissanLeaf.loadEnergies()

print numberAgents
print numberJourneys

for i in range(0,numberAgents):
    fleet['vehicle'+str(i)] = Agent(nissanLeaf,regionType)
#plt.plot(np.linspace(0,24,num=24*60),pool.commute)
#plt.show()
