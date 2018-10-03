import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag, sparse, solvers

# ok here is how it's going to go.
simulationDay = 3
nMC = 100
nH = 50
c_eff = 0.9
capacity = 30 # kWh
pMax = 3.5 # kW
pMax_ = 3.5 # kW for V2G

def interpolate(x0,T):
    x1 = [0.0]*(len(x0)*T)
    for t in range(len(x1)):
        p1 = int(t/T)
        if p1 == len(x0)-1:
            p2 = p1
        else:
            p2 = p1+1
        f = float(t%T)/30
        x1[t] = (1-f)*x0[p1]+f*x0[p2]
    return x1

# First we gotta get vehicle usage and household demand.

# Pick a simulation day (just going to loop round hehe)

# Get the list of all vehicles and journey logs
# get all Vehicles
allVehicles = []
with open('../../../Documents/simulation_results/NTS/clustering/labels2/allVehicles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        allVehicles.append(row[0])

journeyLogs = {}
with open('../../../Documents/UKDA-5340-tab/constance-trips.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        
        day = int(row[6])
        
        if day != simulationDay:
            continue
        vehicle = row[2]
        
        if vehicle not in journeyLogs:
            journeyLogs[vehicle] = []

        try:
            start = int(30*int(int(row[9])/30)+30*random.random())
            end = int(30*int(int(row[10])/30)+30*random.random())
            distance = float(row[11]) # miles
            purpose = row[-2]
        except:
            continue

        kWh = distance*0.3

        if end < start:
            end += 1440

        journeyLogs[vehicle].append([start,end,kWh,purpose])

# Get the HH demand, one from each hh
# get a list of hh?
c = 0
hhProfiles = {}
with open('../../../Documents/sharonb/7591/csv/profiles.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        day = int(row[-1])
        if day != simulationDay:
            continue
        if random.random() > 0.005:
            continue
        p = []
        for t in range(48):
            p.append(float(row[2+t]))
        hhProfiles[c] = p
        c += 1

for pen in [1.0]:
    g2v = []
    v2g = []
    # For each MC simulation
    for mc in range(nMC):
        chosenH = []
        while len(chosenH) < nH:
            ranH = int(random.random()*len(hhProfiles))
            if ranH not in chosenH:
                chosenH.append(ranH)

        totalH = [0.0]*1440
        for h in chosenH:
            p = interpolate(hhProfiles[h],30)
            for t in range(1440):
                totalH[t] += p[t]
        
        nV = int(random.random()*nH*pen)
        chosenV = []
        while len(chosenV) < nV:
            ranV = allVehicles[int(random.random()*len(allVehicles))]
            if ranV not in chosenV:
                chosenV.append(ranV)
