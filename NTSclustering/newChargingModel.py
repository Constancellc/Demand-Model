import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'
trip_data = '../../Documents/UKDA-5340-tab/constance-trips.csv'
# First get the pdfs for charging
pdfs = {'0':{},'1':{}}
pdfs_ = {'0':{},'1':{}}
for d in ['0','1']:
    for i in range(3):
        pdfs[d][i] = {}
        for s in range(6):
            pdfs[d][i][s] = [0]*48
    for s in range(6):
        pdfs_[d][s] = [0]*48

stm = {'0':'jointPdfW','1':'jointPdfWE'}
for d in ['0','1']:
    for i in range(3):       
        with open(stem+stm[d]+str(i+1)+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            s = 0
            for row in reader:
                for t in range(48):
                    pdfs[d][i][s][t] = float(row[t])
                s += 1
                
    with open(stem+stm[d]+'_.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        s = 0
        for row in reader:
            for t in range(48):
                pdfs_[d][s][t] = float(row[t])
            s += 1

# Then get the NTS vehicle labels, and the household to vehicle list
NTS = {}
with open(stem+'NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS[row[0]] = int(row[1])
with open(stem+'NTSlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS[row[0]] = int(row[1])

# The class will take a list of households
class Simulation:
    def __init__(self,households):
        #self.households = households
        self.journeyLogs = {}
        with open(trip_data,'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                hh = row[1]
                if hh not in households:
                    continue
                
                vehicle = row[2]

                if vehicle == '' or vehicle == ' ':
                    continue

                try:
                    day = int(row[6])-1
                    start = int(row[9])+1440*day
                    end = int(row[10])+1440*day
                    dist = float(row[11])
                except:
                    continue
                
                if vehicle not in self.journeyLogs:
                    self.journeyLogs[vehicle] = []
                    
                if end < start:
                    end += 1440
                kWh = dist*0.3

                self.journeyLogs[vehicle].append([start,end,kWh])

    # A dictionary of journey logs will be created

    # function chargeAfterJourney returns True or False
    def chargeAfterJourney(self,d,k,s,t):
        if random.random() < pdfs[d][k][s][t]:
            return True
        else:
            return False
        
    def randomCharge(self,d,s,t):
        if random.random() < pdfs_[d][s][t]/30:
            return True
        else:
            return False

# function: predictCharging
    def predictCharging(self,vehicle,power=3.5):
        jLog = sorted(self.journeyLogs[vehicle])+[[10079,10080,0]]
        capacity = 30
        j = 0
        t = jLog[j][0]
        SOC = 0.999
        startCharge = False
        while t < 10080:
            while t < jLog[j][0] and startCharge == False:
                if t < 7200:
                    d = '0'
                else:
                    d = '1'
                    
                t += 1
                startCharge = self.randomCharge(d,int(SOC*6),int((t%1440)/30))

            if t == jLog[j][0] and t < 10079:
                SOC -= jLog[j][2]/capacity
                if SOC < 0:
                    SOC = 0
                t = jLog[j][1]
                j += 1
                #print(jLog[j])
                try:
                    k = NTS[vehicle+str(int(t/1440)+1)] # check - days in 0?!
                except:
                    #print(vehicle)
                    k = int(random.random()*3) # hack
                if t < 7200:
                    d = '0'
                else:
                    d = '1'

                startCharge = self.chargeAfterJourney(d,k,int(SOC*6),
                                                      int((t%1440)/30))

            if startCharge == True:
                while SOC < 0.99 and t<jLog[j][0] and t<jLog[-1][0]:
                    self.charging[t] += power
                    SOC += power/(60*capacity)
                    t += 1
                startCharge = False

            if t > jLog[j][0]:
                j += 1
                
            if j == len(jLog)-1:
                t = 10080
                    
    def uncontrolledCharge(self,power,capacity):
        self.charging = [0]*10080
        for vehicle in self.journeyLogs:
            self.predictCharging(vehicle,power)
            
        return self.charging

    def dumbCharge(self,power,capacity):
        charging = [0]*10080
        for vehicle in self.journeyLogs:
            jLog = self.journeyLogs[vehicle]
            days = {0:[0,0],1:[0,0],2:[0,0],3:[0,0],4:[0,0],5:[0,0],6:[0,0]}
            for j in jLog:
                t = j[1]%1440
                d = int(j[1]/1440)
                if d > 6:
                    continue
                days[d][1] += j[2]
                if t > days[d][0]:
                    days[d][0] = t
            for d in days:
                if days[d][1] > capacity:
                    days[d][1] = capacity
                time_req = days[d][1]*60/power
                for t in range(int(time_req)):
                    if d*1440+days[d][0]+t < 10080:
                        charging[d*1440+days[d][0]+t] += power

        return charging

    def smartCharge(self):
        return ''

class MC_Simulation:

    def __init__(self,households,nH=None):
        if nH != None and nH > len(households):
            households2 = []
            while len(households2) < nH:
                r = households[int(random.random()*len(households))]
                if r not in households2:
                    households2.append(r)
            households = households2
        self.sim = Simulation(households)

    def dumbCharge(self,power,capacity):
        return self.sim.dumbCharge(power,capacity)

    def uncontrolledCharge(self,power,capacity,nSim=1):
        m = [0]*10080
        l = [999999]*10080
        u = [0]*10080

        x = {}
        for t in range(10080):
            x[t] = []

        for mc in range(nSim):
            c = self.sim.uncontrolledCharge(power,capacity)
            for t in range(10080):
                m[t] += c[t]/nSim
                x[t].append(c[t])

        for t in range(10080):
            lst = sorted(x[t])
            l[t] = lst[int(nSim*0.1)]
            u[t] = lst[int(nSim*0.9)]
                    
        if nSim > 1:
            return [m,l,u]
        else:
            return m

class LV_MC_Simulation:

    def __init__(self,nH,penetration=1):
        self.nH = nH
        
# function: uncontrolledCharge
    # this will apply my new model
    # options? charging power, 

# function: uncontrolledCharge0(power)
    # this will assue charging immediately after last journey until full


