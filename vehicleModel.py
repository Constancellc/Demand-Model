import numpy as np
import csv
import random

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
        self.load = 0
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

            passengers = {'Commute':0.2,'Education':1.1,'Business':0.25,
                          'Shopping':0.7,'Other escort + personal':0.4,
                          'Entertainment':0.75,'Other':0.8}
            for row in array:
                purpose = row[0]

                self.load = passengers[purpose]*60

                for i in range(1,len(regions)):
                    distance = float(row[i])*1609.34 # in m
                    cycle = Drivecycle(distance)
                    v = cycle.velocity 
                    a = cycle.acceleration

                    F = []
                    for value in v:
                        F.append(self.Ta + self.Tb*value + self.Tc*value*value)

                    for j in range(0,len(a)):
                        F[j] += (self.mass+self.load)*a[j]

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
