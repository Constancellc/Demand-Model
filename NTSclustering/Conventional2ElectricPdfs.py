import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'


NTS = {}
MEA = {}

NTStotal = [0]*5
MEAtotal = [0]*5
# get the labels for both data types
with open('NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS[row[0]] = int(row[1])
        NTStotal[int(row[1])] += 1
        
with open('MEAlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA[row[0]] = int(row[1])
        MEAtotal[int(row[1])] += 1

for i in range(5):
    MEAtotal[i] = MEAtotal[i]*100/len(MEA)
    NTStotal[i] = NTStotal[i]*100/len(NTS)

plt.figure(figsize=(5,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.subplot(2,1,1)
plt.bar(np.arange(1,6)-0.2,NTStotal,width=0.4,label='NTS')
plt.bar(np.arange(1,6)+0.2,MEAtotal,width=0.4,label='MEA')
plt.legend()
plt.title('Weekday',y=0.7)
plt.ylabel('Probability')
plt.ylim(0,100)
plt.grid()
NTS2= {}
MEA2 = {}

NTStotal2 = [0]*5
MEAtotal2 = [0]*5
# get the labels for both data types
with open('NTSlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS2[row[0]] = int(row[1])
        NTStotal2[int(row[1])] += 1
        
with open('MEAlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA2[row[0]] = int(row[1])
        MEAtotal2[int(row[1])] += 1

for i in range(5):
    MEAtotal2[i] = MEAtotal2[i]*100/len(MEA2)
    NTStotal2[i] = NTStotal2[i]*100/len(NTS2)

plt.subplot(2,1,2)
plt.bar(np.arange(1,6)-0.2,NTStotal2,width=0.4)
plt.bar(np.arange(1,6)+0.2,MEAtotal2,width=0.4)
plt.grid()
plt.title('Weekend',y=0.7)
plt.ylabel('Probability')
plt.ylim(0,100)
plt.tight_layout()
#plt.show()

# first let's store the individual pdf
with open('clusterPdf.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Cluster','MEA','NTS'])
    for i in range(5):
        writer.writerow([i+1,MEAtotal[i],NTStotal[i]])

# now we need to get the individual cluster start of charging pdfs
chargingPdf = []
chargingPdfWE = []
for i in range(5):
    chargingPdf.append([0]*48)
    chargingPdfWE.append([0]*48)

# now get the MEA data
with open(data2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]+str(int(int(row[1])/7))
        if row[-1] == '0':
            pdf = chargingPdf
            cls = MEA
        else:
            pdf = chargingPdfWE
            cls = MEA2
        
        start = int(int(row[2])/30)
        if start > 47:
            start -= 48

        try:
            pdf[cls[vehicle]][start] += 1
        except:
            continue
        

for i in range(5):
    for t in range(48):
        chargingPdf[i][t] = chargingPdf[i][t]*100/sum(chargingPdf[i])
        chargingPdfWE[i][t] = chargingPdfWE[i][t]*100/sum(chargingPdfWE[i])

plt.figure(figsize=(5,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']
clrs = {'2':'g','3':'y','1':'b','0':'r','4':'c'}
n = 1
for i in range(5):
    plt.subplot(4,3,n)
    plt.plot(chargingPdf[i],c=clrs[str(i)])
    plt.xlim(0,47)
    plt.ylim(0,45)
    plt.grid()
    if n == 2:
        plt.title('(a)')
    if n in [2,3,5]:
        plt.yticks([20,40],['',''])
    else:
        plt.yticks([0,20,40],['0%','20%','40%'])
    if n in []:#1,2,3,4,5]:
        plt.xticks([8,24,40],['',''])
    else:
        plt.xticks(x,x_ticks)
    n += 1
        
n += 1
for i in range(5):
    plt.subplot(4,3,n)
    plt.plot(chargingPdfWE[i],c=clrs[str(i)],label=str(i))
    plt.xlim(0,47)
    plt.ylim(0,45)
    plt.grid()
    if n == 8:
        plt.title('(b)')
    if n in [8,9,11]:
        plt.yticks([20,40],['',''])
    else:
        plt.yticks([0,20,40],['0%','20%','40%'])
    if n in []:#7,8,9]:
        plt.xticks([8,24,40],['',''])
    else:
        plt.xticks(x,x_ticks)
    n += 1
plt.tight_layout()
#plt.show()

# now let's store the individual pdf
with open('chargePdfW.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2','3','4'])
    for t in range(48):
        row = [t]
        for i in range(5):
            row += [chargingPdf[i][t]]
        writer.writerow(row)
        
# now let's store the individual pdf
with open('chargePdfWE.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','0','1','2','3','4'])
    for t in range(48):
        row = [t]
        for i in range(5):
            row += [chargingPdfWE[i][t]]
        writer.writerow(row)       
