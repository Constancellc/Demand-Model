import numpy as np
import csv
import random

class Drivecycle:
    def __init__(self, distance, version):
        
        # First, import artemis
        v0 = []

        if version == 'urban':
            with open('drivecycles/artemis_urban.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    v0.append(float(row[0])*0.277778)

        elif version == 'rural':
            with open('drivecycles/artemis_rural.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    v0.append(float(row[0])*0.277778)

        elif version == 'motorway':
            with open('../drivecycles/artemis_mway130.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    v0.append(float(row[0])*0.277778)

        else:
            raise InputError('please enter a valid version of artemis')

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
    # Vehicle just stores the salient parameters of an individual agent
    def __init__(self,mass,Ta,Tb,Tc,eff,cap):
        self.mass = mass # kg
        self.load = 0.0 #kg
        self.Ta = Ta*4.44822 # convert lbf to N
        self.Tb = Tb*9.9503 # lbf/mph -> N/mps
        self.Tc = Tc*22.258 # lbf/mph2 -> N/(mps)^2 
        self.eff = eff
        self.capacity = cap # kWh
        self.battery = cap
        self.p0 = 587.0 #1170.8 # This is the constant power loss in J/s

    def getEnergyExpenditure(self,cycle,accessoryLoad):
        # accesroy load in kW, cycle a Drivecycle object
        
        v = cycle.velocity # m/s
        a = cycle.acceleration # m/s2

        F = []
        for value in v:
            F.append(self.Ta + self.Tb*value + self.Tc*value*value)

        E = 0
        for i in range(0,len(a)):
            F[i] += (self.mass+self.load)*a[i]

            if a[i] >= 0:
                E += F[i]*v[i]/self.eff
            else:
                E += F[i]*v[i]*self.eff

            E += self.p0

        energy = E*2.77778e-7 # J -> kWh

        energy += len(v)*(accessoryLoad)/3600 # add accesory load 

        return energy

