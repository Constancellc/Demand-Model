import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

#data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'


'''
I have changed from each point being a vehicle to each point eing a vehicle-day

This is going to really change our simulation.

In fact it might be better to start from scratch because this script is a mess.

Writing functions could definitely neaten some stuff up

'''
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
clusterPdfWE = [] 
chargingPdfWE = []
pInt = []
pIntWE = []
for i in range(5):
    chargingPdf.append([])
    chargingPdfWE.append([])

with open('clusterPdf.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        clusterPdf.append(float(row[1])/100)

with open('clusterPdfWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        clusterPdfWE.append(float(row[1])/100)

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

with open('nCharges.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        pInt.append(float(row[1]))
        pIntWE.append(float(row[2]))
        
nV = 1
nSim = 1
cluster_n = [0]*5

clPdf = clusterPdf
chPdf = chargingPdf
days = [1,2,3,4,5]
'''
clPdf = clusterPdfWE
chPdf = chargingPdfWE
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

        kWh = 0
        for d in range(5):
            t1 = 1440*d
            deadline = 0
            c_start = 0
            for j in range(nJ):
                if journeyLogs[v][j][1] < t1+1440 and journeyLogs[v][j][1] > t1:
                    kWh += journeyLogs[v][j][2]
                    if journeyLogs[v][j][1] > c_start:
                        c_start = journeyLogs[v][j][1]
                    try:
                        if journeyLogs[v][j+1][0] > deadline:
                            deadline = journeyLogs[v][j+1][0]
                    except:
                        continue
                
            if kWh == 0:
                continue
            
            c_length = int(60*kWh/3.5)+1

            if deadline == 0:
                deadline += 1440*6

            for t in range(c_start,c_start+c_length):
                if t < 1440*6:#deadline:
                    charging[t] += 3.5
                    kWh -= 3.5/60
                    
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
        now = 0
        
        pdf = []
        p = copy.deepcopy(chPdf[NTS[v]])
        for d in range(5):
            pdf += p

        # first set all times when vehicle not at home equal to zero
        for t in range(len(pdf)):
            if locations[v][t] != '23':
                pdf[t] = 0
                
        # for each day generate a pdf from the first journey today to first tomorrow
        for d in range(5):
            kWh = 0
            # here I need to decide the number of charges
            #nC = np.random.poisson(pInt[NTS[v]])

            t0 = 1440*d
            t1 = 1440*(d+1)

            # first charge
            p2 = copy.deepcopy(pdf[t0:t1])

            # need to find the journey end times - key suspects
            endTimes = []

            for j in journeyLogs[v]:
                if j[1] > t0 and j[1] < t1:
                    endTimes.append(j[1]+1)

            s1 = 0
            s2 = 0

            for t in range(t0,t1):
                if t in endTimes:
                    s1 += p2[t-t0]
                else:
                    s2 += p2[t-t0]

            for t in range(t0,t1):
                if t in endTimes:
                    if s1 > 0:
                        p2[t-t0] = 0.7*p2[t-t0]/s1
                else:
                    if s2 > 0:
                        p2[t-t0] = 0.3*p2[t-t0]/s2
                        
            S = sum(p2)
            # this is both to account for errors and in the case
            # there are no valid end times

            
            if S == 0:
                continue
            for t in range(len(p2)):
                p2[t] = p2[t]/S
            ran = random.random()
            t = 0

            while sum(p2[:t]) < ran:
                t += 1
            t_charge = t0+t

            if later > 0:
                now = later # left over from yesterday
            later = 0

            deadline = 1440*6 # pretty sure deadline is obsolete

            for j in journeyLogs[v]:
                if j[1] > t0 and j[1] < t_charge:
                    now += j[2]
                    kWh += j[2]
                elif j[1] > t0 and j[1] < t1:
                    later += j[2]
                    kWh += j[2]
                if j[0] > t1 and j[0] < deadline:
                    deadline = j[0]

            # we need to factor in the possibility of no charge
            # overrride no charge if SOC too low
            nC = np.random.poisson(pInt[NTS[v]])

            if nC == 0 and now < 10:
                later += now
                continue

            charge_length = 0
            while (locations[v][t_charge+charge_length] == '23') and now > 0:
                charge_length += 1
                now -= 3.5/60

            chargeLog[v].append([t_charge,t_charge+charge_length])
            later += now

            # second charge
            if later > 0 and t_charge+charge_length < t1:
                ran = random.random()

                t = 0
                t_charge2 = None
                s = 0
                for t in range(t_charge+charge_length,t1):
                    s += p2[t-t0]
                    if s > ran and t_charge2 == None:
                        t_charge2 = t
            else:
                t_charge2 = None

            if t_charge2 != None:

                charge_length = 0
                while (locations[v][t_charge2+charge_length] == '23')\
                      and later > 0:
                    charge_length += 1
                    later -= 3.5/60

                chargeLog[v].append([t_charge2,t_charge2+charge_length])

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

