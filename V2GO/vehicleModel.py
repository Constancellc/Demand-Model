import numpy as np
import csv
import random

class Drivecycle:
    def __init__(self, vt):

        v = []
        t = []
        s = 0
        for i in range(len(vt)):
            v.append(vt[i][1]*0.277778) # meters per second
            t.append(vt[i][0]) # seconds
            print(v[-1])
            print(t[-1])
            print('')
            if t[-1] < 60:
                s += v[-1]*t[-1]

        a = [0]
        for i in range(len(v)-1):
            if t[i+1] == 0:
                a.append(0)
            else:
                a.append((v[i+1]-v[i])/t[i+1])

        self.distance = s

        self.time = t

        self.velocity = v

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

    def getEnergyExpenditure(self,cycle):#,accessoryLoad):
        # accesroy load in kW, cycle a Drivecycle object
        
        v = cycle.velocity # m/s
        a = cycle.acceleration # m/s2
        t = cycle.time

        F = []
        for value in v:
            F.append(self.Ta + self.Tb*value + self.Tc*value*value)

        E = 0
        T = 0
        for i in range(0,len(a)):
            F[i] += (self.mass+self.load)*a[i] # N

            if v[i] > 0:
                T += t[i]
                
            if a[i] >= 0:
                E += (F[i]*v[i]/self.eff)*t[i]
            else:
                E += (F[i]*v[i]*self.eff)*t[i]


        E += self.p0*T
        energy = E*2.77778e-7 # J -> kWh

        #energy += len(v)*(accessoryLoad)/3600 # add accesory load 

        return energy

