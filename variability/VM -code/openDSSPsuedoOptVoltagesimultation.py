##import sys
##sys.path.append('C:\Users\Constance\Anaconda2\Lib\site-packages')

# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import sys
import win32com.client

withEVs = True

highOut = 'PsOpthighest_with_evs.csv'
lowOut = 'PsOptlowest_with_evs.csv'

household_profiles = []
vehicle_profiles = []

for i in range(0,1000):
    household_profiles.append([0.0]*1440)
    vehicle_profiles.append([0.0]*1440)

i = 0
with open('household_demand_pool.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row == []:
            continue
        for j in range(0,1000):
            household_profiles[j][i] = float(row[j])
        i += 1

if withEVs == True:
    i = 0
    with open('vehicle_demand_poolPO.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            for j in range(0,1440):
                vehicle_profiles[i][j] = float(row[j])
            i += 1

            
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

    for i in range(1,56):
        with open('household-profiles/'+str(i)+'.csv','w') as csvfile:
            writer = csv.writer(csvfile)
            for j in range(0,1440):
                writer.writerow([household_profiles[chosen[i-1]][j]+\
                                 vehicle_profiles[chosenV[i-1]][j]])
                                     

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

# New Loadshape.Shape_1 npts=1440 minterval=1 csvfile='' useactual=true
