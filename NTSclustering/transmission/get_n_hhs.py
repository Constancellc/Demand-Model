import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

def euclid(p1,p2):
    d = 0
    d += np.power(p1[0]-p2[0],2)
    d += np.power(p1[1]-p2[1],2)
    return np.sqrt(d)

def get_closest(bus_list,p):
    best = None
    closest = 10
    for i in bus_list:
        d = euclid(bus_list[i],p)
        if d < closest:
            closest = d
            best = i
    return best
    
census = '../../../Documents/census/'
stem = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'



locs = {}
with open(census+'centroids-LSOA-LatLon.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[0]] = [float(row[1]),float(row[2])]

dwellings = {}
with open(census+'dwellingType-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    for row in reader:
        if len(row) <= 5:
            continue
        lsoa = ''
        i = 0
        while row[0][i] != ' ':
            lsoa += row[0][i]
            i += 1
        dwellings[lsoa] = int(row[1])

pop = {}
with open(census+'population-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3:
            continue
        try:
            a = float(row[2])
        except:
            continue
        pop[row[1]] = int(row[2])

# now get node locations
subs = {}
nHH = {}
e7 = {}
nV = {}
com = {}
pc = {}
pop_ = {}
kWh = {}

with open('substations.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        subs[row[0]] = [float(row[3]),float(row[2])]
        nHH[row[0]] = 0
        e7[row[0]] = 0
        nV[row[0]] = 0
        com[row[0]] = 0
        pc[row[0]] = 0
        kWh[row[0]] = 0
        pop_[row[0]] = 0

with open(stem+'lsoaX.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        l = locs[row[0]]
        best = get_closest(subs,l)
        nV[best] += float(row[1])*dwellings[row[0]]
        
        com[best] += float(row[2])*dwellings[row[0]]
        
        pc[best] += float(row[3])*dwellings[row[0]]

        pop_[best] += pop[row[0]]
        nHH[best] += dwellings[row[0]]
        
        e7[best] += float(row[5])*dwellings[row[0]]

        kWh[best] += float(row[6])*dwellings[row[0]]


with open('substation_param.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Bus','vehicles per HH','Av Commute (mi)','% by car',
                     'people per HH','%e7','kWh per meter','nHH'])
    for b in nHH:
        if nHH[b] > 0:
            writer.writerow([b,nV[b]/nHH[b],com[b]/nHH[b],pc[b]/nHH[b],
                             pop_[b]/nHH[b],e7[b]/nHH[b],kWh[b]/nHH[b],
                             nHH[b]])
        else:
            writer.writerow([b]+[0.0]*7)
    
        
