import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import datetime

from vehicleModel import Drivecycle, Vehicle
"""
THIS FILE TAKES A SPECIFIC DAY OF THE WEEK, MONTH, REGION TYPE AND POPULATION
THEN RANDOMLY GENERATES A PREDICTED NUMBER OF JOURNEYS FOR THE AREA.

THE FINISH TIME AND ENERGY EXPENDITURE IN KWH OF EACH JOURNEY IS RECORDED AND
THE RESULTS WRITTEN INTO A CSV FILE

THE IDEA IS THAT THE DATA IN THIS CSV FILE CAN BE USED TO SIMULATE VARIOUS
CHARGING SENARIOS FOR LOCAL REGIONS.
"""
# ------------------------------------------------------------------------------
# CLASS DEFINITIONS SECTION
# ------------------------------------------------------------------------------

class Journey:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.purpose = ""
        self.hour = 0
        self.minutes = 0
        self.energy = 0

    def generate(self, regionType, month, day):
        # first choose the purpose of the journey

        array = []

        with open('nts-data/purposeMonth.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            months = next(reader)

            for i in range(0,len(months)):
                if months[i] == month:
                    pdf = []
                    purposes = []
                    for row in reader:
                        pdf.append(float(row[i]))
                        purposes.append(row[0])

        sumPdf = sum(pdf)

        cdf = [0,0,0,0,0,0,0]
        cdf[0] = pdf[0]/sumPdf

        for i in range(1,len(cdf)):
            cdf[i] = cdf[i-1]+pdf[i]/sumPdf

        ran = random.random()

        i = 0

        while cdf[i] < ran:
            i += 1

        self.purpose = purposes[i]

        self.energy = self.vehicle.energy[regionType][self.purpose]
        
        # now sampling to find region day and start hour
        
        files = ['nts-data/purposeDay.csv','nts-data/purposeStartHour.csv']
        out =  []

        for i in range(0,2):
            with open(files[i],'rU') as csvfile:
                pdf = []
                reader = csv.reader(csvfile)
                variables = next(reader)
                variables.remove("")
                for row in reader:
                    if row[0] == self.purpose:
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
            while cdf[i]<=ran and i < len(variables):
                i = i+1

            out.append(variables[i])

        self.day = out[0]
        self.hour = int(out[1])

        # now randomly assign a minute offset

        self.minutes = int(60*random.random())
        self.seconds = int(60*random.random())

        # but we actually want the finish time

        self.minutes += int(60*self.vehicle.times[regionType][self.purpose])

        while self.minutes >= 60:
            self.hour += 1
            self.minutes -= 60

        # health warning: this is a hack
        if self.hour > 23:
            self.hour -= 24


# this is the doing stuff section

# first we need to pick things about our simulation

regionType = 'Urban Conurbation'
month = 'September'
day = 'Monday'
population = 150200

data = []

# still always using the nissan leaf
nissanLeaf = Vehicle(1705,33.78,0.0618,0.02282,0.7)
nissanLeaf.loadEnergies()


journeysPerPerson = 0

with open('number.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['day'] == day:
            if row['month'] == month:
                if row['region'] == regionType:
                    journeysPerPerson = float(row['number'])

if journeysPerPerson == 0:
    print 'Details for region / day / month not found'
else:
    for i in range(0,int(journeysPerPerson*population)):
        trip = Journey(nissanLeaf)
        trip.generate(regionType, month, day)
        data.append([trip.hour, trip.minutes, trip.seconds, trip.energy])
    
fieldnames = ['time','index','energy expended']

with open('journeysModel.csv','w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for entry in data:
        row = {'time': datetime.time(entry[0],entry[1],entry[2])}
        row['index'] = (entry[0]*60+entry[1])*60+entry[2]
        row['energy expended'] = entry[3]
        writer.writerow(row)   
