import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag, sparse, solvers

# ok here is how it's going to go.
simulationDay = 3
nMC = 800
nH = 50
c_eff = 0.9
capacity = 30 # kWh
pMax = 7.0 # kW
pMax_ = 7.0 # kW for V2G

'''
This is the right one

'''

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
        if random.random() > 0.01:
            continue
        p = []
        for t in range(48):
            p.append(float(row[2+t]))
        hhProfiles[c] = p
        c += 1

for pen in np.arange(0.1,1.1,0.1):
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

            b.append(kWh)

        n = len(b)
        if n == 0:
            continue
        b = matrix(b+[0.0]*n)
        A = matrix(0.0,(2*n,n*1440+1))
        G = matrix(0.0,(1440,n*1440+1))
        q = matrix([0.0]*(1440*n)+[1.0])
        P = spdiag([0.0001]*(1440*n+1))
        
        for v in range(n):
            for t in range(1440):
                A[v,1440*v+t] = c_eff/60
                A[v+n,1440*v+t] = a_[v][t]
                G[t,1440*v+t] = 1.0
                
        h0 = []
        for t in range(1440):
            G[t,1440*n] = -1.0
            h0.append(-1.0*totalH[t])

        G1 = sparse([[spdiag([-1.0]*(n*1440))],[matrix([0.0]*(n*1440))]])
        G2 = sparse([[spdiag([1.0]*(n*1440))],[matrix([0.0]*(n*1440))]])
        

        G = sparse([G,G1,G2])
        h = matrix(h0+[0.0]*(n*1440)+[pMax]*(n*1440))

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
            total1[t] += totalH[t]
            for v in range(n):
                total1[t] += x[1440*v+t]
                through1 += x[1440*v+t]*c_eff/60
                
        del A
        del G
        del h
        del P
        del q
                
        # I think I actually need to reformulate for V2G,
        # defining seperate variables for charigng and discharging
        
        A = matrix(0.0,(2*n,2*n*1440+1))
        G = matrix(0.0,(1440,2*n*1440+1))
        P = spdiag([0.0001]*(1440*2*n+1))
        q = matrix([0.0]*(1440*2*n)+[1.0])

        for v in range(n):
            for t in range(1440):
                A[v,1440*v+t] = c_eff/60 # incorporate efficiency here also?
                A[v,1440*(n+v)+t] = -1/(60*c_eff)
                
                A[v+n,1440*v+t] = a_[v][t]
                A[v+n,1440*(n+v)+t] = a_[v][t]

                G[t,1440*v+t] = 1.0
                G[t,1440*(n+v)+t] = -1.0

        for t in range(1440):
            G[t,1440*2*n] = -1.0

        G1 = sparse([[spdiag([-1.0]*(2*n*1440))],[matrix([0.0]*(2*n*1440))]])
        G2 = sparse([[spdiag([1.0]*(2*n*1440))],[matrix([0.0]*(2*n*1440))]])
        
        G = sparse([G,G1,G2])
        h = matrix(h0+[0.0]*(2*n*1440)+[pMax]*(n*1440)+[pMax_]*(n*1440))
                
        '''
        G = sparse([spdiag([-1.0]*(2*n*1440)),spdiag([1.0]*(2*n*1440))])
        h = matrix([0.0]*(2*n*1440)+[pMax]*(n*1440)+[pMax_]*(n*1440))
        
        totalH_ = []
        for i in range(len(totalH)):
            totalH_.append(-1*totalH[i]+0.001) # epsilon... I need to check this

        q = matrix(totalH*n+totalH_*n)
        

        P1 = sparse([[spdiag([1]*1440)]*n]*n)
        P2 = sparse([[spdiag([-1]*1440)]*n]*n)

        P = sparse([[P1,P2],[P2,P1]])
        '''
        
        sol=solvers.qp(P,q,G,h,A,b)

        x = sol['x'] # with V2G

        if sol['status'] != 'optimal':
            continue


        # work out totol power demand
        total2 = [0.0]*1440
        through2 = sum(b)
        for t in range(1440):
            total2[t] += totalH[t]
            for v in range(n):
                total2[t] += x[1440*v+t]
                total2[t] -= x[1440*(v+n)+t]
                through2 += c_eff*x[1440*v+t]/(60) + x[1440*(v+n)+t]/(60*c_eff)
                
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
    with open('../../../Documents/simulation_results/NTS/v2g/v2g_lf'+\
              str(int(100*pen))+'.csv',
              'rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            existing.append(row)
    '''

    with open('../../../Documents/simulation_results/NTS/v2g/v2g_lf'+\
              str(int(100*pen))+'.csv',
              'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Sim No','Peak Demand (kW)','Throughput (kWh)',
                         'Peak Demand2 (kW)','Throughput2 (kWh)'])
        for row in existing:
            writer.writerow(row)
        for i in range(len(g2v)):
            writer.writerow([i]+g2v[i]+v2g[i])
        
plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'

lbls = {'':'UK','texas_':'Texas'}

for loc in ['','texas_']:
    bnft = []
    cost = []
    bnft_u = []
    cost_u = []
    bnft_l = []
    cost_l = []

    conf = 0.75
    for pen in range(10,110,10):
        a = []
        b = []
        with open('../../../Documents/simulation_results/NTS/v2g/'+loc+\
                  'v2g_lf'+str(pen)+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                a.append(100*(float(row[1])-float(row[3]))/float(row[1]))
                try:
                    b.append(100*(float(row[4])-float(row[2]))/float(row[2]))
                except:
                    b.append(0.0)
        '''           
        bnft.append(sum(a)/len(a))
        cost.append(sum(b)/len(b))
        '''
        a = sorted(a)
        b = sorted(b)
        bnft_u.append(a[int(conf*len(a))])
        cost_u.append(b[int(conf*len(b))])
        bnft_l.append(a[int((1-conf)*len(a))])
        cost_l.append(b[int((1-conf)*len(b))])
        bnft.append(a[int(0.5*len(a))])
        cost.append(b[int(0.5*len(b))])
        
    #bnft = filt.gaussian_filter1d(bnft,1)
    #cost = filt.gaussian_filter1d(cost,1)
    plt.subplot(2,1,1)
    plt.plot(range(10,110,10),bnft)
    plt.xlim(10,100)
    plt.ylim(0,30)
    plt.fill_between(range(10,110,10),bnft_l,bnft_u,alpha=0.2)
    plt.ylabel('% Reduction in\nPeak Demand')
    if loc == '':
        plt.grid()
    plt.subplot(2,1,2)
    plt.plot(range(10,110,10),cost,label=lbls[loc])
    plt.xlim(10,100)
    plt.ylim(0,300)
    plt.fill_between(range(10,110,10),cost_l,cost_u,alpha=0.2)
    plt.ylabel('% Increase in\nBattery Throughput')
    if loc == '':
        plt.grid()
    plt.xlabel('% EV Penetration')
    plt.tight_layout()
plt.legend()
plt.savefig('../../../Dropbox/papers/PES-GM-19/img/results.eps',
            format='eps', dpi=1000)
                  

