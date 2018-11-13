import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag, sparse, solvers

# ok here is how it's going to go.
simulationDay = 3
nMC = 4
nH = 50
c_eff = 0.9
capacity = 30 # kWh
pMax = 3.5 # kW


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
with open('../../Documents/simulation_results/NTS/clustering/labels2/allVehicles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        allVehicles.append(row[0])

journeyLogs = {}
with open('../../Documents/UKDA-5340-tab/constance-trips.csv','rU') as csvfile:
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
            shift = 30*random.random()
            start = int(30*int(int(row[9])/30)+shift)
            end = int(30*int(int(row[10])/30)+shift)
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
with open('../../Documents/sharonb/7591/csv/profiles.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        day = int(row[-1])
        if day != simulationDay:
            continue
        if random.random() > 0.01:
            continue
        p = []
        for t in range(48):
            p.append(float(row[2+t]))
        hhProfiles[c] = p
        c += 1


for pen in [1.0]:
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
        
        nV = int(nH*pen)
        chosenV = []
        #vCon = []
        while len(chosenV) < nV:
            ranV = allVehicles[int(random.random()*len(allVehicles))]
            if ranV not in chosenV:
                chosenV.append(ranV)

        b_ = []
        a_ = []
        for v in chosenV:
            if v not in journeyLogs:
                continue
            kWh = 0
            c = []
            for j in journeyLogs[v]:
                kWh += j[2]
                c.append([j[0],j[1]]) # to be clear these are times we cant charge
                if j[3] != '23':
                    c.append([j[1],''])

            a = [0]*1440
            for i in range(len(c)):
                c_ = c[i]
                if c_[1] != '':
                    for t in range(c_[0],c_[1]):
                        if t < 1440:
                            a[t] = 1
                elif i < len(c)-1:
                    for t in range(c_[0],c[i+1][0]):
                        if t < 1440:
                            a[t] = 1
                else:
                    for t in range(c_[0],1440):
                        a[t] = 1

            a_.append(a)

            possible_charge = pMax*(1440-sum(a))/60
            
            if kWh > capacity:
                kWh = capacity
            if kWh >= possible_charge:
                kWh = possible_charge*0.99

            b_.append(kWh)

        n = len(b_)
        if n == 0:
            continue

        # actually, I should only do one optimization

        T = 1440

        A = matrix(0.0,(2*n,n*T))
        b = matrix(b_+[0]*n)
        
        for v in range(n):
            for t in range(T):
                A[v,T*v+t] = c_eff/60
                A[v+n,T*v+t] = a_[v][t]
                

        P = sparse([[spdiag([1]*T)]*n]*n)
        q = matrix(copy.deepcopy(totalH)*n)
        
        G = sparse([spdiag([-1.0]*(n*T)),spdiag([1.0]*(n*T))])
        h = matrix([0.0]*(n*T)+[pMax]*(n*T))

        try:
            sol=solvers.qp(P,q,G,h,A,b)
        except:
            continue

        if sol['status'] != 'optimal':
            continue
        
        x = sol['x'] # original method

        # work out totol power demand and battery throughput
        total1 = [0.0]*48
        total2 = [0.0]*48
        totalH30 = [0.0]*48
        individuals1 = []
        individuals2 = []
        for v in range(n):
            individuals1.append([0]*1440)
            individuals2.append([0]*1440)
            for t in range(1440):
                individuals1[v][t] = x[1440*v+t]
            for t in range(48):
                p_av = sum(x[1440*v+30*t:1440*v+30*(t+1)])/30
                if p_av < 0.05:
                    continue
                t_req = int(p_av*30/3.5)
                p_rem = p_av*30%3.5
                wait = int(random.random()*(29-t_req))
                for t_ in range(t_req):
                    try:
                        individuals2[v][30*t+wait+t_] = 3.5
                    except:
                        continue
                if (30*t+wait+t_req) < 1440:
                    individuals2[v][30*t+wait+t_req] = p_rem
                
        for t in range(1440):
            total1[int(t/30)] += totalH[t]/30
            total2[int(t/30)] += totalH[t]/30
            totalH30[int(t/30)] += totalH[t]/30
            for v in range(n):
                total1[int(t/30)] += individuals1[v][t]/30
                total2[int(t/30)] += individuals2[v][t]/30
                
plt.figure()
plt.plot(np.arange(0,24,0.5),totalH30,c='k',ls=':',label='base')
plt.plot(np.arange(0,24,0.5),total1,label='continous')
plt.plot(np.arange(0,24,0.5),total2,ls='--',label='discrete')
plt.legend()
plt.grid()

plt.figure()
for i in range(4):
    plt.subplot(2,2,i+1)
    plt.plot(individuals1[i])
    plt.plot(individuals2[i],ls='--')
plt.show()
