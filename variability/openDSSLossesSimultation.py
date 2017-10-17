# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import sys
import win32com.client

outStem = '%ev_losses.csv'

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

engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
engine.Start("0")


for pen in [0.0,1.0]:
    L = []
    
    # I want to do this first without EVs, then with
    for mc in range(0,100):
        powerOut = [0.0]*1440
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
                    if random.random() >= pen:
                        powerOut[j] += household_profiles[chosen[i-1]][j]
                        writer.writerow([household_profiles[chosen[i-1]][j]])
                    else:
                        powerOut[j] += household_profiles[chosen[i-1]][j]+\
                                       vehicle_profiles[chosenV[i-1]][j]
                        writer.writerow([household_profiles[chosen[i-1]][j]+
                                         vehicle_profiles[chosenV[i-1]][j]])
                                         

        lowest = [1000.0]*1440
        highest = [0.0]*1440

        engine.text.Command='clear'
        circuit = engine.ActiveCircuit

        #engine.Text.Command='Redirect LoadShapes' + shape + '.txt'

        engine.text.Command='compile master.dss'

        engine.Text.Command='Export mon LINE1_PQ_vs_Time'

        powerIn = [0.0]*1440

        with open('LVTest_Mon_line1_pq_vs_time.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            i = 0
            for row in reader:
                powerIn[i] -= float(row[2])
                powerIn[i] -= float(row[4])
                powerIn[i] -= float(row[6])
                i += 1
        net = []
        for i in range(0,1440):
            net.append(powerIn[i]-powerOut[i])

        L.append(net)

    newL = []
    for i in range(0,1440):
        newL.append([0.0]*len(L))

    for i in range(0,len(L)):
        for j in range(0,1440):
            newL[j][i] = L[i][j]
            
    with open(str(int(100*pen))+outStem,'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in newL:
            writer.writerow(row)

            

