import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
import scipy.ndimage.filters as filt
from clustering import Cluster, ClusteringExercise

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'
eData = '../../Documents/elec_demand/MSOA_domestic_electricity_2016.csv'
outStem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA/'

p1_winter = []
p1_spring = []
p1_summer = []
p1_autumn = []

p2_winter = []
p2_spring = []
p2_summer = []
p2_autumn = []
with open('../../Documents/elec_demand/ProfileClass1.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p1_winter.append(float(row[-3]))
        p1_spring.append(float(row[-6]))
        p1_summer.append(float(row[-9]))
        p1_autumn.append(float(row[1]))
        
with open('../../Documents/elec_demand/ProfileClass2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p2_winter.append(float(row[-3]))
        p2_spring.append(float(row[-6]))
        p2_summer.append(float(row[-9]))
        p2_autumn.append(float(row[1]))

p1 = p1_winter
p2 = p2_winter

s1 = sum(p1)
s2 = sum(p2)

r1 = sum(p1_winter)/(sum(p1_winter)+sum(p1_spring)+sum(p1_summer)+\
                     sum(p1_autumn))
r2 = sum(p2_winter)/(sum(p2_winter)+sum(p2_spring)+sum(p2_summer)+\
                     sum(p2_autumn))
for t in range(48):
    p1[t] = p1[t]/s1
    p2[t] = p2[t]/s2

E7 = {}
Std = {}
n = {}
with open(eData,'r+',encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        LA = row[1]
        if LA == '':
            continue
        if LA not in E7:
            E7[LA] = 0
            Std[LA] = 0
            n[LA] = 0

        E7[LA] += float(row[4])# total kWh E7
        Std[LA] += float(row[5])# total kWh standard
        n[LA] += int(row[9])# total number of customers
        
def interpolate(x0,T):
    x1 = [0.0]*(len(x0)*T)
    for t in range(len(x1)):
        p1_ = int(t/T)
        if p1_ == len(x0)-1:
            p2_ = p1_
        else:
            p2_ = p1_+1
        f = float(t%T)/30
        x1[t] = (1-f)*x0[p1_]+f*x0[p2_]
    return x1

hh_v = {}
with open('../../Documents/UKDA-7553-tab/constance/hh-veh.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) == 1:
            hh_v[row[0]] = []
        else:
            hh_v[row[0]] = row[1:]

def g2v_fill(tot,y):
    en = 0
    for t in range(1440):
        if tot[t] < y:
            en += (y-tot[t])/60
            tot[t] = y

    return [tot,en]

def flatten_g2v(hh,eV):
    total = copy.deepcopy(hh)
    p = min(total)+0.1
    while eV > 0:
        [total,en] = g2v_fill(total,p)
        eV -= en
        p += 0.01

    return total


class MC_Run:

    def __init__(self,baseLoad):
        self.baseLoad = copy.deepcopy(baseLoad)

    def get_charging(self,households,nV,enLogs):
        
        chosen = []
        chosenV = []
        if len(households) < nV:
            print('not enough vehicle data')
            return None

        eV = 0
            
        while len(chosen) < nV:
            ran = int(random.random()*len(households))
            if households[ran] not in chosen:
                chosen.append(households[ran])
                for v in hh_v[households[ran]]:
                    if v in enLogs:
                        eV += enLogs[v]

        return flatten_g2v(self.baseLoad,eV)
        
                 
class MC_Sim:

    def __init__(self,nV,baseLoad,loc=None,lType=None):
        # lType 1-ward, 2-la, 3-ua, 4-county, 5-country
        self.r1 = {}
        self.r2 = {}
        self.nV =  nV
        self.households = []
        self.baseLoad = baseLoad

        if loc == None:
            with open('../../Documents/UKDA-7553-tab/constance/hh-loc.csv',
                      'rU') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    self.households.append(row[0])

        else:
            with open('../../Documents/UKDA-7553-tab/constance/hh-loc.csv',
                      'rU') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if row[lType] == loc:
                        self.households.append(row[0])

        self.enLog = {}
        with open(data,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row[1] not in self.households:
                    continue
                
                vehicle = row[2]
                day = int(row[6])

                if day > 5:
                    continue
                
                if vehicle not in self.enLog:
                    self.enLog[vehicle] = 0

                try:
                    distance = float(row[11]) # miles
                except:
                    continue

                kWh = distance*0.3

                if kWh > 30:
                    kWh = 30

                self.enLog[vehicle] += kWh

    def run(self,nRuns):
        results = []
        for r in range(nRuns):
            run = MC_Run(self.baseLoad)
            total = run.get_charging(self.households,self.nV,self.enLog)
            results.append(max(total))
            del run

        return sum(results)/len(results)

peaks = {}
with open(vehicles+'peaks.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        peaks[row[0]] = [float(row[1]),float(row[2]),]

for la in peaks:
    # get baseLoad
    e = E7[la]*2*r2/(365*0.25)
    s = Std[la]*2*r1/(365*0.25)
    baseLoad = []
    for t in range(48):
        new = (p1[t]*e+p2[t]*s)/n[la]
        baseLoad.append(new)
    baseLoad = interpolate(baseLoad,30)
    baseLoad = baseLoad*5

    # run MC
    sim = MC_Sim(50,baseLoad,la,2)
    res = sim.run(40)

    # store results
    peaks[la][2] = res

with open(vehicles+'peaks.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LA Code','Old Peak','Dumb Peak','Smart Peak'])
    for la in peaks:
        writer.writerow([la]+peaks[la])
    
