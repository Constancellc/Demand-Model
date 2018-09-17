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



av1 = []
av1we = []
for i in range(1,4):
    av1.append([])
    av1we.append([])

    avT = []
    av2 = []
    avTwe = []
    av2we = []

    with open(outstem+'error'+str(i)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            av2.append(float(row[1]))
            av1[i-1].append(float(row[2]))
            avT.append(float(row[3]))
            av2we.append(float(row[4]))
            av1we[i-1].append(float(row[5]))
            avTwe.append(float(row[6]))

m = []
l = []
u = []
for t in range(1440):
    x = []
    for i in range(len(av1)):
        x.append(av1[i][t])
    l.append(min(x))
    u.append(max(x))
    m.append(sum(x)/len(av1))

plt.figure(figsize=(5,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
x = [2*60,6*60,10*60,14*60,18*60,22*60]
x_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
plt.subplot(2,1,1)
plt.plot(avT,label='True')
#plt.plot(m,label='(a)')
plt.fill_between(range(1440),l,u,alpha=0.2)
plt.plot(av2,label='(b)')
plt.xlim(0,1439)
plt.xticks(x,x_ticks)
plt.ylabel('Probability (%)')
plt.ylim(0,0.2)
plt.grid()
plt.title('Weekdays',y=0.8)
plt.legend()

m = []
l = []
u = []
for t in range(1440):
    x = []
    for i in range(len(av1)):
        x.append(av1we[i][t])
    l.append(min(x))
    u.append(max(x))
    m.append(sum(x)/len(av1))
    
plt.subplot(2,1,2)
plt.plot(avTwe,label='True')
plt.plot(m,label='(a)')
plt.fill_between(range(1440),l,u,alpha=0.2)
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
