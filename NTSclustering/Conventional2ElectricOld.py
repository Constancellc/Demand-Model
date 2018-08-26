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
chargingPdf2 = []
clusterPdf2 = [] 
chargingPdfWE = []
chargingPdfWE2 = []
pInt = []
pIntWE = []
for i in range(5):
    chargingPdf.append([])
    chargingPdf2.append([])
    chargingPdfWE.append([])
    chargingPdfWE2.append([])

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
                chargingPdfWE[i].append(float(row[i+1])/3000)

with open('chargePdfW2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(5):
            for t in range(30):
                chargingPdf2[i].append(float(row[i+1])/3000)
            
with open('chargePdfWE2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(5):
            for t in range(30):
                chargingPdfWE2[i].append(float(row[i+1])/3000)

with open('nCharges.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        pInt.append(float(row[1]))
        pIntWE.append(float(row[2]))
        
nV = 50
nSim = 10
cluster_n = [0]*5

clPdf = clusterPdf
chPdf = chargingPdf
chPdf2 = chargingPdf2
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
        locations[v] =['-1']*8640
        
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
                    locations[vehicle][day*1440+t] = '0'
                else:
                    locations[vehicle][day*1440+t-1440] = '0'
                    
            if end < 1440:
                locations[vehicle][day*1440+end] = purposeTo
            else:
                locations[vehicle][day*1440+end-1440] = purposeTo
            
            kWh = distance*0.3 # basic bitch approx

            start += 1440*(day-1)
            end += 1440*(day-1)

            journeyLogs[vehicle].append([start,end,kWh])

            #journeyLogs[vehicle][day-1].append([start,end,kWh,purposeTo])

    # find charging using the dumb assumption
    charging = [0.0]*1440*6
    for v in journeyLogs:
        nJ = len(journeyLogs[v])
        if nJ == 0:
            continue
        j0 = 0
        j1 = 0
        for d in range(5):
            kWh = 0
            t1 = 1440*d
            while journeyLogs[v][j1][0] < t1+1440 and j1 < nJ-1:
                j1 += 1
            c_start = journeyLogs[v][j1-1][1]
            
            for j in range(j0,j1):
                kWh += journeyLogs[v][j][2]
                
            if kWh == 0:
                continue
            
            c_length = int(60*kWh/3.5)

            for t in range(c_start,c_start+c_length):
                try:
                    charging[t] += 3.5
                except:
                    continue
    sim_control.append(charging)
    
    # post processing the locations
    for v in locations:
        t = 0
        while locations[v][t] == '-1' and t < 8600:
            locations[v][t] = '23'
            t += 1
        while t < 8600:
            while locations[v][t] == '0' and t < 8600:
                t += 1
            new = locations[v][t]
            t += 1
            while locations[v][t] == '-1' and t < 8600:
                locations[v][t] = new
                t += 1

    chargeLog = {}
    for v in chosen:
        chargeLog[v] = []
        later = 0

        # need two pdfs - first and second charge
        
        pdf = []
        pdf2 = []
        p = copy.deepcopy(chPdf[NTS[v]])
        p_ = copy.deepcopy(chPdf2[NTS[v]])
        for d in range(5):
            pdf += p
            pdf2 += p_

        for t in range(len(pdf)):
            if locations[v][t] == '0':#!= '23':
                pdf[t] = 0
                pdf2[t] = 0
            
                    
        # for each day generate a pdf from the first journey today to first tomorrow
        for d in range(5):
            # here I need to decide the number of charges
            #nC = np.random.poisson(pInt[NTS[v]])

            t0 = 1440*d
            t1 = 1440*(d+1)

            # first charge
            p2 = copy.deepcopy(pdf[t0:t1])
            
            # normalise
            S = sum(p2)

            if S > 0: 
                for t in range(len(p2)):
                    p2[t] = p2[t]/S

                # randomly sample for first charge time
                ran = random.random()
                t = 0
                while sum(p2[:t]) < ran:
                    t += 1

                t_charge = t0+t

            else:
                t_charge = t0

            now = later # left over from yesterday
            later = 0

            deadline = 1440*6

            for j in journeyLogs[v]:
                if j[0] > t0 and j[1] < t_charge:
                    now += j[2]
                elif j[0] > t0 and j[0] < t1:
                    later += j[2]
                if j[0] > t1 and j[0] < deadline:
                    deadline = j[0]
            '''
            if (nC == 0 and now<10) or now == 0:
                later += now
                continue
                '''

            charge_length = 0
            #while (locations[v][t_charge+charge_length] == '23') and now > 0:
            while (locations[v][t_charge+charge_length] != '0') and now > 0:
                charge_length += 1
                now -= 3.5/60

            chargeLog[v].append([t_charge,t_charge+charge_length])
            later += now

            # second charge
            #if nC > 1 and later > 0:
            if later > 0:
                t0 = t_charge+charge_length
                p2 = copy.deepcopy(pdf2[t0:t1])

                S = sum(p2)

                if S > 0:
                    for t in range(len(p2)):
                        p2[t] = p2[t]/S

                    ran = random.random()
                    t = 0

                    while sum(p2[:t]) < ran:
                        t += 1

                    t_charge = t0+t
                    charge_length = 0
                    
                    while t_charge+charge_length < deadline and later > 0:
                        charge_length += 1
                        later -= 3.5/60

                    chargeLog[v].append([t_charge,t_charge+charge_length])

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

