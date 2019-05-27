import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import datetime

# first fi
distances = {'w':{},'we':{}}
nTrips = {'w':{},'we':{}}

avTrip = {'w':[0]*48,'we':[0]*48}

def normalise(p):
    p2 = [0]*len(p)
    s = sum(p)
    for i in range(len(p)):
        p2[i] = p[i]/s
    return p2

with open('../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[-1] == '1':
            ty = 'we'
        else:
            ty = 'w'
            
        userID = row[0]+'_'+row[1]
        if userID not in nTrips[ty]:
            nTrips[ty][userID] = 1
            distances[ty][userID] = float(row[4])/1609
        else:
            nTrips[ty][userID] += 1
            distances[ty][userID] += float(row[4])/1609

        for t in range(int(row[2]),int(row[3])):
            if t < 1440:
                avTrip[ty][int(t/30)] += 1
            else:
                avTrip[ty][int((t-1440)/30)] += 1

distances2 = {'w':{},'we':{}}
nTrips2 = {'w':{},'we':{}}

avTrip2 = {'w':[0]*48,'we':[0]*48}

with open('../../Documents/UKDA-5340-tab/constance-trips.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[2] == '':
            continue
        if int(row[6]) > 5:
            ty = 'we'
        else:
            ty = 'w'
            
        userID = row[2]+'_'+row[6]
        if userID not in nTrips2[ty]:
            nTrips2[ty][userID] = 1
            distances2[ty][userID] = float(row[-4])
        else:
            nTrips2[ty][userID] += 1
            distances2[ty][userID] += float(row[-4])

        try:
            s = int(row[-6])
            e = int(row[-5])
        except:
            continue
        if e < s:
            e += 1440

        for t in range(s,e):
            if t < 1440:
                avTrip2[ty][int(t/30)] += 1
            else:
                avTrip2[ty][int((t-1440)/30)] += 1
                
_dist = {'w':[0]*20,'we':[0]*20}
_nTrips = {'w':[0]*15,'we':[0]*15}
_dist2 = {'w':[0]*20,'we':[0]*20}
_nTrips2 = {'w':[0]*15,'we':[0]*15}

for t in ['w','we']:
    for v in distances[t]:
        try:
            _nTrips[t][int(nTrips[t][v])] += 1
        except:
            continue
        try:
            _dist[t][int(float(distances[t][v])/5)] += 1
        except:
            continue
    for v in distances2[t]:
        try:
            _nTrips2[t][int(nTrips2[t][v])] += 1
        except:
            continue
        try:
            _dist2[t][int(float(distances2[t][v])/5)] += 1
        except:
            continue
    _dist[t] = normalise(_dist[t])
    _dist2[t] = normalise(_dist2[t])
    _nTrips2[t] = normalise(_nTrips2[t])
    _nTrips[t] = normalise(_nTrips[t])
    avTrip[t] = normalise(avTrip[t])
    avTrip2[t] = normalise(avTrip2[t])


plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 12

pn = {'w':1,'we':2}
pt = {'w':'Weekday','we':'Weekend'}
for t in ['w','we']:
    plt.figure(1,figsize=(8.5,3))
    plt.subplot(1,2,pn[t])
    plt.bar(np.arange(0,15)-0.2,_nTrips2[t],width=0.4,label='NTS')
    plt.bar(np.arange(0,15)+0.2,_nTrips[t],width=0.4,label='MEA')
    plt.xlabel('Number of Trips per Day')
    plt.xlim(0,12)
    if t == 'w':
        plt.ylabel('Probability')
    plt.title(pt[t],y=0.85)
    plt.grid()
    if t == 'we':
        plt.legend()
        plt.tight_layout()
        plt.savefig('../../Dropbox/thesis/chapter3/img/mea_nts_trips.eps',
                    format='eps',dpi=1000, bbox_inches='tight', pad_inches=0.)
        
    plt.figure(2,figsize=(8.5,3))
    plt.subplot(1,2,pn[t])
    plt.bar(np.arange(0,100,5)+4,_dist2[t],width=2,label='NTS')
    plt.bar(np.arange(0,100,5)+6,_dist[t],width=2,label='MEA')
    plt.xlabel('Daily Distance (miles)')
    plt.xlim(0,104)
    if t == 'w':
        plt.ylabel('Probability')
    plt.title(pt[t],y=0.85)
    plt.grid()
    if t == 'we':
        plt.tight_layout()
        plt.savefig('../../Dropbox/thesis/chapter3/img/mea_nts_dist.eps',
                    format='eps',dpi=1000, bbox_inches='tight', pad_inches=0.)
    
    plt.figure(3,figsize=(8.5,3))
    plt.subplot(1,2,pn[t])
    if t == 'w':
        plt.ylabel('Likelihood')
    plt.title(pt[t],y=0.85)
    plt.grid()
    plt.plot(np.linspace(0,24,num=48),avTrip2[t])
    plt.plot(np.linspace(0,24,num=48),avTrip[t])
    plt.xticks([4,12,20],['04:00','12:00','20:00'])
    plt.xlim(0,24)
    plt.ylim(0,0.07)
    if t == 'we':
        plt.tight_layout()
        plt.savefig('../../Dropbox/thesis/chapter3/img/mea_nts_prof.eps',
                    format='eps',dpi=1000, bbox_inches='tight', pad_inches=0.)
plt.show()
