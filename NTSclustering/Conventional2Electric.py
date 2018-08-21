import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

#data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

NTS = {}
NTS_ = {0:[],1:[],2:[],3:[],4:[]}
# get the labels for the conventional data
with open('NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS_[int(row[1])].append(row[0])
        NTS[row[0]] = int(row[1])

# get all of the pdfs
clusterPdf = []
chargingPdf = []
clusterPdf2 = [] # for weekend
chargingPdf2 = []
for i in range(5):
    chargingPdf.append([])
    chargingPdf2.append([])

with open('clusterPdf.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        clusterPdf.append(float(row[1])/100)

with open('clusterPdfWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        clusterPdf2.append(float(row[1])/100)

with open('chargePdfW.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(5):
            for t in range(30):
                chargingPdf[i].append(float(row[i+1])/3000)
            
with open('chargePdfWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(5):
            for t in range(30):
                chargingPdf2[i].append(float(row[i+1])/3000)


nV = 50
nSim = 20
cluster_n = [0]*5

clPdf = clusterPdf
chPdf = chargingPdf
days = [1,2,3,4,5]
'''
clPdf = clusterPdf2
chPdf = chargingPdf2
days = [6,7]
'''
for v in range(nV):
    ran = random.random()
    i = 0
    while sum(clPdf[:i]) < ran:
        i += 1
    cluster_n[i-1] += 1

sim_results = []
sim_control = []

for sim in range(nSim):
    chosen = []
    for i in range(5):
        if cluster_n[i] == 0:
            continue
        shortlist = NTS_[i]
        np.random.shuffle(shortlist)
        for v in range(cluster_n[i]):
            chosen.append(shortlist[v])

    journeyLogs = {}
    locations = {}
    for v in chosen:
        journeyLogs[v] = []
        for d in range(5):
            locations[v+str(d+1)] = ['-1']*1440
            journeyLogs[v].append([])
        
    # get conventional vehicles' usage
    with open(data,'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            vehicle = row[2]
            if vehicle not in chosen:
                continue
            day = int(row[6])
            if day not in days:
                continue

            try:
                start = int(30*int(int(row[9])/30)+30*random.random())
                end = int(30*int(int(row[10])/30)+30*random.random())
                distance = float(row[11]) # miles
            except:
                continue

            purposeTo = row[-2]
            for t in range(start,end):
                if t < 1440:
                    locations[vehicle+str(day)][t] = '0'
                else:
                    try:
                        locations[vehicle+str(day+1)][t-1440] = '0'
                    except:
                        continue
            if end < 1440:
                locations[vehicle+str(day)][end] = purposeTo
            else:
                try:
                    locations[vehicle+str(day+1)][end-1440] = purposeTo
                except:
                    continue
            
            kWh = distance*0.3 # basic bitch approx

            journeyLogs[vehicle][day-1].append([start,end,kWh,purposeTo])

    # find charging using the dumb assumption
    charging = [0.0]*1440*6
    for v in journeyLogs:
        for d in range(5):
            if len(journeyLogs[v][d]) == 0:
                continue
            kWh = 0
            for i in range(len(journeyLogs[v][d])):
                kWh += journeyLogs[v][d][i][2]
            c_length = int(60*kWh/3.5)
            c_start = journeyLogs[v][d][-1][1]+1440*d

            for t in range(c_start,c_start+c_length):
                try:
                    charging[t] += 3.5
                except:
                    continue
    sim_control.append(charging)
    
    # post processing the locations
    for d in locations:
        t = 0
        while locations[d][t] == '-1' and t < 1438:
            locations[d][t] = '23'
            t += 1
        while t < 1439:
            while locations[d][t] == '0' and t < 1438:
                t += 1
            new = locations[d][t]
            t += 1
            while locations[d][t] == '-1' and t < 1438:
                locations[d][t] = new
                t += 1

    chargeLog = {}
    for v in chosen:
        chargeLog[v] = []
        later = 0
        
        pdf = []
        p = copy.deepcopy(chPdf[NTS[v]])
        for d in range(5):
            pdf += p

            for t in range(1440):
                if locations[v+str(d+1)][t] != '23':
                    pdf[d*1440+t] = 0
                    
        # for each day generate a pdf from the first journey today to first tomorrow
        for d in range(5):

            if journeyLogs[v][d] == []:
                continue

            t0 = journeyLogs[v][d][0][0]+1440*d

            try:
                t1 = journeyLogs[v][d+1][0][0]+1440*(d+1)
            except:
                t1 = 1440*(d+2)

            p2 = copy.deepcopy(pdf[t0:t1])

            # normalise
            S = sum(p2)

            if sum(p2) == 0:# BUG SOMETHING ELSE WOULD BE BETTER
                continue
            
            for t in range(len(p2)):
                p2[t] = p2[t]/S

            # randomly sample for first charge time
            ran = random.random()
            t = 0
            while sum(p2[:t]) < ran:
                t += 1

            t_charge = t0+t

            now = later
            later = 0

            for j in journeyLogs[v][d]:
                if j[1] < t_charge:
                    now += j[2]
                else:
                    later += j[2]

            charge_length = int(60*(now/3.5))

            if t_charge+charge_length < t1:
                chargeLog[v].append([t_charge,t_charge+charge_length])
                now = 0
            else:
                chargeLog[v].append([t_charge,t1])
                now -= 3.5*(t1-t_charge)/60
            '''
            if later > 0 and now == 0:
                p3 = copy.deepcopy(pdf[journeyLogs[v][d][-1][1]:t1])

                if len(p3) < 60:
                    continue
                
                else:
                    S = sum(p3)
                    for t in range(len(p3)):
                        p3[t] = p3[t]/S

                    ran = random.random()
                    t = 0
                    while sum(p3[:t]) < ran:
                        t += 1

                    t_charge = journeyLogs[v][d][-1][1]+t+1440*d

                    print(t_charge)

                    charge_length = 0

                    while t_charge+charge_length < t1 and later > 0:
                        later -= 3.5/60
                        charge_length += 1

                    chargeLog[v].append([t_charge,t_charge+charge_length])
            '''
            later += now
                
    charging = [0]*(1440*6)

    for v in chargeLog:
        for c in chargeLog[v]:
            for t in range(c[0],c[1]):
                charging[t] += 3.5

    sim_results.append(charging)

with open('50evs.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t']+list(range(nSim)))
    for t in range(1440*4):
        row = [t+1440]
        for i in range(nSim):
            row.append(sim_results[i][t+1440])
        writer.writerow(row)


with open('50evsCtrl.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t']+list(range(nSim)))
    for t in range(1440*4):
        row = [t+1440]
        for i in range(nSim):
            row.append(sim_control[i][t+1440])
        writer.writerow(row)

