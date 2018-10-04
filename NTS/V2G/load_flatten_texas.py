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
#capacity = 30 # kWh
#pMax = 3.5 # kW
#pMax_ = 3.5 # kW for V2G

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

def v2g_eval(hh,e0,delta):
    over = 0
    p = (e0+delta)/24
    for t in range(1440):
        if hh[t] > p:
            over += hh[t]/60
    return over

def flatten_v2g(hh,eV):
    e0 = sum(hh)/60 + eV
    delta = 0
    for i in range(10):
        over = v2g_eval(hh,e0,delta)
        delta = over*(1/0.81-1)

    return [over,[(e0+delta)/24]*1440]

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

# first get hhs and then their energy consumotion

households = []
with open('../../../Documents/NHTS/constance/texas-hh.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if int(row[1]) == simulationDay:
            households.append(row[0])

print(len(households))
en = {}
hh_v = {}
for hh in households:
    en[hh] = 0
    hh_v[hh] = []
    
with open('../../../Documents/NHTS/constance/texas-trips.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        day = int(row[2])
        if day != simulationDay:
            continue
        hh = row[1]
        if hh not in households:
            continue
        v = row[0]
        if v not in hh_v[hh]:
            hh_v[hh].append(v)
        #start = int(row[5])
        #end = int(row[6])

        en[hh] += 0.3*float(row[7])

# Get the HH demand, one from each hh
# get a list of hh?
c = 0
hhProfiles = {}
with open('../../../Documents/pecan-street/1min-texas/profiles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = []
        for t in range(48):
            p.append(float(row[t]))
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
                
        chosenV = []
        nV = 0
        while len(chosenV) < int(nH*pen):
            ranV = households[int(random.random()*len(households))]
            if ranV not in chosenV:
                chosenV.append(en[ranV])
                nV += len(hh_v[ranV])

        if nV == 0:
            g2v.append([max(totalH),0])
            v2g.append([max(totalH),0])
            continue
            
        eV = sum(chosenV)

        [over,tot1] = flatten_v2g(totalH,eV/0.9)
        tot2 = flatten_g2v(totalH,eV/0.9)
        through2 = eV*2
        through1 = eV*2+over*2/0.9

        g2v.append([max(tot2),through2/nV])
        v2g.append([max(tot1),through1/nV])

    existing = []
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
    
