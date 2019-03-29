import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag, sparse, solvers


solvers.options['show_progress'] = False

# ok here is how it's going to go.
simulationDay = 3
nMC = 100
nH = 311
c_eff = 0.9 
pMax = 7 # kW G2V
pMax_ = 7 # kW V2G
capacity = 30 # kWh
t_res = 30

# get losses cost matricies
with open('epriK1/c.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        _c = float(row[0])

    _q = []
    with open('epriK1/q.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            _q.append(float(row[0]))
    _q = matrix(_q)

    _P = matrix(0.0,(nH,nH))
    with open('epriK1/P.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        for row in reader:
            for j in range(len(row)):
                _P[i,j] += float(row[j])
            i += 1
            
def getLosses(_profiles,t_res):

    if t_res == 1:
        profiles = _profiles
    else:
        profiles = []
        for i in range(len(_profiles)):
            p = interpolate(_profiles[i],t_res)
            profiles.append(p)
        
    # profiles will be a list of nH profiles
    losses = 0
    for t in range(1440):
        y = [0]*nH
        for i in range(len(profiles)):
            y[i] -= profiles[i][t]*1000
        y = matrix(y)
        losses += (y.T*_P*y+_q.T*y)[0]+_c
    
    return losses/60000


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
'''        
# get household profiles
c = 0
hhProfiles = {}
with open('../../../Documents/pecan-street/hourly-texas/profiles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = [0.0]*48
        for t in range(48):
            p[t] += float(row[t])
        hhProfiles[c] = p
        c += 1

p_home = [0.95]*2+[1.0]*6+[0.95]*2+[0.9]*2+[0.85,0.8,0.75,0.7,0.6,0.5]+\
         [0.45]*8+[0.5]*4+[0.55,0.6,0.65,0.65,0.7,0.7,0.75,0.75,0.8,0.8]+\
         [0.825,0.85,0.85,0.875,0.9,0.925,0.925,0.95]

for pen in [2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100]:
    pen = pen/100
    g2v = []
    v2g = []
    # For each MC simulation
    for mc in range(nMC):
        chosenH = []
        while len(chosenH) < nH:
            ranH = int(random.random()*len(hhProfiles))
            chosenH.append(ranH)

        totalH = [0.0]*int(1440/t_res)
        for h in chosenH:
            p = copy.deepcopy(hhProfiles[h])#interpolate(hhProfiles[h],int(30/t_res))
            for t in range(int(1440/t_res)):
                totalH[t] += p[t]
        
        nV = int(nH*pen)
        hh_loc = []

        if nV == nH:
            hh_loc = range(nV)

        while len(hh_loc) < nV:
            r = int(random.random()*nH)
            if r not in hh_loc:
                hh_loc.append(r)
                
        a_ = []
        b = []
        for v in range(nV):
            a = []
            for t in range(48):
                if random.random() < p_home[t]:
                    a.append(0)
                else:
                    a.append(1)
            a_.append(a)
            b.append(abs(np.random.normal(9,3)))
            if sum(a)*pMax*0.8*t_res/60 < b[v]:
                b[v] = sum(a)*pMax*0.8*t_res/60 
        '''
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

            a = [0]*int(1440/t_res)
            for i in range(len(c)):
                c_ = c[i]
                if c_[1] != '':
                    for t in range(int(c_[0]/t_res),int(c_[1]/t_res)):
                        if t < int(1440/t_res):
                            a[t] = 1
                elif i < len(c)-1:
                    for t in range(int(c_[0]/t_res),int(c[i+1][0]/t_res)):
                        if t < int(1440/t_res):
                            a[t] = 1
                else:
                    for t in range(int(c_[0]/t_res),int(1440/t_res)):
                        a[t] = 1

            a_.append(a)

            possible_charge = pMax*(int(1440/t_res)-sum(a))*t_res/60
            
            if kWh > capacity:
                kWh = capacity
            if kWh >= possible_charge:
                kWh = possible_charge*0.99

            b.append(kWh)
            '''

        n = len(b)
        if n == 0:
            continue
        b = matrix(b+[0.0]*n)
        A = matrix(0.0,(2*n,n*int(1440/t_res)+1))
        G = matrix(0.0,(int(1440/t_res),n*int(1440/t_res)+1))
        q = matrix([0.0]*(int(1440/t_res)*n)+[1.0])
        P = spdiag([0.0001]*(int(1440/t_res)*n+1))
        
        for v in range(n):
            for t in range(int(1440/t_res)):
                A[v,int(1440/t_res)*v+t] = c_eff*t_res/60
                A[v+n,int(1440/t_res)*v+t] = a_[v][t]
                G[t,int(1440/t_res)*v+t] = 1.0
                
        h0 = []
        for t in range(int(1440/t_res)):
            G[t,int(1440/t_res)*n] = -1.0
            h0.append(-1.0*totalH[t])

        G1 = sparse([[spdiag([-1.0]*(n*int(1440/t_res)))],
                     [matrix([0.0]*(n*int(1440/t_res)))]])
        G2 = sparse([[spdiag([1.0]*(n*int(1440/t_res)))],
                     [matrix([0.0]*(n*int(1440/t_res)))]])
        

        G = sparse([G,G1,G2])
        h = matrix(h0+[0.0]*(n*int(1440/t_res))+[pMax]*(n*int(1440/t_res)))

        try:
            sol=solvers.qp(P,q,G,h,A,b)
        except:
            continue
        
        x = sol['x'] # without V2G

        if sol['status'] != 'optimal':
            continue       

        # work out totol power demand and battery throughput
        total1 = [0.0]*int(1440/t_res)
        profiles = []
        for h in range(nH):
            profiles.append(copy.deepcopy(hhProfiles[chosenH[h]]))

        through1 = sum(b)
        for t in range(int(1440/t_res)):
            total1[t] += totalH[t]
            for v in range(n):
                total1[t] += x[int(1440/t_res)*v+t]
                through1 += x[int(1440/t_res)*v+t]*t_res*c_eff/60
                profiles[hh_loc[v]][t] += x[int(1440/t_res)*v+t]

        losses1 = getLosses(profiles,t_res)
                
        del A
        del G
        del h
        del P
        del q
                
        # I think I actually need to reformulate for V2G,
        # defining seperate variables for charigng and discharging
        
        A = matrix(0.0,(2*n,2*n*int(1440/t_res)+1))
        G = matrix(0.0,(int(1440/t_res),2*n*int(1440/t_res)+1))
        P = spdiag([0.0001]*(int(1440/t_res)*2*n+1))
        q = matrix([0.0]*(int(1440/t_res)*2*n)+[1.0])

        for v in range(n):
            for t in range(int(1440/t_res)):
                A[v,int(1440/t_res)*v+t] = c_eff*t_res/60 # incorporate efficiency here also?
                A[v,int(1440/t_res)*(n+v)+t] = -t_res/(60*c_eff)
                
                A[v+n,int(1440/t_res)*v+t] = a_[v][t]
                A[v+n,int(1440/t_res)*(n+v)+t] = a_[v][t]

                G[t,int(1440/t_res)*v+t] = 1.0
                G[t,int(1440/t_res)*(n+v)+t] = -1.0

        for t in range(int(1440/t_res)):
            G[t,int(1440/t_res)*2*n] = -1.0

        G1 = sparse([[spdiag([-1.0]*(2*n*int(1440/t_res)))],
                     [matrix([0.0]*(2*n*int(1440/t_res)))]])
        G2 = sparse([[spdiag([1.0]*(2*n*int(1440/t_res)))],
                     [matrix([0.0]*(2*n*int(1440/t_res)))]])
        
        G = sparse([G,G1,G2])
        h = matrix(h0+[0.0]*(2*n*int(1440/t_res))+\
                   [pMax]*(n*int(1440/t_res))+[pMax_]*(n*int(1440/t_res)))
        
        sol=solvers.qp(P,q,G,h,A,b)

        x = sol['x'] # with V2G

        if sol['status'] != 'optimal':
            continue

        profiles = []
        for h in range(nH):
            profiles.append(copy.deepcopy(hhProfiles[chosenH[h]]))

        # work out totol power demand
        total2 = [0.0]*int(1440/t_res)
        through2 = sum(b)
        for t in range(int(1440/t_res)):
            total2[t] += totalH[t]
            for v in range(n):
                total2[t] += x[int(1440/t_res)*v+t]
                total2[t] -= x[int(1440/t_res)*(v+n)+t]
                through2 += c_eff*x[int(1440/t_res)*v+t]*t_res/60 +\
                            x[int(1440/t_res)*(v+n)+t]*t_res/(60*c_eff)
                profiles[hh_loc[v]][t] += x[int(1440/t_res)*v+t]
                profiles[hh_loc[v]][t] -= x[int(1440/t_res)*(v+n)+t]


        losses2 = getLosses(profiles,t_res)
              
        g2v.append([max(total1),through1/n,losses1])
        v2g.append([max(total2),through2/n,losses2])
        
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
            existing.append(row)'''
    
    with open('../../../Documents/simulation_results/NTS/v2g/texas_v2g_lf'+\
              str(int(100*pen))+'.csv',
              'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Sim No','Peak Demand (kW)','Throughput (kWh)',
                         'Losses (kWh)','Peak Demand2 (kW)','Throughput2 (kWh)',
                         'Losses2 (kWh)'])
        for row in existing:
            writer.writerow(row)
        for i in range(len(g2v)):
            writer.writerow([i]+g2v[i]+v2g[i])
