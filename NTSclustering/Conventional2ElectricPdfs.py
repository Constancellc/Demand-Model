import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'

stem = '../../Documents/simulation_results/NTS/clustering/labels/'

'''
CHANGES THAT NEED TO BE MADE

I've updated the feature vector so may need ot change how i'm storing vehicles /
looking for their labels



'''
NTS = {}
MEA = {}

NTStotal = [0]*3
MEAtotal = [0]*3
# get the labels for both data types
with open(stem+'NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS[row[0]] = int(row[1])
        NTStotal[int(row[1])] += 1
        
with open(stem+'MEAlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA[row[0]] = int(row[1])
        MEAtotal[int(row[1])] += 1

for i in range(3):
    MEAtotal[i] = MEAtotal[i]*100/len(MEA)
    NTStotal[i] = NTStotal[i]*100/len(NTS)

plt.figure(figsize=(5,1.6))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.subplot(1,2,1)
plt.bar(np.arange(1,4)-0.2,NTStotal,width=0.4,label='NTS')
plt.bar(np.arange(1,4)+0.2,MEAtotal,width=0.4,label='MEA')
plt.legend()
plt.title('Weekday')
plt.ylabel('Probability')
plt.ylim(0,100)
plt.grid()
NTS2= {}
MEA2 = {}

NTStotal2 = [0]*3
MEAtotal2 = [0]*3
# get the labels for both data types
with open(stem+'NTSlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS2[row[0]] = int(row[1])
        NTStotal2[int(row[1])] += 1
        
with open(stem+'MEAlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA2[row[0]] = int(row[1])
        MEAtotal2[int(row[1])] += 1

for i in range(3):
    MEAtotal2[i] = MEAtotal2[i]*100/len(MEA2)
    NTStotal2[i] = NTStotal2[i]*100/len(NTS2)

plt.subplot(1,2,2)
plt.bar(np.arange(1,4)-0.2,NTStotal2,width=0.4)
plt.bar(np.arange(1,4)+0.2,MEAtotal2,width=0.4)
plt.grid()
plt.title('Weekend')
plt.ylabel('Probability')
plt.ylim(0,100)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/clusterPdfs.eps', format='eps', dpi=1000)
#plt.show()

# first let's store the individual pdf
with open(stem+'clusterPdf.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Cluster','MEA','NTS'])
    for i in range(3):
        writer.writerow([i+1,MEAtotal[i],NTStotal[i]])


with open(stem+'clusterPdfWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Cluster','MEA','NTS'])
    for i in range(3):
        writer.writerow([i+1,MEAtotal2[i],NTStotal2[i]])

# now we need to get the individual cluster start of charging pdfs
chargingPdf = []
chargingPdfWE = []
chargingPdf2 = []
chargingPdfWE2 = []
nCharges = {}
nChargesWE = {}
for i in range(3):
    chargingPdf.append([0]*48)
    chargingPdfWE.append([0]*48)
    chargingPdf2.append([0]*48)
    chargingPdfWE2.append([0]*48)

# now get the MEA data
with open(data2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]+str(int(int(row[1])/7))
        day = int(row[1])%7
        
        if row[-1] == '0':
            pdf = chargingPdf
            pdf2 = chargingPdf2
            cls = MEA
            nc = nCharges
        else:
            pdf = chargingPdfWE
            pdf2 = chargingPdfWE2
            cls = MEA2
            nc = nChargesWE
        
        start = int(int(row[2])/30)
        if start >= 48:
            start -= 48
            
        if vehicle not in nc:
            nc[vehicle] = {0:0,1:0,2:0,3:0,4:0,5:0,6:0} # we would expect either 2 or 5 of these to be 0

        try:
            pdf[cls[vehicle]][start] += 1
        except:
            continue
            
        if nc[vehicle][day] == 0:
            nc[vehicle][day] = 1
            
        else:
            nc[vehicle][day] += 1
            '''
            try:
                pdf2[cls[vehicle]][start] += 1
            except:
                continue
            '''
              

# now get pdfs
nChargesPdf = []
nChargesPdfWE = []
for i in range(3):
    nChargesPdf.append([0]*25)
    nChargesPdfWE.append([0]*10)

for vehicle in nCharges:
    for d in nCharges[vehicle]:
        try:
            nChargesPdf[cls[vehicle]][nCharges[vehicle][d]] += 1
        except:
            continue
    try:
        nChargesPdf[cls[vehicle]][0] -= 2 # for weekend days
    except:
        continue
    
for vehicle in nChargesWE:
    for d in nChargesWE[vehicle]:
        try:
            nChargesPdfWE[cls[vehicle]][nChargesWE[vehicle][d]] += 1
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
        nChargesPdfWE[i][t] = nChargesPdfWE[i][t]/S
        exp += nChargesPdfWE[i][t]*t
    pIntWE.append(exp)

print(pInt)
print(pIntWE)

for i in range(3):
    s1 = sum(chargingPdf[i])
    s2 = sum(chargingPdfWE[i])
    s3 = sum(chargingPdf2[i])
    s4 = sum(chargingPdfWE2[i])
    for t in range(48):
        chargingPdf[i][t] = chargingPdf[i][t]*100/s1
        chargingPdfWE[i][t] = chargingPdfWE[i][t]*100/s2
        #chargingPdf2[i][t] = chargingPdf2[i][t]*100/s3
        #chargingPdfWE2[i][t] = chargingPdfWE2[i][t]*100/s4

plt.figure(figsize=(5,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']
clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}
n = 1
for i in range(3):
    plt.subplot(2,3,n)
    plt.plot(chargingPdf[i],c=clrs[str(i)])
    plt.xlim(0,47)
    plt.ylim(0,10)
    plt.grid()
    if n == 2:
        plt.title('Weekday')
    if n in [2,3,5]:
        plt.yticks([4,8],['',''])
    else:
        plt.yticks([0,4,8],['0%','4%','8%'])
    if n in []:#7,8,9]:
        plt.xticks([0,4,8],['',''])
    else:
        plt.xticks(x,x_ticks)
    n += 1
    
for i in range(3):
    plt.subplot(2,3,n)
    plt.plot(chargingPdfWE[i],c=clrs[str(i)],label=str(i))
    plt.xlim(0,47)
    plt.ylim(0,10)
    plt.grid()
    if n == 5:
        plt.title('Weekend')
    if n in [5,6]:
        plt.yticks([4,8],['',''])
    else:
        plt.yticks([0,4,8],['0%','4%','8%'])
    if n in []:#7,8,9]:
        plt.xticks([0,20,40],['',''])
    else:
        plt.xticks(x,x_ticks)
    n += 1
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/chargePdfs.eps', format='eps', dpi=1000)
'''
plt.figure(figsize=(5,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']
clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}
n = 1
for i in range(5):
    plt.subplot(4,3,n)
    plt.plot(chargingPdfWE[i],c=clrs[str(i)])
    plt.xlim(0,47)
    plt.ylim(0,10)
    plt.grid()
    if n == 2:
        plt.title('First Charge')
    if n in [2,3,5]:
        plt.yticks([4,8],['',''])
    else:
        plt.yticks([0,4,8],['0%','4%','8%'])
    if n in []:#7,8,9]:
        plt.xticks([0,4,8],['',''])
    else:
        plt.xticks(x,x_ticks)
    n += 1
        
n += 1
for i in range(5):
    plt.subplot(4,3,n)
    plt.plot(chargingPdfWE2[i],c=clrs[str(i)],label=str(i))
    plt.xlim(0,47)
    plt.ylim(0,10)
    plt.grid()
    if n == 8:
        plt.title('Additional Charge')
    if n in [8,9,11]:
        plt.yticks([4,8],['',''])
    else:
        plt.yticks([0,4,8],['0%','4%','8%'])
    if n in []:#7,8,9]:
        plt.xticks([0,4,8],['',''])
    else:
        plt.xticks(x,x_ticks)
    n += 1
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/chargePdfsWE.eps', format='eps', dpi=1000)
'''

plt.figure(figsize=(5,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.bar(np.arange(1,4)-0.2,pInt,width=0.4,label='Week')
plt.bar(np.arange(1,4)+0.2,pIntWE,width=0.4,label='Weekend')
plt.grid()
plt.ylabel('Expected Charges')
plt.xlabel('Cluster')
plt.legend()
plt.ylim(0,1.5)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/ncharges.eps', format='eps', dpi=1000)


# now let's store the individual pdf
with open(stem+'chargePdfW.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2','3','4'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [chargingPdf[i][t]]
        writer.writerow(row)
        
# now let's store the individual pdf
with open(stem+'chargePdfWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2','3','4'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [chargingPdfWE[i][t]]
        writer.writerow(row)
        
# now let's store the individual pdf
with open(stem+'chargePdfW2.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2','3','4'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [chargingPdf2[i][t]]
        writer.writerow(row)
        
# now let's store the individual pdf
with open(stem+'chargePdfWE2.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2','3','4'])
    for t in range(48):
        row = [t]
        for i in range(3):
            row += [chargingPdfWE2[i][t]]
        writer.writerow(row)

with open(stem+'nCharges.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['cluster','w','we'])
    for i in range(3):
        writer.writerow([i,pInt[i],pIntWE[i]])


plt.show()
