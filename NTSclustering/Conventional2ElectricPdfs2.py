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

'''

This is not a replacement file, this is trying something new!

Ok, thinking time.

What I want to know is the probability that a journey end results in a charge,
given the SOC, time, weekday/weekend, and cluster.

I need to step through all of the journeys, see if they resulted in a charge
and store the observation in the appropriate pdf.

The problem is that I only have SOC recorded when there is a charge, not when
there isn't. However, I do have the energy consumption in Wh of each journey.

So here is what I will have to do:

Get all journey end times and energy consumption

Get all charges

For each vehicle step through and add a SOC


I will make a new journeys dict which will contain a list for each vehicle of
[day,mins,kWh,soc]

where the last parameter will be updated as I go

I will have to make sure to only start while the charging data is active

==== UPDATE ====

I don't think this is working - I think we're going to have to interpolate the
SOC. Basically we'll have to find the nearest known point of SOC and try and
work backwards or forwards. This still doesn't help if it turns out there is a
lot of charging not at work. I mean I guess it helps a bit. I need to think more

Proposal:
Sort through all of the journeys and store then as
[end,kWh,purp,SOC,plugin]

except the last two will not be filled in.

Then sort through all of the charges and fill in Y and the SOC on all other
points, store all the indexes for which the values are known

Next for each missing entry find the nearest known one and infer the SOC at that
point. If it is > 0 and the purpose is home, add it to the distribution.
'''
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
with open(trip_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]

        if vehicle not in journeys:
            journeys[vehicle] = []
            
        day = int(row[1])

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
for i in range(3):
    wPdf[i] = {}
    wePdf[i] = {}
    for t in ['y','n']:
        wPdf[i][t] = []
        wePdf[i][t] = []

        for S in range(6):
            wPdf[i][t].append([0]*48)
            wePdf[i][t].append([0]*48)
known = {}
n = 0
for vehicle in journeys:
    if vehicle not in known:
        known[vehicle] = []
    jLog = journeys[vehicle]
    cLog = charges[vehicle]

    cList = []
    cSOC = {}
    for c in cLog:
        t = int(c[0]*1440+c[1])
        cList.append(t)
        cSOC[t] = c[2]


    for j1 in range(len(jLog)):
        j = jLog[j1]
        t = j[0]*1440+j[1]
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
    '''
        
    c = 0
    j = 0    
    while j < len(jLog) and c < len(cLog):
        if cLog[c][0] == jLog[j][0]:
            
            d = abs(cLog[c][1]-jLog[j][1])
            if d < 10:
                n += 1
                jLog[j][4] = cLog[c][2]
                jLog[j][5] = True
                known[vehicle].append(j)#1440*cLog[c][0]+cLog[c][1])
                c += 1
            else:
                # ok I think I see the problem here, we could be on the right
                # day but the charge happens later in the 
                jLog[j][5] == False
            j += 1

        elif jLog[j][0] < cLog[c][0]:
            jLog[j][5] = False
            j += 1

        elif jLog[j][0] > cLog[c][0]:
            c += 1
    '''

        
print(n)
del charges

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
            if j[-3] == '0':
                if vehicle+str(j[0]) not in MEA:
                    continue
                wPdf[MEA[vehicle+str(j[0])]]['n'][SOC][t] += 1
            else:
                if vehicle+str(j[0]) not in MEA2:
                    continue
                wePdf[MEA2[vehicle+str(j[0])]]['n'][SOC][t] += 1
                
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

    plt.subplot(3,1,i+1)
    plt.imshow(heatmaps[i],vmin=0,vmax=1)
plt.show()
