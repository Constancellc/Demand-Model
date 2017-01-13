import matplotlib.pyplot as plt
import numpy as np
import csv
import random

from vehicleModel import Drivecycle, Vehicle

# ------------------------------------------------------------------------------
# CLASS DEFINITIONS SECTION
# ------------------------------------------------------------------------------

class JourneyPool:
    def __init__(day, month, regionType):
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
        self.eduction = [0]*60*24
        self.business = [0]*60*24
        self.shopping = [0]*60*24
        self.escort = [0]*60*24
        self.entertainment = [0]*60*24
        self.other = [0]*60*24

    def addJourney(day):

        files = ['nts-data/purposeDay.csv','nts-data/purposeMonth.csv',
                 'nts-data/regionTypePurpose.csv']
        fixed = [self.day, self.month, self.regionType]

        purpose|day = [0]*7
        purpose|month = [0]*7
        purpose|region = [0]*7
        
        out = []
        
        # first, find the purpose given the regionType, or maybe day of week, or month... FUCK
        with open('nts-data/purposeDay.csv') as csvfile:
            reader = csv.reader(csvfile)
            variables = next(reader)
            for i in range(0,len(days)):
                if variables[i] == self.day:
                    index = i

            if index is False:
                raise Error('pdf problems')

            purposes = []
            pdf = []
            
            for row in reader:
                if row == days:
                    continue
                else:
                    purposes.append(row[0])
                    pdf.append(row[dayIndex])
        sumPdf = 0

        for number in pdf:
           sumPdf += float(pdf)

        distribution = [0]*7

        for i in range(0,7):
           distribution[i] = float(pdf[i])/sumPdf

        out.append(distribution)
        
class Agent:
    def __init__(vehicle, regionType):
        # vehicle - a loaded instance of the Vehicle class, regionType - string


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

if region = '':
    region = 'United Kingdom'

with open('vehiclesPerHead.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == region:
            carsPerPerson = row[1]

if carsPerPerson == 0:
    raise Error('are you sure that is a valid region?')

numberAgents = carsPerPerson*population

# ok, now we know how much of everything we need let's start generating

# first the pool
