import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

charge_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'

trip_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

outstem = '../../Documents/simulation_results/NTS/clustering/power/'
# First get the pdfs for charging
pdfs = {'0':{},'1':{}}
pdfs_ = {'0':{},'1':{}}
for d in ['0','1']:
    for i in range(3):
        pdfs[d][i] = {}
        for s in range(6):
            pdfs[d][i][s] = [0]*48
    for s in range(6):
        pdfs_[d][s] = [0]*48

stm = {'0':'jointPdfW','1':'jointPdfWE'}
for d in ['0','1']:
    for i in range(3):       
        with open(stem+stm[d]+str(i+1)+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            s = 0
            for row in reader:
                for t in range(48):
                    pdfs[d][i][s][t] = float(row[t])
                s += 1
                
    with open(stem+stm[d]+'_.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        s = 0
        for row in reader:
            for t in range(48):
                pdfs_[d][s][t] = float(row[t])
            s += 1

def chargeAfterJourney(d,k,s,t):
    if random.random() < pdfs[d][k][s][t]:
        return True
    else:
        return False
        
def randomCharge(d,s,t):
    if random.random() < pdfs_[d][s][t]/30:
        return True
    else:
        return False

def normalise(x):
    s = sum(x)
    for i in range(len(x)):
        x[i] = x[i]/s
    return x
    
# Then get the NTS vehicle labels, and the household to vehicle list
MEA = {}
with open(stem+'MEAlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA[row[0]] = int(row[1])
with open(stem+'MEAlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA[row[0]] = int(row[1])


# How will things change for the test?
journeyLogs = {}
dType = {}
with open(trip_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]
        if vehicle not in journeyLogs:
            journeyLogs[vehicle] = []
            dType[vehicle] = {}

        day = int(row[1])
        start = int(row[2])
        end = int(row[3])
        dType[vehicle][day] = row[-1]

        if start > end:
            end += 1440
        kWh = float(row[-2])/1000

        journeyLogs[vehicle].append([day,start,end,kWh,dType])

def step(t,d):
    t += 1
    if t >= 1440:
        t = 0
        d += 1
    return [t,d]
    
'''
# now get the MEA data
with open(charge_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        #soc = float(row[4])
        start = int(row[2])
        end = int(row[3])
        if row[-1] == '0':
            true[int(start/30)] += 1
            for t in range(start,end):
                try:
                    true2[int(t/30)] += 1
                except:
                    true2[int(t/30)-48] += 1
        else:
            trueWE[int(start/30)] += 1
            for t in range(start,end):
                try:
                    trueWE2[int(t/30)] += 1
                except:
                    trueWE2[int(t/30)-48] += 1
'''
pred_charges = []
for i in range(1):
    for vehicle in journeyLogs:
        jLog = sorted(journeyLogs[vehicle])
        d = jLog[0][0]
        t = jLog[0][1]
        j = 0
        SOC = 0.99
        capacity = 24
        startCharge = False

        while d < jLog[-1][0]:
            if vehicle == '':
                print([d,t])
                print(jLog[j][0:2])
                print('')
            startCharge = False
            while (t < jLog[j][1] or d < jLog[j][0]) and startCharge == False:
                [t,d] = step(t,d)
                try:
                    startCharge = randomCharge(dType[vehicle][d],int(SOC*6),
                                               int(t/30))
                except:
                    startCharge = False
                if startCharge == True:
                    pred_charges.append([vehicle,d,t,SOC,'r'])

            if t == jLog[j][1] and d == jLog[j][0]:
                SOC -= jLog[j][3]/capacity
                if SOC < 0:
                    SOC = 0
                t = jLog[j][2]
                if t >= 1440:
                    t -= 1440
                    d += 1
                j += 1

                try:
                    k = MEA[vehicle+str(int(t/1440)+1)] # check - days in 0?!
                except:
                    k = int(random.random()*3) # hack
                try:
                    dt = dType[vehicle][day]
                except:
                    dt = '0'

                startCharge = chargeAfterJourney(dt,k,int(SOC*6),int(t/30))
                if startCharge == True:
                    pred_charges.append([vehicle,d,t,SOC,'aj'])

            if startCharge == True:
                try:
                    dt = dType[vehicle][day]
                except:
                    dt = '0'
                if dt == '0':
                    t2 = t
                    while SOC <= 0.99:
                        SOC += 3.5/(60*capacity)
                        t2 += 1
                        if t2 == 1440:
                            t2 = 0
                else:
                    t2 = t
                    while SOC <= 0.99:
                        SOC += 3.5/(60*capacity)
                        t2 += 1
                        if t2 == 1440:
                            t2 = 0
                SOC = 0.99
                startCharge = False

            if j == len(jLog)-1:
                d = jLog[-1][0]

            if t >= jLog[j][1] and d >= jLog[j][0]:
                j += 1

with open('../../Documents/My_Electric_Avenue_Technical_Data/pred_charges.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for row in pred_charges:
        writer.writerow(row)
with open('../../Documents/My_Electric_Avenue_Technical_Data/d_type.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for v in dType:
        for d in dType[v]:
            writer.writerow([v,d,dType[v]])
    
