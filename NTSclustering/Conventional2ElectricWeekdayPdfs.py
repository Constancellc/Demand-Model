import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from clustering import Cluster, ClusteringExercise

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

data2 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'

data3 = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

NTS = {}

# get the labels for both data types
with open(stem+'NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS[row[0]] = int(row[1])
        
NTS2 = {}
# get the labels for both data types
with open(stem+'NTSlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NTS2[row[0]] = int(row[1])

n = 0
c1 = [0]*7
c2 = [0]*7
c3 = [0]*7
c4 = [0]*7

nts_n = {'W':[0,0,0],'WE':[0,0,0]}
with open(stem+'allVehicles.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        vehicle = row[0]
        n += 1

        for day in range(5):
            try:
                c = NTS[vehicle+str(day+1)]
            except:
                c4[day] += 1
                continue
            nts_n['W'][c] += 1
            if c == 0:
                c1[day] += 1
            elif c == 1:
                c2[day] += 1
            elif c == 2:
                c3[day] += 1

        for day in range(5,7):
            try:
                c = NTS2[vehicle+str(day+1)]
            except:
                c4[day] += 1
                continue
            nts_n['WE'][c] += 1

            if c == 0:
                c1[day] += 1
            elif c == 1:
                c2[day] += 1
            elif c == 2:
                c3[day] += 1
print(nts_n)

for i in range(7):
    c1[i] = 100*(c1[i]+c2[i]+c3[i])/n                  
    c2[i] = 100*(c2[i]+c3[i])/n
    c3[i] = 100*c3[i]/n
    
plt.figure(figsize=(5,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.bar(range(7),[100]*7,color='#C0C0C0')
plt.bar(range(5),c1[:5],color='#FFBBBB')
plt.bar(range(5),c2[:5],color='#BBBBFF')
plt.bar(range(5),c3[:5],color='#BBFFBB')
plt.bar(range(5,7),c1[5:],color='#FFFFBB')
plt.bar(range(5,7),c2[5:],color='#FFBBFF')
plt.bar(range(5,7),c3[5:],color='#BBFFFF')
plt.xticks(range(7),['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
plt.legend(loc=[1.05,0.5])
plt.ylim(0,100)
plt.ylabel('Percentage')
#plt.grid(zorder=1)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/clustering/img/composition.eps', format='eps', dpi=1000)

nts_dist = {'W':[0,0,0],'WE':[0,0,0]}
with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[2]
        day = row[6]
        
        if int(row[6]) > 5:
            try:
                c = NTS2[vehicle+day]
            except:
                continue
            nts_dist['WE'][c] += float(row[11])
        else:
            try:
                c = NTS[vehicle+day]
            except:
                continue
            nts_dist['W'][c] += float(row[11])

for t in ['W','WE']:
    for i in range(3):
        print(nts_dist[t][i]/nts_n[t][i])
plt.show()
