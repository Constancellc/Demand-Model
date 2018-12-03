import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
import scipy.ndimage.filters as filt
from clustering import Cluster, ClusteringExercise

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

charge_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'

trip_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'


NTS = {}
MEA = {}
NTS2 = {}
MEA2 = {}

# get the labels for both data types
with open(stem+'NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS[row[0]] = int(row[1])
        
with open(stem+'MEAlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA[row[0]] = int(row[1])

# get the labels for both data types
with open(stem+'NTSlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS2[row[0]] = int(row[1])
        
with open(stem+'MEAlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA2[row[0]] = int(row[1])

def get_nearest(p,lst):
    d = 30
    for x in lst:
        if abs(x-p) < d:
            d = abs(x-p)

    return d

def get_nearest2(p,lst):
    d = 30
    for x in lst:
        if abs(x[0]-p) < d:
            d = abs(x[0]-p)

    return d

def get_nearest3(p,lst):
    d = 2000000
    best = None
    for x in lst:
        if abs(x-p) < d:
            d = abs(x-p)
            best = x

    return best

y = []
n = []

for i in range(3):
    y.append([])
    n.append([])
    for s in range(10):
        y[i].append([0]*48)
        n[i].append([0]*48)


charges = {}
highest = {}
lowest = {}
# now get the MEA data
with open(charge_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]

        if vehicle not in charges:
            charges[vehicle] = []
            highest[vehicle] = 0
            lowest[vehicle] = 10000

        day = int(row[1])

        if day < lowest[vehicle]:
            lowest[vehicle] = day
        if day > highest[vehicle]:
            highest[vehicle] = day

        soc = float(row[4])
        start = int(row[2])

        charges[vehicle].append([day,start,soc])
       
journeys = {}
typ = {}
with open(trip_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]

        if vehicle not in journeys:
            journeys[vehicle] = []
            typ[vehicle] = {}
            
        day = int(row[1])
        typ[vehicle][day] = row[-1]

        if day < lowest[vehicle]:
            continue
        elif day > highest[vehicle]:
            continue
        
        end = int(row[3])
        dType = row[-1]
        kWh = float(row[-2])/1000
        
        #start = int(row[2])
        #dist = float(row[-3])/1000

        if end > 1440:
            end -= 1440
            day += 1

        journeys[vehicle].append([day,end,kWh,dType,None,None])

# I need 12 arrays to store the reults
wPdf = {}
wePdf = {}
wPdf_ = {}
wePdf_ = {}
for i in range(3):
    wPdf[i] = {}
    wePdf[i] = {}
    for t in ['y','n']:
        wPdf[i][t] = []
        wePdf[i][t] = []
        wPdf_[t] = []
        wePdf_[t] = []

        for S in range(6):
            wPdf[i][t].append([0]*48)
            wePdf[i][t].append([0]*48)
            wPdf_[t].append([0]*48)
            wePdf_[t].append([0]*48)

known = {}
n = 0
for vehicle in journeys:
    if vehicle not in known:
        known[vehicle] = []
    jLog = journeys[vehicle]
    cLog = charges[vehicle]

    cList = []
    weList = []
    jList = []
    cSOC = {}
    for c in cLog:
        t = int(c[0]*1440+c[1])
        cList.append(t)
        weList.append
        cSOC[t] = c[2]
        if cSOC[t] == 1:
            cSOC[t] = 0.99


    for j1 in range(len(jLog)):
        j = jLog[j1]
        t = j[0]*1440+j[1]
        jList.append(t)
        t1 = get_nearest3(t,cList)


        if t1 == None:
            continue

        elif abs(t1-t) < 10:
            n += 1
            j[5] = True
            j[4] = cSOC[t1]
            known[vehicle].append(j1)
        else:
            j[5] = False

    # cList now contains a list of all the charges and jList a list of journeys
    for c in cList:
        t1 = get_nearest3(c,jList)

        if t1 == None:
            continue

        elif abs(t1-c) < 10:
            continue

        day = int(c/1440)
        try:
            if typ[vehicle][day] == '0':
                wPdf_['y'][int(cSOC[c]*6)][int(float(c%1440)/30)] += 1
            else:
                wePdf_['y'][int(cSOC[c]*6)] [int(float(c%1440)/30)]+= 1
        except:
            continue

    del cList
    del jList
        
        
print(n)
del charges
del typ

for vehicle in journeys:
    jLog = journeys[vehicle]
    for j1 in range(len(jLog)):
        j = jLog[j1]
        if j[-1] == True:
            SOC = j[4]#int(12*j[4])
            t = int(j[1]/30)
            if SOC == 1.0:
                SOC = 0.99
            if t == 48:
                t = 47
            if j[-3] == '0':
                if vehicle+str(j[0]) not in MEA:
                    continue
                wPdf[MEA[vehicle+str(j[0])]]['y'][int(6*SOC)][t] += 1
                
            else:
                if vehicle+str(j[0]) not in MEA2:
                    continue
                wePdf[MEA2[vehicle+str(j[0])]]['y'][int(6*SOC)][t] += 1

            continue

        if j[-1] == None:
            continue

        j2 = get_nearest3(j1,known[vehicle])

        if j2 == None:
            continue
        
            
        if j1 < j2:
            SOC = jLog[j2][4]
            for i in range(j2-j1):
                SOC += jLog[j2-i][2]/24

        else:
            SOC = 1
            for i in range(j1-j2):
                SOC -= jLog[j1-i][2]/24

        if SOC > 0 and SOC < 1:
            # store result in relevant array
            jLog[j1][4] = SOC
            SOC = int(6*SOC)
            t = int(j[1]/30)
            if t == 48:
                t = 47

            try:
                t1 = int(jLog[j1+1][1]/30)
            except:
                t1 = t
            if t1 < t:
                t1 += 48
            
            if j[-3] == '0':
                if vehicle+str(j[0]) not in MEA:
                    continue
                wPdf[MEA[vehicle+str(j[0])]]['n'][SOC][t] += 1
                for t_ in range(t,t1):
                    try:
                        wPdf_['n'][SOC][t_] += 1
                    except:
                        wPdf_['n'][SOC][t_-48] += 1
                        
            else:
                if vehicle+str(j[0]) not in MEA2:
                    continue
                wePdf[MEA2[vehicle+str(j[0])]]['n'][SOC][t] += 1
                for t_ in range(t,t1):
                    try:
                        wePdf_['n'][SOC][t_] += 1
                    except:
                        wePdf_['n'][SOC][t_-48] += 1
                
del known
plt.figure()
heatmaps = {}
for i in range(3):
    heatmaps[i] = []
    for s in range(6):
        heatmaps[i].append([0]*48)

    for s in range(6):
        for t in range(48):
            try:
                heatmaps[i][s][t] = wPdf[i]['y'][s][t]/(wPdf[i]['y'][s][t]+\
                                                    wPdf[i]['n'][s][t])
            except:
                continue
            if wPdf[i]['y'][s][t]+wPdf[i]['n'][s][t] == 1:
                heatmaps[i][s][t] = 0
                
    heatmaps[i] = filt.gaussian_filter(heatmaps[i],1)

    with open(stem+'jointPdfW'+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for s in range(6):
            writer.writerow(heatmaps[i][s])

    plt.subplot(3,1,i+1)
    plt.imshow(heatmaps[i],vmin=0,vmax=1,cmap='magma')
plt.figure()
heatmaps = {}
for i in range(3):
    heatmaps[i] = []
    for s in range(6):
        heatmaps[i].append([0]*48)

    for s in range(6):
        for t in range(48):
            try:
                heatmaps[i][s][t] = wePdf[i]['y'][s][t]/(wePdf[i]['y'][s][t]+\
                                                    wePdf[i]['n'][s][t])
            except:
                continue
            if wePdf[i]['y'][s][t]+wePdf[i]['n'][s][t] == 1:
                heatmaps[i][s][t] = 0
                
    heatmaps[i] = filt.gaussian_filter(heatmaps[i],1)
    
    with open(stem+'jointPdfWE'+str(i+1)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for s in range(6):
            writer.writerow(heatmaps[i][s])

    plt.subplot(3,1,i+1)
    plt.imshow(heatmaps[i],vmin=0,vmax=1,cmap='magma')

           
plt.figure()
plt.subplot(2,1,1)
heatmap = np.zeros((6,48))
for s in range(6):
    for t in  range(48):
        try:
            heatmap[s][t] = wPdf_['y'][s][t]/(wPdf_['y'][s][t]+\
                                               wPdf_['n'][s][t])
        except:
            continue
        if wPdf_['y'][s][t]+wPdf_['n'][s][t] == 1:
            heatmap[s][t] = 0
heatmap = filt.gaussian_filter(heatmap,1)
plt.imshow(heatmap,vmin=0,vmax=1,cmap='magma')

with open(stem+'jointPdfW_.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for s in range(6):
        writer.writerow(heatmap[s])

plt.subplot(2,1,2)
heatmap = np.zeros((6,48))
for s in range(6):
    for t in  range(48):
        try:
            heatmap[s][t] = wePdf_['y'][s][t]/(wePdf_['y'][s][t]+\
                                               wePdf_['n'][s][t])
        except:
            continue
        if wePdf_['y'][s][t]+wePdf_['n'][s][t] == 1:
            heatmap[s][t] = 0
heatmap = filt.gaussian_filter(heatmap,1)
plt.imshow(heatmap,vmin=0,vmax=1,cmap='magma')

with open(stem+'jointPdfWE_.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for s in range(6):
        writer.writerow(heatmap[s])
        
plt.tight_layout()
plt.show()
