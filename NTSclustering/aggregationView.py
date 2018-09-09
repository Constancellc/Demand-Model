import csv
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/simulation_results/NTS/clustering/power/'


nV = [10,20,30,40,50]

results = []
for i in range(len(nV)):
    results.append([])
    
with open(stem+'aggregation.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(len(row)-1):
            results[i].append(float(row[i+1]))
m = []
u = []
l = []

print(results)
for i in range(len(nV)):
    N = len(results[i])
    av = sum(results[i])/N
    v = 0
    for j in range(N):
        v += np.power(results[i][j]-av,2)/N
    v = np.sqrt(v)

    m.append(av)
    u.append(av+v)
    l.append(av-v)

plt.figure(figsize=(5,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'
plt.plot(nV,m)
plt.fill_between(nV,l,u,alpha=0.2)
plt.grid()
plt.ylim(0,1.1*max(u))

results = []
for i in range(len(nV)):
    results.append([])
    
with open(stem+'aggregation30.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(len(row)-1):
            results[i].append(float(row[i+1]))
m = []
u = []
l = []

print(results)
for i in range(len(nV)):
    N = len(results[i])
    av = sum(results[i])/N
    v = 0
    for j in range(N):
        v += np.power(results[i][j]-av,2)/N
    v = np.sqrt(v)

    m.append(av)
    u.append(av+v)
    l.append(av-v)

plt.plot(nV,m)
plt.fill_between(nV,l,u,alpha=0.2)
plt.tight_layout()
plt.show()
