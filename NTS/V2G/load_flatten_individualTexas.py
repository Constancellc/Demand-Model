import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag, sparse, solvers
import scipy.ndimage.filters as filt

# ok here is how it's going to go.
simulationDay = 3
nH = 311
c_eff = 0.9
capacity = 30 # kWh
pMax = 3.5 # kW
pMax_ = 3.5 # kW for V2G


def interpolate(x0,T):
    x1 = [0.0]*(len(x0)*T)
    for t in range(len(x1)):
        p1 = int(t/T)
        if p1 == len(x0)-1:
            p2 = p1
        else:
            p2 = p1+1
        f = float(t%T)/30
        x1[t] = (1-f)*x0[p1]+f*x0[p2]
    return x1

def v2g_eval(hh,e0,delta,constrain=[],limit=0):
    over = 0
    p = (e0+delta)/24
    p = p*(1440/(1440-len(constrain)))
    for t in range(1440):
        if hh[t] > p and (t not in constrain or p<limit):
            over += hh[t]/60
    return over

def flatten_v2g(hh,eV,constrain=[],limit=0):
    e0 = sum(hh)/60 + eV
    delta = 0
    for i in range(10):
        over = v2g_eval(hh,e0,delta,constrain,limit)
        delta = over*(1/0.81-1)

    out = []
    for t in range(1440):
        if t in constrain:
            if (e0+delta)/24 > limit and limit != 0:
                out.append(limit)
            else:
                out.append(hh[t])
        else:
            out.append((e0+delta)/24)

    out = filt.gaussian_filter1d(out,40)

    return [over,out]

def g2v_fill(tot,y,constrain=[],limit=0):
    en = 0
    for t in range(1440):
        if tot[t] < y and (t not in constrain or y<limit):
            en += (y-tot[t])/60
            tot[t] = y

    return [tot,en]

def flatten_g2v(hh,eV,constrain=[],limit=0):
    total = copy.deepcopy(hh)
    p = min(total)+0.1
    while eV > 0:
        [total,en] = g2v_fill(total,p,constrain,limit)
        eV -= en
        p += 0.01

    return total


# First we gotta get vehicle usage and household demand.

# Pick a simulation day (just going to loop round hehe)

# Get the list of all vehicles and journey logs
# get all Vehicles
'''
allVehicles = []
with open('../../../Documents/simulation_results/NTS/clustering/labels2/allVehicles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        allVehicles.append(row[0])

journeyLogs = {}
with open('../../../Documents/UKDA-5340-tab/constance-trips.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        
        day = int(row[6])
        
        if day != simulationDay:
            continue
        vehicle = row[2]
        
        if vehicle not in journeyLogs:
            journeyLogs[vehicle] = []

        try:
            start = int(30*int(int(row[9])/30)+30*random.random())
            end = int(30*int(int(row[10])/30)+30*random.random())
            distance = float(row[11]) # miles
            purpose = row[-2]
        except:
            continue

        kWh = distance*0.3

        if end < start:
            end += 1440

        journeyLogs[vehicle].append([start,end,kWh,purpose])
'''
# Get the HH demand, one from each hh
# get a list of hh?
# get household profiles
c = 0
hhProfiles = {}
with open('../../../Documents/pecan-street/hourly-texas/profiles.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p = [0.0]*48
        for t in range(48):
            p[t] += float(row[t])
        p = filt.gaussian_filter1d(p,1)
        hhProfiles[c] = p
        c += 1

# ok first get the households

chosenH = []
while len(chosenH) < nH:
    ranH = int(random.random()*len(hhProfiles))
    if ranH not in chosenH:
        chosenH.append(ranH)

totalH = [0.0]*1440
for h in chosenH:
    p = interpolate(hhProfiles[h],30)
    for t in range(1440):
        totalH[t] += p[t]

t_ = np.linspace(0,24,num=1440)
plt.figure(figsize=(3,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'

eV = nH*9
[over,tot1] = flatten_v2g(totalH,eV/0.9)
tot2 = flatten_g2v(totalH,eV/0.9)
plt.plot(t_,totalH,c='k',ls=':',label='Base')
plt.plot(t_,tot2,c='g',label='G2V')
plt.plot(t_,tot1,c='r',ls='--',label='V2G')
plt.ylim(0.7*min(totalH),1.3*max(tot2))
plt.xticks([4,12,20],['04:00','12:00','20:00'])
plt.xlim(0,24)
plt.yticks([250,500,750,1000],['0.2','0.4','0.6','0.8','1.0','1.2'])
plt.legend()
plt.ylabel('Power (MW)')
plt.grid()

plt.tight_layout()
plt.savefig('../../../Dropbox/papers/V2G/img/profiles2.eps',dpi=1000,
            format='eps')

plt.figure(figsize=(6,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'
# then get the vehicles
pn = 1
t_ = np.linspace(0,24,num=1440)
for pen in [1.0,0.5,0.25,0.1]:
    nV = int(nH*pen)
    eV = nV*9
    lim = None
    if pen == 0.25:
        constrain = list(range(657,730))+list(range(803,900))
        lim = 386
    elif pen == 0.1:
        constrain = list(range(487,673))+list(range(671,1060))
        lim = 210
    else:
        constrain = []

    [over,tot1] = flatten_v2g(totalH,eV/0.9,constrain,limit=lim)
    tot2 = flatten_g2v(totalH,eV/0.9,constrain,limit=lim)
    
    plt.subplot(2,2,pn)
    plt.plot(t_,totalH,c='k',ls=':',label='Base')
    plt.plot(t_,tot2,c='g',label='G2V')
    plt.plot(t_,tot1,c='r',ls='--',label='V2G')
    plt.title(str(int(100*pen))+'%',y=0.8)
    plt.ylim(0.7*min(totalH),1.3*max(tot2))
    plt.xticks([4,12,20],['04:00','12:00','20:00'])
    plt.xlim(0,24)
    if pn in [1,3]:
        plt.ylabel('Power (kW)')
    plt.grid()
    pn += 1
    if pn == 2:
        plt.legend(ncol=1,loc=2)

plt.tight_layout()
#plt.savefig('../../../Dropbox/papers/V2G/img/profiles2.eps',dpi=1000,
#            format='eps')
plt.show()

