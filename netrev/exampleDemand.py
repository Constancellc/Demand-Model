import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import datetime
import copy

hh = '30054'

base = '../../Documents/netrev/constance/EVcustomers10minData.csv'

def v_shift(p,e):
    if e < 3.5:
        return p
    nC = int(e/3.5)
    best = None
    peak = 10
    for t in range(144):
        p_ = []
        for t2 in range(nC):
            if t+t2 < 144:
                p_.append(p[t+t2])
            else:
                p_.append(p[t+t2-144])
        if max(p_) < peak:
            peak = max(p_)
            best = t

    new = copy.deepcopy(p)
    for t in range(nC):
        if best+t < 144:
            new[best+t] += 3.5
        else:
            new[best+t-144] += 3.5

    return new

def v_fill(p,e):
    p_ = copy.deepcopy(p)
    while e > 0:
        continue
        
profiles = {}
with open(base,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locID = row[0]
        if locID != hh:
            continue

        dayNo = int(row[1])

        if dayNo not in profiles:
            profiles[dayNo] = {}
            
        typ = row[2]

        profile = []
        for i in range(0,144):
            profile.append(float(row[3+i]))
            
        profiles[dayNo][typ] = profile

for dayNo in profiles:
    p1 = profiles[dayNo]['House data']
    p2 = profiles[dayNo]['Charge point']
    p3 = []
    for t in range(144):
        p3.append(p1[t]-p2[t])

    y_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
    y = range(12,156,24)
    plt.figure()
    plt.rcParams["font.family"] = 'serif'
    plt.rcParams["font.size"] = '14'
    plt.plot(p3,c='b',lw=3,label='Before')
    plt.plot(p1,c='r',lw=3,ls='--',label='After')
    plt.legend()
    plt.ylim(0,1.1*max(p1))
    plt.xticks(y,y_ticks)
    plt.ylabel('Power (kW)')
    plt.title('A Household\'s Power Demand Before and After EV Charging')
    plt.xlabel('Time')
    plt.grid()
    plt.xlim(0,144)
    plt.show()

    p4 = v_shift(p3,sum(p2))
    plt.figure()
    y_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
    y = range(12,156,24)
    plt.figure()
    plt.rcParams["font.family"] = 'serif'
    plt.rcParams["font.size"] = '14'
    plt.plot(p3,c='b',lw=3,label='Before')
    plt.plot(p4,c='r',lw=3,ls='--',label='After')
    plt.legend()
    plt.ylim(0,1.1*max(p1))
    plt.xticks(y,y_ticks)
    plt.ylabel('Power (kW)')
    plt.title('A Household\'s Power Demand Before and After EV Charging')
    plt.xlabel('Time')
    plt.grid()
    plt.xlim(0,144)
    plt.show()
                         
