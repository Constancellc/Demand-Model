import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import datetime

# ------------------------------------------------------------------------------
# CLASS DEFINITIONS SECTION
# ------------------------------------------------------------------------------

class Drivecycle:
    def __init__(self, distance):
        
        # First, import artemis
        v0 = []
        with open('artemis_urban.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                v0.append(float(row[0])*0.277778)

        # Then, calculate distance covered by one cycle
        s0 = 0
        for value in v0:
            s0 += value

        v = []
        if s0 >= distance:
            # If the distance covered by one cycle is greater than the trip
            s = 0
            i = 0
            while s <= distance:
                v.append(v0[i])
                s += v0[i]
                i += 1

        else:
            for i in range(0,int(distance/s0)):
                for value in v0:
                    v.append(value)
            s = int(distance/s0)*s0
            
            while s <= distance:
                v.append(v0[i])
                s += v0[i]
                i += 1

        self.velocity = v

        a = [0]

        for i in range(0,len(v)-1):
            a.append(v[i+1]-v[i])

        self.acceleration = a

class Vehicle:
    def __init__(self,mass,Ta,Tb,Tc,eff):
        self.mass = mass
        self.Ta = Ta
        self.Tb = Tb
        self.Tc = Tc
        self.eff = eff

    def loadEnergies(self):
        # first we're going to want to get the region specific lengths, then
        # scale the drive cycle and finally work out the energies
        energy = {'Urban Conurbation':{'Commute':0,'Education':0,'Business':0,
                               'Shopping':0,'Other escort + personal':0,
                               'Entertainment':0,'Other':0},
          'Urban City and Town':{'Commute':0,'Education':0,'Business':0,
                                 'Shopping':0,'Other escort + personal':0,
                                 'Entertainment':0,'Other':0},
          'Rural Town and Fringe':{'Commute':0,'Education':0,'Business':0,
                                   'Shopping':0,'Other escort + personal':0,
                                   'Entertainment':0,'Other':0},
          'Rural Village, Hamlet and Isolated Dwelling':{'Commute':0,
                                                         'Education':0,
                                                         'Business':0,
                                                         'Shopping':0,
                                                         'Other escort + personal':0,
                                                         'Entertainment':0,
                                                         'Other':0}}
        
        times = {'Urban Conurbation':{'Commute':0,'Education':0,'Business':0,
                               'Shopping':0,'Other escort + personal':0,
                               'Entertainment':0,'Other':0},
          'Urban City and Town':{'Commute':0,'Education':0,'Business':0,
                                 'Shopping':0,'Other escort + personal':0,
                                 'Entertainment':0,'Other':0},
          'Rural Town and Fringe':{'Commute':0,'Education':0,'Business':0,
                                   'Shopping':0,'Other escort + personal':0,
                                   'Entertainment':0,'Other':0},
          'Rural Village, Hamlet and Isolated Dwelling':{'Commute':0,
                                                         'Education':0,
                                                         'Business':0,
                                                         'Shopping':0,
                                                         'Other escort + personal':0,
                                                         'Entertainment':0,
                                                         'Other':0}}

        array = []
        
        with open('FINALregionTypePurposeLength.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array.append(row)

            regions = array[0]
            
            array = array[1:]

            for row in array:
                purpose = row[0]

                for i in range(1,len(regions)):
                    distance = float(row[i])*1609.34 # in m
                    cycle = Drivecycle(distance)
                    v = cycle.velocity 
                    a = cycle.acceleration

                    F = []
                    for value in v:
                        F.append(self.Ta + self.Tb*value + self.Tc*value*value)

                    for j in range(0,len(a)):
                        F[j] += self.mass*a[j]

                    E = 0
                    for j in range(0,len(a)):
                        if a[j] >= 0:
                            E += F[j]*v[j]/self.eff
                        else:
                            E += F[j]*v[j]*self.eff

                    energy[regions[i]][purpose] = E*2.77778e-7 # kWh
                    times[regions[i]][purpose] = float(len(v))/3600 # hours

        self.energy = energy
        self.times = times

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

        with open('FINALpurposeMonth.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            months = next(reader)

            for i in range(0,len(months)):
                if months[i] == month:
                    pdf = []
                    purposes = []
                    for row in reader:
                        pdf.append(float(row[i]))
                        purposes.append(row[0])

#            purposes.remove('')
#            pdf.remove(month)
            
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
        
        files = ['FINALpurposeDay.csv','FINALpurposeStartHour.csv']
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

        # but we actually want the finish time

        self.minutes += int(60*self.vehicle.times[regionType][self.purpose])

        while self.minutes >= 60:
            self.hour += 1
            self.minutes -= 60


# this is the doing stuff section

# first we need to pick things about our simulation

regionType = 'Urban Conurbation'
month = 'September'
day = 'Monday'

data = []

nissanLeaf = Vehicle(1705,33.78,0.0618,0.02282,0.7)
nissanLeaf.loadEnergies()

for i in range(0,100):
    trip = Journey(nissanLeaf)
    trip.generate(regionType, month, day)
    data.append([trip.hour, trip.minutes, trip.energy])

fieldnames = ['time','energy expended']

with open('journeysModel.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        time = datetime.time(row[0],row[1])
        writer.writerow([time,row[2]])

                
