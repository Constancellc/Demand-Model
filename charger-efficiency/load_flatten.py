import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag, sparse, solvers

# ok here is how it's going to go.
simulationDay = 3
nMC = 1
nH = 50
c_eff = 0.9
capacity = 30 # kWh
pMax = 7.0 # kW
pMax_ = 7.0 # kW for V2G


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

'''
TO DO

I need to change the formulation so that after the optimization the vehicle
limits are allocated more accurately

Can I think of a better way that the

Incorporation of teh distribution losses

It might be good to go to 1 min load data in this case, maybe from network rev?

'''



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


for pen in [0.5]:
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
            #vCon.append({})
            #for t in range(48):
            #    vCon[v][t] = []
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
                            #vCon[v][int(t/30)].append(t%30)
                            a[t] = 1
                elif i < len(c)-1:
                    for t in range(c_[0],c[i+1][0]):
                        if t < 1440:
                            #vCon[v][int(t/30)].append(t%30)
                            a[t] = 1
                else:
                    for t in range(c_[0],1440):
                        #vCon[v][int(t/30)].append(t%30)
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
        b = matrix(b_+[0.0]*n)
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

        sol=solvers.qp(P,q,G,h,A,b)
        
        x = sol['x'] # original method

        # work out totol power demand and battery throughput
        total1 = [0.0]*1440
        individuals1 = []
        for v in range(n):
            individuals1.append([])
        for t in range(1440):
            total1[t] += totalH[t]
            for v in range(n):
                total1[t] += x[1440*v+t]
                individuals1[v].append(x[1440*v+t])
                
        del A
        del G
        del h
        del P
        del q

        # for the second optimization the decision variable will be the minutes
        # within each half hour that the vehicle was charging

        # b will contain the number of minutes charging required (incl eff)

        # h will BOTH contain the limit thing and the number of
        
        G = matrix(0.0,(48,n*48+1))
        
        A = matrix(0.0,(n,n*48+1))
        G = matrix(0.0,(48,n*48+1))
        q = matrix([0.0]*(48*n)+[1.0])
        P = spdiag([0.0001]*(48*n+1))

        for v in range(n):
            for t in range(48):
                A[v,48*v+t] = c_eff*pMax/60
                G[t,48*v+t] = pMax/30
                
        h = []
        for t in range(48):
            G[t,48*n] = -1.0
            h_ = 0
            for t2 in range(30):
                h_ += -1.0*totalH[t*30+t2]/30
            h.append(h_)
        
        for v in range(n):
            h_ = [30]*48
            for t in range(1440):
                h_[int(t/30)] -= a_[v][t]
            h += h_

        h = matrix(h+[0.0]*(n*48))
        b = matrix(b_)
        
        G1 = sparse([[spdiag([1.0]*(n*48))],[matrix([0.0]*(n*48))]])
        G2 = sparse([[spdiag([-1.0]*(n*48))],[matrix([0.0]*(n*48))]])

        G = sparse([G,G1,G2])

        print(A.size)
        print(b.size)
        print(G.size)
        print(h.size)
        print(P.size)
        print(q.size)

        sol=solvers.qp(P,q,G,h,A,b)
        
        x = sol['x'] # new method

        # ok, first I need to seperate out the individual profiles

        total2 = [0.0]*1440
        for t in range(1440):
            total2[t] += totalH[t]

        '''

        individuals2 = []
        for i in range(v):
            individuals2.append([0]*1440)

        # for each time interval
        for t in range(48):
            veh = []                            

            # get all vehicles and order them by their floats
            for v in range(n):
                minC = x[v*48+t]
                maxC = h[48+v*48+t]
                veh.append([maxC-minC,v])
            veh = sorted(veh)

            # work out the ideal shape which the vehices should fill
            cumulative = []

            for i in range(len(veh)):
                v = veh[i][1]
                f = veh[i][0]
                minC = x[v*48+t]
                maxC = h[48+v*48+t]

                # get time constraints
                con = vCon[v][t]

                # these are a list of the times within the half hour which
                # cannot be charged

                if con == []:
                    frst = 0
                    lst = 29

                if 0 in con:
                    frst = max(con)+1
                    lst = 29
                elif 29 in co:
                    frst = 0
                    lst = min(con)-1

                if f == 0:
                    for t_ in range(minC):
                        cumulative[v][t*48+t_] -= 1
                        individuals[v][t*48+t_] += pMax

                else:
                    # find best time to allocate                   

        '''
        

        # then step through allocating charge to vehicles in order of most
        # constrained to least constrained
        '''
        individuals2 = []
        for v in range(n):
            individuals2.append([])
            for t in range(48):
                minCharged = x[v*48+t]
                if minCharged == 0:
                    individuals2[v] += [0]*30
                    continue
                elif minCharged == 30:
                    individuals2[v] += [pMax]*30
                    continue
                maxCharged = h[48+v*48+t]

                flt = maxCharged-minCharged
                wait = int(random.random()*flt)

                new = [0]*30

                for t in range(int(round(minCharged,0))):
                    new[int(t+wait+30-maxCharged)] = pMax
                individuals2[v] += new
        '''
        individuals2 = []
        for v in range(n):
            individuals2.append([])
            for t in range(48):
                minCharged = int(round(x[v*48+t],0))
                wait = int(random.random()*30)

                new = [0]*30
                for t_ in range(wait,wait+minCharged):
                    if t_ < 30:
                        new[t_] += pMax
                    else:
                        new[t_-30] += pMax
                    
                individuals2[v] += new

            for t in range(1440):
                total2[t] += individuals2[v][t]

plt.figure()
plt.subplot(2,1,1)
plt.plot(total1)
plt.plot(totalH,ls=':',c='k')
plt.plot(total2)

totalH30 = [0]*48
total130 = [0]*48
total230 = [0]*48
for t in range(1440):
    totalH30[int(t/30)] += totalH[t]/30
    total130[int(t/30)] += total1[t]/30
    total230[int(t/30)] += total2[t]/30


plt.subplot(2,1,2)
plt.plot(total130)
plt.plot(totalH30,ls=':',c='k')
plt.plot(total230)
plt.show()
        
                

