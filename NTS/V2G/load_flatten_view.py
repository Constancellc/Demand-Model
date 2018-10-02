import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

pen = 50

l1 = []
t1 = []
l2 = []
t2 = []
with open('../../../Documents/simulation_results/NTS/v2g/v2g_lf'+\
          str(pen)+'.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        l1.append(float(row[1])/50)
        t1.append(float(row[2])/(0.5*pen))
        l2.append(float(row[3])/50)
        t2.append(float(row[4])/(0.5*pen))

plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.subplot(2,1,1)
plt.ylabel('Peak Demand\nPer Household (kW)')
plt.boxplot([l1,l2],sym='')
plt.xticks([1,2],['Uni-directional','Bi-directional'])
plt.ylim(0,0.8)
plt.grid()
plt.subplot(2,1,2)
plt.boxplot([t1,t2],sym='')
plt.xticks([1,2],['Uni-directional','Bi-directional'])
plt.ylabel('Average Throughput\nPer EV Battery (kWh)')
plt.grid()
plt.ylim(0,10)
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
