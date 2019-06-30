import numpy as np
import csv
import random

'''
Notes:

- Currently hard coded to only accept drivecycles at 1 second resolution

'''

class Drivecycle:
    def __init__(self, vt,slope=None):

        if slope == None:
            self.slope = [0.0]*len(vt)
        else:
            self.slope = slope

        v = []
        t = []
        s = 0
        for i in range(len(vt)):
            v.append(vt[i]*0.277778) # meters per second
            t.append(i) # seconds
            s += v[-1]

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
        self.Ta = Ta#*4.44822 # convert lbf to N
        self.Tb = Tb#*9.9503 # lbf/mph -> N/mps
        self.Tc = Tc#*22.258 # lbf/mph2 -> N/(mps)^2 
        self.eff = eff
        self.capacity = cap # kWh
        self.battery = cap
        self.p0 = 1300.0 # This is the constant power loss in J/s

    def getEnergyExpenditure(self,cycle):#,accessoryLoad):
        # accesroy load in kW, cycle a Drivecycle object
        
        v = cycle.velocity # m/s
        a = cycle.acceleration # m/s2
        t = cycle.time
        s = cycle.slope

        F = []
        for value in v:
            F.append(self.Ta + self.Tb*value + self.Tc*value*value)
        for i in range(len(v)):
            F[i] += self.mass*9.81*np.sin(s[i])

        E = 0
        T = 0
        for i in range(0,len(a)):
            F[i] += (self.mass+self.load)*a[i] # N

            if v[i] > 0.1:
                T += 1#t[i]
                
            if a[i] >= 0:
                E += (F[i]*v[i]/self.eff)#*t[i]
            else:
                E += (F[i]*v[i]*self.eff)#*t[i]


        E += self.p0*T
        energy = E*2.77778e-7 # J -> kWh

        #energy += len(v)*(accessoryLoad)/3600 # add accesory load 

        return energy
    
    def getEnergyExpenditurePerSecond(self,cycle):#,accessoryLoad):
        # accesroy load in kW, cycle a Drivecycle object
        
        v = cycle.velocity # m/s
        a = cycle.acceleration # m/s2
        t = cycle.time
        s = cycle.slope

        F = []
        for value in v:
            F.append(self.Ta + self.Tb*value + self.Tc*value*value)
        for i in range(len(v)):
            F[i] += self.mass*9.81*np.sin(s[i])

        energy = []
        for i in range(0,len(a)):
            F[i] += (self.mass+self.load)*a[i] # N
                
            if a[i] >= 0:
                E = (F[i]*v[i]/self.eff)#*t[i]
            else:
                E = (F[i]*v[i]*self.eff)#*t[i]

            if v[i] < 1 and abs(a[i]) < 1:
                energy.append(0.0)
            else:
                energy.append((E+self.p0)*2.77778e-7)

        return energy

