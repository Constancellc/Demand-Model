import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
import scipy.ndimage.filters as filt
from clustering import Cluster, ClusteringExercise

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

stem = '../../Documents/simulation_results/NTS/clustering/labels/'

assumed_capacity = 30 # kWh
assumed_charge_power = 3.5 # kW
assumed_kwh_limit = 25
def normalise(pdf):
    s = sum(pdf)
    for i in range(len(pdf)):
        pdf[i] = pdf[i]/s

def sample(pdf):
    if sum(pdf) == 0:
        return int(random.random()*len(pdf))
    x = 0
    ran = random.random()
    while sum(pdf[:x]) <= ran:
        x += 1
    return x
        
# get cluster labels
labels = {}
allVehicles = []
found = {}
# get the labels for both data types
with open(stem+'NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # reminder that row[0] contains the vehicle id + the day of week
        labels[row[0]] = int(row[1])
        v = row[0][:-1]
        if v not in found:
            allVehicles.append(v)
            found[v] = 0
del found

# get all charging pdfs
chargePdf = {0:[],1:[],2:[]}
chargePdfWE = {0:[],1:[],2:[]}
socPdf = {0:[],1:[],2:[]}
socPdfWE = {0:[],1:[],2:[]}

with open(stem+'chargePdfW.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            for t in range(30):
                chargePdf[i].append(float(row[i+1]))
            
with open(stem+'chargePdfWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            for t in range(30):
                chargePdfWE[i].append(float(row[i+1]))

with open(stem+'socPdfW.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            socPdf[i].append(float(row[i+1]))

with open(stem+'socPdfWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            socPdfWE[i].append(float(row[i+1]))

for pdf in [chargePdf,chargePdfWE,socPdf,socPdfWE]:
    for i in range(3):
        normalise(pdf[i])

# function defs go here
def get_charge_pdf(clst,typ,home,endTimes):
    if typ == 'W':
        pdf2 = copy.deepcopy(chargePdf[clst])
    elif typ == 'WE':
        pdf2 = copy.deepcpoy(chargePdfWE[clst])

    # first set all times not at home to 0
    for t in range(len(pdf2)):
        if home[t] == 0:
            pdf2[t] = 0

    # then scale all of the endTimes to be 0.7 and the others to be 0.3
    s1 = 0
    s2 = 0
    for t in range(len(pdf2)):
        if t in endTimes:
            s1 += pdf2[t]
        else:
            s2 += pdf2[t]
            
    if s1 == 0 and s2 == 0:
        return pdf2
    elif s1 == 0 or s2 == 0:
        normalise(pdf2)
    else:
        for t in range(len(pdf2)):
            if t in endTimes:
                pdf2[t] = pdf2[t]*0.7/s1
            else:
                pdf2[t] = pdf2[t]*0.3/s2
        normalise(pdf2)

    return pdf2

def get_charge_times(pdf2,kWh0,day,clst,typ,log):
    cTimes = []
    # sample a charge start time pdf

    # ok, first sample

    completed = []

    for charge_sample in range(3):
        kWh = copy.deepcopy(kWh0)
        for c in completed:
            kWh -= c
            
        cT = sample(pdf2)
        nextUsed = 1440*(day+1)

        # work out the kWh consumed by that point
        for j in log:
            if j[1] > day*1440 and j[1] < cT+day*1440:
                kWh += j[2]
                
            elif j[0] > cT+day*1440 and j[0] < nextUsed:
                nextUsed = j[0]
                
        SOC = 100-(100*kWh/assumed_capacity)

        if typ == 'W':
            SOCmin = sample(socPdf[clst])
        elif typ == 'WE':
            SOCmin = sample(socPdfWE[clst])

        if SOC < SOCmin:
            # start charging
            t = cT
            c = 0
            while kWh > 0 and t < nextUsed:
                c += assumed_charge_power/60
                kWh -= assumed_charge_power/60
                t += 1

            if c > 0:
                cTimes.append([cT,t])
                completed.append(c)

    return cTimes
        
# first get all vehicle usage and locations
journeyLogs = {}
with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[2]+row[6] not in labels:
            continue
        vehicle = row[2]
        day = int(row[6])

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

        start += 1440*(day-1)
        end += 1440*(day-1)
        
        if vehicle not in journeyLogs:
            journeyLogs[vehicle] = []

        journeyLogs[vehicle].append([start,end,kWh,purpose])
                        
# then for each simulation
nV = 50
print(len(allVehicles))
sim_results = []
sim_control = []
for mc in range(20):
    charging = [0]*8440
    dumb_charging = [0]*8440
    # randomly choose vehicles
    chosen = []
    while len(chosen) < nV:
        ran = int(random.random()*len(allVehicles))
        if allVehicles[ran] not in chosen:
            chosen.append(allVehicles[ran])

    for vehicle in chosen:
        home = [1]*7200
        endTimes = [[],[],[],[],[]]
        kWh = 0

        for i in range(len(journeyLogs[vehicle])):
            j = journeyLogs[vehicle][i]
            start = j[0]
            end = j[1]

            day = int(end/1440)
            if day < 5:
                endTimes[day].append(end%1440)

            for t in range(start,end):
                try:
                    home[t] = 0
                except:
                    continue

            if j[3] != '23' and i <len(journeyLogs[vehicle])-1:
                for t in range(end,journeyLogs[vehicle][i+1][0]):
                    try:
                        home[t] = 0
                    except:
                        continue
            
        for day in range(5):
            if kWh > assumed_kwh_limit: # hack but potentially justified 
                kWh = assumed_kwh_limit
            try:
                clst = labels[vehicle+str(day+1)]
            except:
                continue
            home2 = home[1440*day:1440*(day+1)]
            pdf2 = get_charge_pdf(clst,'W',home2,endTimes[day])

            kWh0 = copy.deepcopy(kWh)
            chargeTimes = get_charge_times(pdf2,kWh0,day,clst,'W',
                                           journeyLogs[vehicle])

            kWh2 = 0
            # add days journeys to kWh
            for j in journeyLogs[vehicle]:
                if j[1] > 1440*day and t < 1440*(day+1):
                    kWh += j[2]
                    kWh2 += j[2]
            if kWh2 > assumed_kwh_limit:
                kWh2 = assumed_kwh_limit
                    
            # implement charges
            for charge in chargeTimes:
                for t in range(charge[0],charge[1]):
                    if t+day*1440 < len(charging)-1:
                        charging[t+day*1440] += assumed_charge_power
                        kWh -= assumed_charge_power/60
                    
            del pdf2
            try:
                t = endTimes[day][-1]+1440*day
            except:
                t = 1440*day
                
            while kWh2 > 0 and t < 8000:
                kWh2 -= assumed_charge_power/60
                dumb_charging[t] += assumed_charge_power
                t += 1

    sim_results.append(charging)
    sim_control.append(dumb_charging)


with open('50evs.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t']+list(range(len(sim_results))))
    for t in range(1440*4):
        row = [t+1440]
        for i in range(len(sim_results)):
            row.append(sim_results[i][t+1440])
        writer.writerow(row)


with open('50evsCtrl.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t']+list(range(len(sim_results))))
    for t in range(1440*4):
        row = [t+1440]
        for i in range(len(sim_control)):
            row.append(sim_control[i][t+1440])
        writer.writerow(row)
