import csv
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.ndimage.filters as filt

journeyLogs = {}
with open('../../../Documents/UKDA-5340-tab/constance-trips.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        
        day = int(row[6])

        if day != 3:
            continue
        
        vehicle = row[2]
        
        if vehicle not in journeyLogs:
            journeyLogs[vehicle] = []

        try:
            shift = 30*random.random()
            start = int(30*int(int(row[9])/30)+shift)
            end = int(30*int(int(row[10])/30)+shift)
            distance = float(row[11]) # miles
            purpose = row[-2]
        except:
            continue

        kWh = distance
        if end < start:
            end += 1440

        journeyLogs[vehicle].append([start,end,kWh,purpose])

p_home = [0]*1440
dist = [0]*20
      
for v in journeyLogs:
    d = 0
    c = []
    for j in journeyLogs[v]:
        d += j[2]
        c.append([j[0],j[1]]) # to be clear these are times we cant charge
        if j[3] != '23':
            c.append([j[1],''])

    a = [0]*1440
    for i in range(len(c)):
        c_ = c[i]
        if c_[1] != '':
            for t in range(c_[0],c_[1]):
                if t < 1440:
                    a[t] = 1
                else:
                    a[t-1440] = 1
        elif i < len(c)-1:
            for t in range(c_[0],c[i+1][0]):
                if t < 1440:
                    a[t] = 1
                else:
                    a[t-1440] = 1
        else:
            for t in range(c_[0],c[0][0]):
                if t < 1440:
                    a[t] = 1
                else:
                    a[t-1440] = 1

    try:
        dist[int(d/10)] += 1
    except:
        continue

    for t in range(1440):
        p_home[t] += 1-a[t]

av = 0

for i in range(len(dist)):
    dist[i] = dist[i]/len(journeyLogs)
    av += 10*i*dist[i]

print(av)
for t in range(1440):
    p_home[t] = p_home[t]/len(journeyLogs)

#dist = filt.gaussian_filter1d(dist,1)


journeyLogs = {}

texas_hh = []
with open('../../../Documents/NHTS/constance/texas-hh.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if int(row[1]) == 3:
            texas_hh.append(row[0])

with open('../../../Documents/NHTS/constance/texas-trips.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        hh = row[1]
        if hh not in texas_hh:
            continue
        v = row[0]
        if v not in journeyLogs:
            journeyLogs[v] = []
            
        start = int(row[5])
        end = int(row[6])
        purp = row[-1]

        if purp in ['01','02']:
            home = True
        else:
            home = False

        kWh = float(row[7])

        journeyLogs[v].append([start,end,kWh,home])


p_home2 = [0]*1440
dist2 = [0]*20
      
for v in journeyLogs:
    d = 0
    c = []
    for j in journeyLogs[v]:
        d += j[2]
        c.append([j[0],j[1]]) # to be clear these are times we cant charge
        if j[3] == False:
            c.append([j[1],''])

    a = [0]*1440
    for i in range(len(c)):
        c_ = c[i]
        if c_[1] != '':
            for t in range(c_[0],c_[1]):
                if t < 1440:
                    a[t] = 1
                else:
                    a[t-1440] = 1
        elif i < len(c)-1:
            for t in range(c_[0],c[i+1][0]):
                if t < 1440:
                    a[t] = 1
                else:
                    a[t-1440] = 1
        else:
            for t in range(c_[0],c[0][0]):
                if t < 1440:
                    a[t] = 1
                else:
                    a[t-1440] = 1

    try:
        dist2[int(d/10)] += 1
    except:
        continue

    for t in range(1440):
        p_home2[t] += 1-a[t]

av = 0
for i in range(len(dist)):
    dist2[i] = dist2[i]/len(journeyLogs)
    av += 10*i*dist2[i]

print(av)
    
for t in range(1440):
    p_home2[t] = p_home2[t]/len(journeyLogs)
print(len(journeyLogs))
plt.figure(figsize=(6,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.plot(np.arange(0,120,10),dist[:12],c='b',label='UK')
plt.plot(np.arange(0,120,10),dist2[:12],c='g',ls='--',label='Texas')
plt.xlim(0,110)
plt.ylim(0,0.35)
plt.grid()
plt.xlabel('Distance (miles)')
plt.ylabel('Probability density')
plt.tight_layout()
plt.savefig('../../../Dropbox/papers/PES-GM-19/img/dist.eps',
            format='eps', dpi=1000)


plt.figure(figsize=(6,2.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.plot(np.linspace(0,24,num=1440),p_home,c='b',label='UK')
plt.plot(np.linspace(0,24,num=1440),p_home2,c='g',ls='--',label='Texas')
plt.xticks([2,6,10,14,18,22],['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.legend(ncol=2)
plt.xlim(0,24)
plt.ylim(0,1)
plt.grid()
plt.ylabel('Probability vehicle home')
plt.tight_layout()
plt.savefig('../../../Dropbox/papers/PES-GM-19/img/p_home.eps',
            format='eps', dpi=1000)

plt.show()
