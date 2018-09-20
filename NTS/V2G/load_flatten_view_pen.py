import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

bnft = []
cost = []
bnft_u = []
cost_u = []
bnft_l = []
cost_l = []

conf = 0.95
for pen in range(20,110,10):
    a = []
    b = []
    with open('../../../Documents/simulation_results/NTS/v2g/v2g_lf'+\
              str(pen)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            a.append(100*(float(row[1])-float(row[3]))/float(row[1]))
            b.append(100*(float(row[4])-float(row[2]))/float(row[2]))
            
    bnft.append(sum(a)/len(a))
    cost.append(sum(b)/len(b))
    a = sorted(a)
    b = sorted(b)
    bnft_u.append(a[int(conf*len(a))])
    cost_u.append(b[int(conf*len(b))])
    bnft_l.append(a[int((1-conf)*len(a))])
    cost_l.append(b[int((1-conf)*len(b))])
    

plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.subplot(2,1,1)
plt.plot(range(20,110,10),bnft)
plt.fill_between(range(20,110,10),bnft_l,bnft_u,alpha=0.2)
plt.ylabel('% Reduction in Peak Demand')
plt.grid()
plt.subplot(2,1,2)
plt.plot(range(20,110,10),cost)
plt.fill_between(range(20,110,10),cost_l,cost_u,alpha=0.2)
plt.ylabel('% Increase in Battery Throughput')
plt.grid()
plt.tight_layout()
plt.show()
        
'''
m1 = []
l1 = []
u1 = []

m2 = []
l2 = []
u2 = []

with open('../../../Documents/simulation_results/NTS/v2g_lf.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        m1.append(float(row[1])/50)
        u1.append(float(row[2])/50)
        l1.append(float(row[3])/50)
        m2.append(float(row[4])/50)
        u2.append(float(row[5])/50)
        l2.append(float(row[6])/50)

plt.figure()
plt.plot(m1)
plt.fill_between(range(1440),l1,u1,alpha=0.2)
plt.plot(m2)
plt.fill_between(range(1440),l2,u2,alpha=0.2)
plt.show()
'''
