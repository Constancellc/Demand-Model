# packages
import csv
import random
import copy
import datetime
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/netrev/TC2a/'

# this section will extract the whol data
'''
day0 = datetime.datetime(2012,10,1)
hh = {}
with open(stem+'TrialMonitoringDataPassiv.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[1] in ['solar power','whole home power import']:
            if row[0] not in hh:
                hh[row[0]] = {}
            day = datetime.datetime(int(row[3][6:10]),int(row[3][3:5]),
                                    int(row[3][:2]))
            dayNo = (day-day0).days
            if dayNo not in hh[row[0]]:
                hh[row[0]][dayNo] = [0.0]*1440
                
            time = int(row[3][11:13])*60+int(row[3][14:16])

            hh[row[0]][dayNo][time] += float(row[4])

with open(stem+'1minProfiles.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Loc','Day','Time (mins)','Power (kW)'])
    for l in hh:
        for d in hh[l]:
            for t in range(1440):
                writer.writerow([l,d,t,hh[l][d][t]])
'''

hh = {}
with open(stem+'1minProfiles.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] not in hh:
            hh[row[0]] = {}
        if row[1] not in hh[row[0]]:
            hh[row[0]][row[1]] = [0]*1440
        hh[row[0]][row[1]][int(row[2])] = float(row[3])

def agg(p):
    p2 = [0]*48
    for t in range(1440):
        p2[int(t/30)] += p[t]/30
    return p2

def interpolate(p):
    p2 = [0]*1440
    for t in range(1440):
        a = int(t/30)
        f = float(t%30)/30
        if a < 47:
            b = a + 1
        else:
            b = a
        p2[t] = (1-f)*p[a]+f*p[b]
    return p2


def interpolate2(p):
    p2 = [0]*1440
    for t in range(1440):
        p2[int(t/30)] = p[t]
    return p2

def add_noise(p,v):
    p2 = []
    noise = np.random.normal(0,v,1440)
    for t in range(1440):
        p2.append(p[t]*(1+noise[t]))
        #p2.append(p[t]+noise[t])
    return p2

def error(a,b):
    e = 0
    for t in range(1440):
        e += np.power(a[t]-b[t],2)
    return np.sqrt(e/1440)

x = np.arange(0.02,0.8,0.02)
y = [0]*len(x)

def find_best_noise(p):
    p_ = interpolate2(p)# or 1 depending on filling wanted
    lowest = 10000000
    best = None
    for i in range(len(x)):
        v = x[i]#in np.arange(0.02,0.5,0.02):
        for sim in range(10):
            p2 = add_noise(p_,v)
            e = error(p2,p)
            if e < lowest:
                lowest = e
                best = v
    return best


for h in hh:
    for d in hh[h]:
        v = find_best_noise(hh[h][d])
        for i in range(len(x)):
            if x[i] == v:
                y[i] += 1

plt.figure()
plt.bar(x,y,width=0.01)
plt.show()
'''
y = [0]*300

for h in hh:
    for d in hh[h]:
        
        #plt.figure()
        #plt.plot(hh[h][d])
        p = agg(hh[h][d])
        #p_ = interpolate(p)
        #p2 = add_noise(p_,0.1)
        #plt.plot(p2)
        try:
            r = max(hh[h][d])/max(p)
        except:
            continue
        #print(r)
        try:
            y[int(100*(r-1))] += 1
        except:
            y[-1] += 1
        #plt.plot(np.arange(0,1440,30),p)
        #plt.show()

plt.bar(range(len(y)),y)
plt.show()


average = [0]*719

for h in hh:
    for d in hh[h]:
        data = hh[h][d]
        ps = np.abs(np.fft.fft(data))**2

        idx = range(1,720)
        p = ps[idx]

        for f in range(719):
            average[f] += p[f]

time_step = 60
freqs = np.fft.fftfreq(1440, time_step)

#plt.plot(freqs[idx], ps[idx])
plt.plot(freqs[idx],average)
plt.xlim(0.0005,0.017)
plt.show()
'''
