import csv
import matplotlib.pyplot as plt
import random
import numpy as np

cens = '../../../Documents/census/'
stem = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'

# first the census data
nCars = {}
with open(cens+'cars-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3:
            continue
        try:
            a = float(row[2])
        except:
            continue
        
        lsoa = row[1]

        avCars = (float(row[3])+float(row[4])*2+float(row[5])*3+float(row[6])*4)\
                 /(float(row[2])+float(row[3])+float(row[4])+float(row[5])+
                   float(row[6]))
        nCars[lsoa] = avCars

driveToWork = {}
with open(cens+'methodToWork-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3:
            continue
        try:
            a = float(row[2])
        except:
            continue
        
        lsoa = row[1]

        per = round((float(row[3])+float(row[4]))/float(row[2]),2)
        driveToWork[lsoa] = per

distToWork = {}
with open(cens+'distToWork-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3:
            continue
        try:
            a = float(row[2])
        except:
            continue
        
        lsoa = row[1]
        distToWork[lsoa] = round(0.621371*float(row[3])/float(row[2]),2)

pop = {}
with open(cens+'population-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3:
            continue
        try:
            a = float(row[2])
        except:
            continue
        pop[row[1]] = int(row[2])

nHH = {}
with open(cens+'nHh-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3:
            continue
        try:
            a = float(row[2])
        except:
            continue
        nHH[row[1]] = int(row[2])


# now the LSOA electricity

elec = '../../../Documents/elec_demand/LSOA_domestic_electricity_2017.csv'
elec2 = '../../../Documents/elec_demand/MSOA_domestic_electricity_2016.csv'
gas = '../../../Documents/elec_demand/LSOA_domestic_gas_2017.csv'

# I need a way to predict % e& - maybe assume all hh not with gas on e7?
'''
nGas = {}

with open(gas,'rU',encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        nGas[row[5]] = int(row[-3])
'''
lsoa2msoa = {}
e7 = {}
avKWh = {}
with open(elec,'rU',encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        lsoa = row[5]#[1:-1]
        msoa = row[3]
        mean = row[-2]#[1:-1]
        if len(mean) < 2:
            continue
        lsoa2msoa[lsoa] = msoa
        '''
        n = int(row[-3])
        try:
            e7[lsoa] = round((n-nGas[lsoa])/n,3)
        except:
            e7[lsoa] = 0
        '''
        avKWh[lsoa] = float(mean)

nE7 = {}
nStd = {}
with open(elec2,'r+',encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        # lsoa = row[5]
        msoa = row[3]
        if msoa == '':
            continue

        if msoa not in nE7:
            nE7[msoa] = 0
            nStd[msoa] = 0
        
        nE7[msoa] += int(row[8])# total number of E7 meters
        nStd[msoa] += int(row[7])# total number of standard standard


for lsoa in lsoa2msoa:
    try:
        msoa = lsoa2msoa[lsoa]
        e7[lsoa] = 100*nE7[msoa]/(nE7[msoa]+nStd[msoa])
    except:
        e7[lsoa] = 10
        
with open(stem+'lsoaX.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LSOA','vehicles per HH','Av Commute (mi)','% by car',
                     'people per HH','%e7','kWh per meter','nHH'])
    for l in nCars:
        
        try:
            writer.writerow([l,nCars[l],distToWork[l],driveToWork[l],
                             round(pop[l]/nHH[l],2),e7[l],avKWh[l],nHH[l]])
        except:
            continue
        
