import csv
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/simulation_results/NTS/clustering/power/'

m = []
l = []
u = []
m2 = []
l2 = []
u2 = []
with open(stem+'charging.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        m.append(float(row[1])/50)
        l.append((float(row[1])-np.sqrt(float(row[2])))/50)
        u.append((float(row[1])+np.sqrt(float(row[2])))/50)
        m2.append(float(row[3])/50)
        l2.append((float(row[3])-np.sqrt(float(row[4])))/50)
        u2.append((float(row[3])+np.sqrt(float(row[4])))/50)
        
plt.figure(figsize=(5,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.plot(m)
plt.fill_between(range(len(m)),l,u,alpha=0.2)
plt.plot(m2)
plt.fill_between(range(len(m)),l2,u2,alpha=0.2)


plt.xlim(0,1440)
plt.xticks([2*60,6*60,10*60,14*60,18*60,22*60],
           ['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.grid()
plt.ylabel('Power Demand (kW)')
plt.ylim(0,1.8)
plt.legend()
plt.tight_layout()
plt.show()
'''
m = []
l = []
u = []
m2 = []
l2 = []
u2 = []
with open(stem+'available.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        m.append(float(row[1])/50)
        l.append((float(row[1])-np.sqrt(float(row[2])))/50)
        u.append((float(row[1])+np.sqrt(float(row[2])))/50)
        m2.append(float(row[3])/50)
        l2.append((float(row[3])-np.sqrt(float(row[4])))/50)
        u2.append((float(row[3])+np.sqrt(float(row[4])))/50)
        
plt.figure(figsize=(5,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.plot(m)
plt.fill_between(range(len(m)),l,u)
plt.plot(m2)
plt.fill_between(range(len(m)),l2,u2)


plt.xlim(0,1440)
plt.xticks([2*60,6*60,10*60,14*60,18*60,22*60],
           ['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.grid()
plt.ylabel('Power Demand (kW)')
plt.ylim(0,1.8)
plt.legend()
plt.tight_layout()
plt.show()

            
 '''         
          
            
