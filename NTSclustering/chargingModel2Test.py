import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
import scipy.ndimage.filters as filt
from clustering import Cluster, ClusteringExercise

data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'

outstem = '../../Documents/simulation_results/NTS/clustering/power/'

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'


assumed_capacity = 30 # kWh
assumed_charge_power = 3.5 # kW
assumed_kwh_limit = 35
def normalise(pdf):
    s = sum(pdf)
    for i in range(len(pdf)):
        pdf[i] = pdf[i]/s

def sample(pdf):
    if sum(pdf) == 0:
        return int(random.random()*len(pdf))
    normalise(pdf)
    x = 0
    ran = random.random()
    while sum(pdf[:x]) <= ran:
        x += 1
    return x

# get cluster labels
labels = {}
# get the labels for both data types
with open(stem+'MEAlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # reminder that row[0] contains the vehicle id + the day of week
        labels[row[0]] = int(row[1])
      
with open(stem+'MEAlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        labels[row[0]] = int(row[1])

# get all charging pdfs
chargePdf = {0:[],1:[],2:[]}
chargePdfWE = {0:[],1:[],2:[]}
chargePdf2 = {0:[],1:[],2:[]}
chargePdfWE2 = {0:[],1:[],2:[]}
availPdf = {0:[],1:[],2:[]}
availPdfWE = {0:[],1:[],2:[]}
#endPdf = {0:[],1:[],2:[]}
#endPdfWE = {0:[],1:[],2:[]}
socPdf = {0:[],1:[],2:[]}
socPdfWE = {0:[],1:[],2:[]}

#with open(stem+'chargePdfW.csv','rU') as csvfile:
with open(stem+'meaEnds.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            for t in range(30):
                chargePdf[i].append(float(row[i+1]))
        
#with open(stem+'chargePdfWE.csv','rU') as csvfile:
with open(stem+'meaEndsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            for t in range(30):
                chargePdfWE[i].append(float(row[i+1]))
                
with open(stem+'chargePdfW2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            for t in range(30):
                chargePdf2[i].append(float(row[i+1]))
            
with open(stem+'chargePdfWE2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            for t in range(30):
                chargePdfWE2[i].append(float(row[i+1]))

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
            
with open(stem+'meaAvail.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            availPdf[i].append(float(row[i+1]))
            
with open(stem+'meaAvailWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(3):
            availPdfWE[i].append(float(row[i+1]))

for i in range(3):
    for t in range(1440):
        chargePdf2[i][t] = chargePdf[i][t]/availPdf[i][t]
        chargePdfWE2[i][t] = chargePdf[i][t]/availPdfWE[i][t]

# do not normalise avaliability as it is a likelihood not a probability

for pdf in [chargePdf,chargePdfWE,chargePdf2,chargePdfWE2,socPdf,socPdfWE]:
    for i in range(3):
        normalise(pdf[i])
    
del availPdf
del availPdfWE

# function defs go here
def get_charge_pdf(clst,typ,home,endTimes):
    if typ == 'W':
        pdf2 = copy.deepcopy(chargePdf[clst])
        pdf3 = copy.deepcopy(chargePdf2[clst])
        #aPdf = availPdf[clst]
        p_aft = 0.704
        
    elif typ == 'WE':
        pdf2 = copy.deepcopy(chargePdfWE[clst])
        pdf3 = copy.deepcopy(chargePdfWE2[clst])
        #aPdf = availPdfWE[clst]
        p_aft = 0.666
        
    # first set all times not at home to 0
    for t in range(len(pdf2)):
        if home[t] == 0:
            pdf2[t] = 0
            pdf3[t] = 0

    # then scale all of the endTimes to be 0.7 and the others to be 0.3
    if len(endTimes) == 0:
        pdf_ = pdf3

    else:
        s2 = 0
        s3 = 0
        pdf_ = [0]*len(pdf2)
        for t in range(len(pdf2)):
            if t in endTimes:
                pdf_[t] = pdf2[t]
                s2 += pdf2[t]
            else:
                pdf_[t] = pdf3[t]
                s3 += pdf3[t]

        if s2 == 0 and s3 == 0:
            pdf_ = [1]*len(pdf2)

        elif s2 == 0:
            pdf_ = pdf3

        elif s3 == 0:
            pdf_ = pdf2

        else:
            for t in range(len(pdf2)):
                if t in endTimes:
                    pdf_[t] = pdf_[t]*p_aft/s2
                else:
                    pdf_[t] = pdf_[t]*(1-p_aft)/s3
    normalise(pdf_)
    return pdf_

def get_charge_times(pdf2,kWh0,clst,typ,log):
    cTimes = []
    # sample a charge start time pdf

    # ok, first sample

    completed = []

    for charge_sample in range(3):
        kWh = copy.deepcopy(kWh0)
        for c in completed:
            kWh -= c
            
        cT = sample(pdf2)
        nextUse = 1440+log[0][0]

        # work out the kWh consumed by that point
        for j in log:
            if j[1] < cT:
                kWh += j[2]
            else:
                if j[0] < nextUse:
                    nextUse = j[0]
                
        SOC = 100-(100*kWh/assumed_capacity)
        if SOC < 0:
            SOC = 0

        if typ == 'W':
            SOCmin = sample(socPdf[clst])
        elif typ == 'WE':
            SOCmin = sample(socPdfWE[clst])

        if SOC < SOCmin:
            # start charging
            t = cT
            c = 0
            while kWh > 0 and t < nextUse:
                c += assumed_charge_power/60
                kWh -= assumed_charge_power/60
                t += 1

            if c > 0:
                cTimes.append([cT,t])
                completed.append(c)

    return cTimes

def predict(log,typ,clst,kWh0):
    home = [1]*1440
    endTimes = []
    for j in log:
        endTimes.append(j[1])
        for t in range(j[0],j[1]):
            if t < 1440:
                home[t] = 0
            
    pdf2 = get_charge_pdf(clst,typ,home,endTimes)

    return get_charge_times(pdf2,kWh0,clst,typ,log)

def s_e(a,b):
    s = 0
    for t in range(len(a)):
        s += np.power(a[t]-b[t],2)
    return s

lowest = {}
highest = {}
typs = {}
# first get all vehicle usage and locations
journeyLogs = {}
with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:

        vehicle = row[0]
        
        vehicle += row[1]

        if row[-1] != '0': # only weekday for noow
            typs[vehicle] = 'W'
        else:
            typs[vehicle] = 'WE'
        
        if vehicle not in journeyLogs:
            journeyLogs[vehicle] = []
        
        start = int(row[2])
        end = int(row[3])

        if end == start:
            continue
        elif end < start:
            end += 1440

        #distance = float(row[4])/1609 # m -> miles
        kWh = float(row[5])/900 # Wh - kWh and taking into account efficiency

        if end < start:
            end += 1440

        journeyLogs[vehicle].append([start,end,kWh])

chargeLogs = {}
# now I need to get the actual charging data
with open(data2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]
        if vehicle not in lowest:
            lowest[vehicle] = 1000
            highest[vehicle] = 0
            
        day = int(row[1])

        if day > highest[vehicle]:
            highest[vehicle] = day
        if day < lowest[vehicle]:
            lowest[vehicle] = day

        vehicle += row[1]

        if vehicle not in chargeLogs:
            chargeLogs[vehicle] = []

        start = int(row[2])
        end = int(row[3])

        if end < start:
            end += 1440

        chargeLogs[vehicle].append([start,end])

avT = [0]*1440
av1 = [0]*1440
av2 = [0]*1440

avTwe = [0]*1440
av1we = [0]*1440
av2we = [0]*1440

n = 0
s1 = 0
s2 = 0
for vehicle in lowest:
    kWh0 = 0
    for d in range(lowest[vehicle],highest[vehicle]):
        if kWh0 > assumed_kwh_limit:
            kWh0 = assumed_kwh_limit
            
        chargingT = [0]*1440
        charging1 = [0]*1440
        charging2 = [0]*1440
        # okay, I should make a function to predict a single day
        v = vehicle+str(d)
        if v not in journeyLogs:
            continue
        if v not in labels:
            continue
        n += 1
        '''
        if v not in chargeLogs:
            continue
        '''
        cT = predict(journeyLogs[v],typs[v],labels[v],kWh0)
        
        for c in cT:
            for t in range(c[0],c[1]):
                if t < 1440:
                    charging1[t] = 1
                else:
                    charging1[t-1440] = 1

        kWh0 -= assumed_charge_power*sum(charging1)/60
        
        kWh2 = 0
        start = 0
        for j in journeyLogs[v]:
            kWh0 += j[2]
            kWh2 += j[2]
            t = j[1]

        if kWh2 > assumed_capacity:
            kWh2 = assumed_capacity
            
        # then predict the dumb charging
        while kWh2 > 0:
            if t < 1440:
                charging2[t] = 1
            else:
                charging2[t-1440] = 1
            kWh2 -= assumed_charge_power/60
            t += 1
            
        # then get the actual charging
        if v in chargeLogs:
            for c in chargeLogs[v]:
                for t in range(c[0],c[1]):
                    if t < 1440:
                        chargingT[t] = 1
                    else:
                        chargingT[t-1440] = 1
        if typs[v] == 'W':
            for t in range(1440):
                avT[t] += chargingT[t]
                av1[t] += charging1[t]
                av2[t] += charging2[t]
        else:
            for t in range(1440):
                avTwe[t] += chargingT[t]
                av1we[t] += charging1[t]
                av2we[t] += charging2[t]

for av in [avT,av1,av2,avTwe,av1we,av2we]:
    normalise(av)
    for t in range(len(av)):
        av[t] = av[t]*100
        

s1 = s_e(av1,avT)
s2 = s_e(av2,avT)
print(s1)
print(s2)
s1 = s_e(av1we,avTwe)
s2 = s_e(av2we,avTwe)
print(s1)
print(s2)

with open(outstem+'error2.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','dumb','smart','true','dumbWe','smartWe','trueWe'])
    for t in range(1440):
        writer.writerow([t,av2[t],av1[t],avT[t],av2we[t],av1we[t],avTwe[t]])

plt.figure(figsize=(5,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
x = [2*60,6*60,10*60,14*60,18*60,22*60]
x_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
plt.subplot(2,1,1)
plt.plot(avT,label='True')
plt.plot(av1,label='(a)')
plt.plot(av2,label='(b)')
plt.xlim(0,1439)
plt.xticks(x,x_ticks)
plt.ylabel('Probability (%)')
plt.ylim(0,0.2)
plt.grid()
plt.title('Weekdays',y=0.8)
plt.legend()

plt.subplot(2,1,2)
plt.plot(avTwe,label='True')
plt.plot(av1we,label='(a)')
plt.plot(av2we,label='(b)')
plt.xlim(0,1439)
plt.xticks(x,x_ticks)
plt.title('Weekends',y=0.8)
plt.ylabel('Probability (%)')
plt.ylim(0,0.25)
plt.grid()
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/error.eps', format='eps', dpi=1000)

plt.show()
