import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag, sparse, solvers

# ok here is how it's going to go.
simulationDay = 3
nMC = 80
nH = 50
c_eff = 0.9 
pMax = 3.5 # kW G2V
pMax_ = 3.5 # kW V2G
capacity = 30 # kWh

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

# get vehicle use
texas_hh = []
with open('../../../Documents/NHTS/constance/texas-hh.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if int(row[1]) == simulationDay:
            texas_hh.append(row[0])
            
allVehicles = []
journeyLogs = {}
with open('../../../Documents/NHTS/constance/texas-trips.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        day = int(row[2])
        if day != simulationDay:
            continue
        hh = row[1]
        if hh not in texas_hh:
            continue
        v = row[0]
        if v not in journeyLogs:
            journeyLogs[v] = []
            allVehicles.append(v)
            
        start = int(row[5])
        end = int(row[6])
        purp = row[-1]

        if purp in ['01','02']:
            home = True
        else:
            home = False

        kWh = 0.3*float(row[7])

        journeyLogs[v].append([start,end,kWh,home])
        
# get household profiles
c = 0
hhProfiles = {}
with open('../../../Documents/pecan-street/1min-texas/profiles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = [0.0]*48
        for t in range(1440):
            p[int(t/30)] += float(row[t])/30
        hhProfiles[c] = p
        c += 1


for pen in [60]:
    pen = pen/100
    g2v = []
    v2g = []
    # For each MC simulation
    for mc in range(nMC):
        chosenH = []
        while len(chosenH) < nH:
            ranH = int(random.random()*len(hhProfiles))
            if ranH not in chosenH:
                chosenH.append(ranH)

        totalH = [0.0]*144
        totalH1 = [0.0]*1440
        for h in chosenH:
            p = interpolate(hhProfiles[h],30)
            for t in range(1440):
                totalH[int(t/10)] += p[t]/10
                totalH1[t] += p[t]
        
        nV = int(nH*pen)
        chosenV = []
        while len(chosenV) < nV:
            ranV = allVehicles[int(random.random()*len(allVehicles))]
            if ranV not in chosenV:
                chosenV.append(ranV)

        b = []
        a_ = []
        for v in chosenV:
            if v not in journeyLogs:
                continue
            kWh = 0
            c = []
            for j in journeyLogs[v]:
                kWh += j[2]
                c.append([j[0],j[1]]) # to be clear these are times we cant charge
                if j[3] == False:
                    c.append([j[1],''])

            a = [0]*144
            for i in range(len(c)):
                c_ = c[i]
                if c_[1] != '':
                    for t in range(int(c_[0]/10),int(c_[1]/10)):
                        if t < 144:
                            a[t] = 1
                elif i < len(c)-1:
                    for t in range(int(c_[0]/10),int(c[i+1][0]/10)):
                        if t < 144:
                            a[t] = 1
                else:
                    for t in range(int(c_[0]/10),144):
                        a[t] = 1

            a_.append(a)

            possible_charge = pMax*(144-sum(a))/6
            
            if kWh > capacity:
                kWh = capacity
            if kWh >= possible_charge:
                kWh = possible_charge*0.99

            b.append(kWh)

        n = len(b)
        if n == 0:
            continue
        b = matrix(b+[0.0]*n)
        A = matrix(0.0,(2*n,n*144+1))
        G = matrix(0.0,(144,n*144+1))
        q = matrix([0.0]*(144*n)+[1.0])
        P = spdiag([0.0001]*(144*n+1))
        
        for v in range(n):
            for t in range(144):
                A[v,144*v+t] = c_eff/6
                A[v+n,144*v+t] = a_[v][t]
                G[t,144*v+t] = 1.0
                
        h0 = []
        for t in range(144):
            G[t,144*n] = -1.0
            h0.append(-1.0*totalH[t])

        G1 = sparse([[spdiag([-1.0]*(n*144))],[matrix([0.0]*(n*144))]])
        G2 = sparse([[spdiag([1.0]*(n*144))],[matrix([0.0]*(n*144))]])
        

        G = sparse([G,G1,G2])
        h = matrix(h0+[0.0]*(n*144)+[pMax]*(n*144))

        try:
            sol=solvers.qp(P,q,G,h,A,b)
        except:
            continue
        
        x = sol['x'] # without V2G

        if sol['status'] != 'optimal':
            continue

        # work out totol power demand and battery throughput
        total1 = [0.0]*1440
        through1 = sum(b)
        for t in range(1440):
            total1[t] += totalH1[t]
            for v in range(n):
                total1[t] += x[144*v+int(t/10)]
                through1 += x[144*v+int(t/10)]*c_eff/60
                
        del A
        del G
        del h
        del P
        del q
                
        # I think I actually need to reformulate for V2G,
        # defining seperate variables for charigng and discharging
        
        A = matrix(0.0,(2*n,2*n*144+1))
        G = matrix(0.0,(144,2*n*144+1))
        P = spdiag([0.0001]*(144*2*n+1))
        q = matrix([0.0]*(144*2*n)+[1.0])

        for v in range(n):
            for t in range(144):
                A[v,144*v+t] = c_eff/6 # incorporate efficiency here also?
                A[v,144*(n+v)+t] = -1/(6*c_eff)
                
                A[v+n,144*v+t] = a_[v][t]
                A[v+n,144*(n+v)+t] = a_[v][t]

                G[t,144*v+t] = 1.0
                G[t,144*(n+v)+t] = -1.0

        for t in range(144):
            G[t,144*2*n] = -1.0

        G1 = sparse([[spdiag([-1.0]*(2*n*144))],[matrix([0.0]*(2*n*144))]])
        G2 = sparse([[spdiag([1.0]*(2*n*144))],[matrix([0.0]*(2*n*144))]])
        
        G = sparse([G,G1,G2])
        h = matrix(h0+[0.0]*(2*n*144)+[pMax]*(n*144)+[pMax_]*(n*144))
        
        sol=solvers.qp(P,q,G,h,A,b)

        x = sol['x'] # with V2G

        if sol['status'] != 'optimal':
            continue

        # work out totol power demand
        total2 = [0.0]*1440
        through2 = sum(b)
        for t in range(144):
            total2[t] += totalH[t]
            for v in range(n):
                total2[t] += x[144*v+t]
                total2[t] -= x[144*(v+n)+t]
                through2 += c_eff*x[144*v+t]/(6) + x[144*(v+n)+t]/(6*c_eff)
              
        g2v.append([max(total1),through1/n])
        v2g.append([max(total2),through2/n])

        
        del A
        del b
        del G
        del h
        del P
        del q
    existing = []
    
    '''
    with open('../../../Documents/simulation_results/NTS/v2g/texas_v2g_lf'+\
              str(int(100*pen))+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            existing.append(row)
    '''
    
    with open('../../../Documents/simulation_results/NTS/v2g/texas_v2g_lf'+\
              str(int(100*pen))+'.csv',
              'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Sim No','Peak Demand (kW)','Throughput (kWh)',
                         'Peak Demand2 (kW)','Throughput2 (kWh)'])
        for row in existing:
            writer.writerow(row)
        for i in range(len(g2v)):
            writer.writerow([i]+g2v[i]+v2g[i])
