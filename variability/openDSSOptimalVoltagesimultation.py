# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import sys
import win32com.client
from cvxopt import matrix, spdiag, solvers, sparse

highOut = 'highest_with_evs_opt.csv'
lowOut = 'lowest_with_evs_opt.csv'

household_profiles = []
vehicle_profiles = []

for i in range(0,1000):
    household_profiles.append([0.0]*1440)
    vehicle_profiles.append([0.0]*1440)

i = 0
with open('household_demand_pool.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for j in range(0,1000):
            household_profiles[j][i] = float(row[j])
        i += 1

i = 0
with open('vehicle_demand_pool.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for j in range(0,1440):
            vehicle_profiles[i][j] = float(row[i])
        i += 1

vehicle_req = []
for profile in vehicle_profiles:
    start = 0
    energy = sum(profile) #kW-min

    if energy == 0:
        vehicle_req.append([0,0.0])
        continue

    while profile[start] == 0:
        start += 1

    vehicle_req.append([start,energy])

del(vehicle_profiles)

engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
engine.Start("0")

L = []
H = []

# I want to do this first without EVs, then with
for mc in range(0,100):

    # pick the household demand profiles
    chosen = []
    while len(chosen) < 55:
        ran = int(random.random()*1000)
        if ran not in chosen:
            chosen.append(ran)

    chosenV = []
    while len(chosenV) < 55:
        ran = int(random.random()*1000)
        if ran not in chosenV:
            chosenV.append(ran)

    # here the optimisation happens

    # first calculate base load
    baseLoad = [0.0]*1440

    for i in range(0,1440):
        for j in range(0,len(chosen)):
            baseLoad[i] += household_profiles[chosen[j]][i]

    # then collect energy and timing requirements
    b = []
    t_av = []

    unused = []

    t = 1440 # may want to change this...

    for i in range(0,len(chosenV)):

        if vehicle_req[chosenV[i]][1] == 0:
            unused.append(i)
            continue
        b.append(vehicle_req[chosenV[i]][1])
        t_av.append(vehicle_req[chosenV[i]][0])

    A1 = matrix(0.0,(len(b),t*len(b))) # ensures right amount of energy provided
    A2 = matrix(0.0,(len(b),t*len(b))) # ensures vehicle only charges when avaliable

    n = len(chosenV)-len(unused)
    
    b += [0.0]*len(b)
    b = matrix(b)

    skp = 0
    for j in range(0,len(chosenV)):
        if j in unused:
            skp += 1
            continue

        arrival = t_av[j-skp]

        for i in range(0,t):
            A1[n*(t*j+i)+j] = 1.0

            if i < arrival:
                A2[n*(t*j+i)+j] = 1.0

    A = sparse([A1,A2])

    A3 = spdiag([-1]*(t*n)) # ensures non-negative charging power
    A4 = spdiag([1]*(t*n)) # ensures charging powers less than pMax
    G = sparse([A3,A4])

    h = []
    for i in range(0,t*n):
        h.append(0.0)
    for i in range(0,t*n):
        h.append(3.5)

    h = matrix(h)

    q = [] # incorporates base load into the objective function
    for i in range(0,n):
        for j in range(0,len(baseLoad)):
            q.append(baseLoad[j])

    q = matrix(q)

    I = spdiag([1]*t)
    P = sparse([[I]*n]*n)

    sol = solvers.qp(P,q,G,h,A,b) # solve quadratic program
    X = sol['x']

    optimal_profiles = []

    v = 0
    for i in range(0,len(chosenV)):
        if i in unused:
            optimal_profiles.append([0.0]*t)
            continue
        
        load = []
        for j in range(0,t):
            load.append(X[v*t+j]) # extract each vehicles load
        optimal_profiles.append(load)
        v += 1

    for i in range(1,56):
        with open('household-profiles/'+str(i)+'.csv','w') as csvfile:
            writer = csv.writer(csvfile)
            for j in range(0,1440):
                writer.writerow([household_profiles[chosen[i-1]][j]+
                                 optimal_profiles[i-1][j]])                                     

    lowest = [1000.0]*1440
    highest = [0.0]*1440

    engine.text.Command='clear'
    circuit = engine.ActiveCircuit

    #engine.Text.Command='Redirect LoadShapes' + shape + '.txt'

    engine.text.Command='compile master.dss'

    for line in range(1,906):
        engine.Text.Command='Export mon LINE'+str(line)+'_VI_vs_Time'

        t = 0

        with open('LVTest_Mon_line'+str(line)+'_vi_vs_time.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                v1 = float(row[2])
                v2 = float(row[4])
                v3 = float(row[6])

                for v in [v1,v2,v3]:
                    if v <= lowest[t]:
                        lowest[t] = v
                    if v >= highest[t]:
                        highest[t] = v

                t += 1

    L.append(lowest)
    H.append(highest)

# transpose for conveniencce
newL = []
newH = []

for i in range(0,1440):
    newL.append([0]*len(L))
    newH.append([0]*len(L))

for i in range(0,1440):
    for j in range(0,len(L)):
        newL[i][j] = L[j][i]
        newH[i][j] = H[j][i]
    
with open(lowOut,'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in newL:
        writer.writerow(row)
with open(highOut,'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in newH:
        writer.writerow(row)


