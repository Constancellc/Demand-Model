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
chargeLog = {}
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

        #soc = int(6*float(row[4]))
        start = int(row[2])

        charges[vehicle].append([day,start])

        vehicle += str(day)

        if vehicle not in chargeLog:
            chargeLog[vehicle] = []
        
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

        journeys[vehicle].append([day,end,kWh,dType,None])


for vehicle in journeys:
    jLog = journeys[vehicle]
    cLog = charges[vehicle]

    c = 0
    j = 0

    soc = 1

    while j < len(jLog):
        soc -= jLog[j][2]/24

        print(soc)

        if soc < 0:
            print(soc)
            soc = 0

        jLog[j][4] = soc
        
        j += 1

        if cLog[c][0] >= jLog[j][0] and cLog[c][1] >= jLog[j][1]:
            soc = 1
            c += 1


del charges

# Let's check this soc thing
for vehicle in journeys:
    s = []
    for j in journeys[vehicle]:
        s.append(j[4])
    plt.figure()
    plt.plot(s)
    plt.show()
        
# now I need to step through the journeys and work out if there was a charge

'''
        



chargeTimes = {}       
# now get the MEA data
with open(charge_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[-1] == '1':
            continue
        vehicle = row[0]+row[1]

        if vehicle not in chargeTimes:
            chargeTimes[vehicle] = []

        soc = int(6*float(row[4]))
        start = int(row[2])

        chargeTimes[vehicle].append([start,soc])
        
tripEnds = {}
# now get the MEA data
with open(trip_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    #next(reader)
    for row in reader:
        print(row)
        if row[-1] == '1': # skip weekends
            continue
        kWh = float(row[-2])/1000
        vehicle = row[0]
            
        dayNo = int(row[1])
        end = int(row[3])
        #start = int(row[2])
        #dist = float(row[-3])/1000

        if end > 1440:
            end -= 1440
            dayNo += 1

        vehicle += str(dayNo)
        if vehicle not in tripEnds:
            tripEnds[vehicle] = []


        if soc < 0:
            soc = 0
            
        tripEnds[vehicle].append([end,kWh])


for vehicle in endTimes:
    ends = endTimes[vehicle]

    try:
        k = MEA[vehicle]
    except:
        continue

    try:
        charges = chargeTimes[vehicle]
    except:
        charges = []

    cT = []
    for charge in charges:
        cT.append(charge[0])

    for j in ends:
        d = get_nearest(end,cT)

        if d > 5:
            c

        try:
            k = MEA[vehicle]
        except:
            continue
        try:
            ends = tripEnds[vehicle]
        except:
            ends = []
        soc = int(6*float(row[4]))
        start = int(row[2])
        d = get_nearest(start,ends)
        
        if d > 5:
            continue
        
        start = int(start/30)

        


        


        
        #soc = int(100*float(row[4])+random.random()*16.666-8.333)

        vehicle += row[1]
        
        if row[-1] == '0':
            pdf = chargingPdf
            pdf2 = chargingPdf2
            pdf3 = endPdf
            sPdf = socPdf
            cls = MEA
            nc = nCharges
        else:
            pdf = chargingPdfWE
            pdf2 = chargingPdfWE2
            pdf3 = endPdfWE
            sPdf = socPdfWE
            cls = MEA2
            nc = nChargesWE
        
        start = int(row[2])
        try:
            ends = tripEnds[vehicle]
        except:
            ends = []

        d = get_nearest(start,ends)
        if d < 5:
            pdf_ = pdf
            try:
                pdf3['y'][cls[vehicle]][start] += 1
            except:
                continue
        else:
            pdf_ = pdf2
            try:
                pdf3['n'][cls[vehicle]][start] += 1
            except:
                continue
        
        if start >= 48:
            start -= 48

        soc = int(100*float(row[4])+random.random()*16.666-8.333)
                  
        if vehicle not in nc:
            nc[vehicle] = 1
        else:
            nc[vehicle] += 1

            
        try:
            pdf_[cls[vehicle]][start] += 1
        except:
            continue
            
        try:
            sPdf[cls[vehicle]][soc] += 1
        except:
            continue

plt.figure()
for i in range(3):
    plt.subplot(3,1,i+1)
    plt.plot(endPdf['y'][i])
    plt.plot(endPdf['n'][i])
plt.show()

# now get the MEA data
with open(data3,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]

        if vehicle not in highest:
            continue

        day = int(row[1])

        if day < lowest[vehicle] or day > highest[vehicle]:
            continue
        
        if row[-1] == '0':
            nc = nCharges
        else:
            nc = nChargesWE

        if vehicle+row[1] not in nc:
            nc[vehicle+row[1]] = 0
            
# now get pdfs
nChargesPdf = []
nChargesPdfWE = []
for i in range(3):
    nChargesPdf.append([0]*25)
    nChargesPdfWE.append([0]*10)

for vehicle in nCharges:
    try:
        nChargesPdf[MEA[vehicle]][nCharges[vehicle]] += 1
    except:
        continue
    
for vehicle in nChargesWE:
    try:
        nChargesPdfWE[MEA2[vehicle]][nChargesWE[vehicle]] += 1
    except:
        continue

pInt = []
pIntWE = []
for i in range(3):
    S = sum(nChargesPdf[i])
    S2 = sum(nChargesPdfWE[i])
    exp = 0
    for t in range(len(nChargesPdf[i])):
        nChargesPdf[i][t] = nChargesPdf[i][t]/S
        exp += nChargesPdf[i][t]*t
    pInt.append(exp)
    exp = 0
    for t in range(len(nChargesPdfWE[i])):
        nChargesPdfWE[i][t] = nChargesPdfWE[i][t]/S2
        exp += nChargesPdfWE[i][t]*t
    pIntWE.append(exp)

print(pInt)
print(pIntWE)
half = [0,0,0]
halfWE = [0,0,0]
for i in range(3):
    s1 = sum(chargingPdf[i])
    s2 = sum(chargingPdfWE[i])
    s3 = sum(chargingPdf2[i])
    s4 = sum(chargingPdfWE2[i])
    for t in range(48):
        chargingPdf[i][t] = chargingPdf[i][t]*100/s1
        chargingPdfWE[i][t] = chargingPdfWE[i][t]*100/s2
        chargingPdf2[i][t] = chargingPdf2[i][t]*100/s3
        chargingPdfWE2[i][t] = chargingPdfWE2[i][t]*100/s4

for i in range(3):
    s1 = sum(socPdf[i])
    s2 = sum(socPdfWE[i])
    socPdf2 = filt.gaussian_filter1d([0]+socPdf[i],5)
    socPdfWE2 = filt.gaussian_filter1d([0]+socPdfWE[i],4)
    c1 = 0
    c2 = 0
    for t in range(101):
        if half[i] == 0:
            c1 += socPdf[i][t]
            if c1 > s1/2:
                half[i] = t
        if halfWE[i] == 0:
            c2 += socPdfWE[i][t]
            if c2 > s2/2:
                halfWE[i] = t
        socPdf[i][t] = float(socPdf2[t+1])*100.0/float(s1)
        socPdfWE[i][t] = socPdfWE2[t+1]*100/s2

plt.figure(figsize=(5,2.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']
clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}
clrs2 = {'0':'y','1':'m','2':'c'}
n = 1
for i in range(3):
    plt.subplot(2,3,n)
    plt.plot(chargingPdf[i],c=clrs[str(i)])
    plt.plot(chargingPdf2[i],c=clrs[str(i)],ls=':')
    plt.xlim(0,47)
    plt.ylim(0,12)
    plt.grid()
    if n == 2:
        plt.title('Weekday')
    if n in [2,3,5]:
        plt.yticks([5,10],['',''])
    else:
        plt.yticks([0,5,10],['0%','5%','10%'])
    if n in []:#7,8,9]:
        plt.xticks([0,4,8],['',''])
    else:
        plt.xticks(x,x_ticks)
    n += 1
    
for i in range(3):
    plt.subplot(2,3,n)
    plt.plot(chargingPdfWE[i],c=clrs2[str(i)],label=str(i))
    plt.plot(chargingPdfWE2[i],c=clrs2[str(i)],ls=':',label=str(i))
    plt.xlim(0,47)
    plt.ylim(0,12)
    plt.grid()
    if n == 5:
        plt.title('Weekend')
    if n in [5,6]:
        plt.yticks([5,10],['',''])
    else:
        plt.yticks([0,5,10],['0%','5%','10%'])
    plt.xticks(x,x_ticks)
    n += 1
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/chargePdfs.eps', format='eps', dpi=1000)

plt.figure(figsize=(5,2.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}
clrs2 = {'0':'y','1':'m','2':'c'}
n = 1
for i in range(3):
    plt.subplot(2,3,n)
    plt.plot(socPdf[i],c=clrs[str(i)])
    plt.plot([half[i],half[i]],[0,socPdf[i][half[i]]],c='k',ls=':')
    plt.xlim(0,100)
    plt.ylim(0,2)
    plt.grid()
    if n == 2:
        plt.title('Weekday')
    if n in [2,3,5]:
        plt.yticks([1,2],['',''])
    else:
        plt.yticks([0,1,2],['0%','1%','2%'])

    n += 1
    
for i in range(3):
    plt.subplot(2,3,n)
    plt.plot(socPdfWE[i],c=clrs2[str(i)],label=str(i))
    plt.plot([halfWE[i],halfWE[i]],[0,socPdfWE[i][halfWE[i]]],c='k',ls=':')
    plt.xlim(0,100)
    plt.ylim(0,2)
    plt.grid()
    if n == 5:
        plt.title('Weekend')
    if n in [5,6]:
        plt.yticks([1,2],['',''])
    else:
        plt.yticks([0,1,2],['0%','1%','2%'])
    n += 1
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/socPdfs.eps', format='eps', dpi=1000)

plt.figure(figsize=(5,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.bar(np.arange(1,4)-0.2,pInt,width=0.4,label='Week')
plt.bar(np.arange(1,4)+0.2,pIntWE,width=0.4,label='Weekend')
plt.grid()
plt.ylabel('Expected Charges')
plt.xlabel('Cluster')
plt.legend()
plt.xticks(range(1,4),['1','2','3'])
#plt.ylim(0,1.5)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/ncharges.eps', format='eps', dpi=1000)


# now let's store the individual pdf
with open(stem+'chargePdfW.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [chargingPdf[i][t]]
        writer.writerow(row)
        
with open(stem+'chargePdfWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [chargingPdfWE[i][t]]
        writer.writerow(row)

with open(stem+'meaAvail.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2'])
    for t in range(1440):
        row = [t]
        for i in range(3):
            row += [availPdf[i][t]]
        writer.writerow(row)
        
with open(stem+'meaAvailWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2'])
    for t in range(1440):
        row = [t]
        for i in range(3):
            row += [availPdfWE[i][t]]
        writer.writerow(row)

with open(stem+'meaEnds.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [endPdf['y'][i][t]/(endPdf['n'][i][t]+endPdf['y'][i][t])]
        writer.writerow(row)
        
with open(stem+'meaEndsWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [endPdfWE['y'][i][t]/(endPdfWE['n'][i][t]+endPdfWE['y'][i][t])]
        writer.writerow(row)

with open(stem+'chargePdfW2.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [chargingPdf2[i][t]]
        writer.writerow(row)
        
with open(stem+'chargePdfWE2.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [chargingPdfWE2[i][t]]
        writer.writerow(row)

with open(stem+'socPdfW.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['SOC','0','1','2'])
    for t in range(101):
        row = [t]
        for i in range(3):
            row += [socPdf[i][t]]
        writer.writerow(row)
        
with open(stem+'socPdfWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['SOC','0','1','2'])
    for t in range(101):
        row = [t]
        for i in range(3):
            row += [socPdfWE[i][t]]
        writer.writerow(row)
        

with open(stem+'nCharges.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['cluster','w','we'])
    for i in range(3):
        writer.writerow([i,pInt[i],pIntWE[i]])

plt.show()
'''
