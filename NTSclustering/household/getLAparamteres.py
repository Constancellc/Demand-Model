import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

stem = '../../../Documents/simulation_results/NTS/clustering/labels2/'
trip_data = '../../../Documents/UKDA-5340-tab/constance-trips.csv'
hh_data = '../../../Documents/UKDA-5340-tab/constance-households.csv'
hh_loc = '../../../Documents/UKDA-7553-tab/constance/hh-loc.csv'
outstem = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'
trip_data0 = '../../../Documents/UKDA-5340-tab/tab/tripeul2016.tab'
locs = []
hh_l = {}
nH = {}


        
with open(hh_loc,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:  
        if row[2] not in locs:
            locs.append(row[2])
            nH[row[2]] = 0
        nH[row[2]] += 1
        hh_l[row[0]] = row[2]

cDist = {}
cMode = {}
veh = {}
nPeople = {}

for l in locs:
    cDist[l] = [0,0]
    cMode[l] = [0,0]
    veh[l] = []
    nPeople[l] = [0,0]


with open(trip_data0,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    next(reader)
    for row in reader:
        mode = row[20]
        hh = row[4]
        purp = row[31]
        dist = float(row[26])

        if purp != '1':
            continue
        

        if mode in ['5','6']:#,'7','8','9','10','11','12','13','14','15','16','17']:
            cMode[hh_l[hh]][0] += 1

        cMode[hh_l[hh]][1] += 1
        cDist[hh_l[hh]][0] += dist
        cDist[hh_l[hh]][1] += 1

with open(hh_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        try:
            nPeople[hh_l[row[0]]][0] += int(row[-2])
            nPeople[hh_l[row[0]]][1] += 1
        except:
            continue


with open(trip_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        hh = row[1]
        v = row[2]
        dist = float(row[11])
        purp = row[13]
        try:
            if v not in veh[hh_l[hh]]:
                veh[hh_l[hh]].append(v)
        except:
            continue
        '''
        if purp == '1':
            cDist[hh_l[hh]][0] += dist
            cDist[hh_l[hh]][1] += 1
        '''


with open(outstem+'NTSparams.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LA','Vehicles per HH','Av Commute (miles)',
                     '% Commute by car','Av People per HH'])
    for l in locs:
        row = [l]
        row += [len(veh[l])/nH[l]]
        try:
            row += [cDist[l][0]/cDist[l][1]]
        except:
            row += [0]
        try:
            row += [cMode[l][0]/cMode[l][1]]
        except:
            row += [0]
        row += [nPeople[l][0]/nPeople[l][1]]
        writer.writerow(row)
        
