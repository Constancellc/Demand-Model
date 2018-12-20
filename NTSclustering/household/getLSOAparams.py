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
gas = '../../../Documents/elec_demand/LSOA_domestic_gas_2017.csv'

# I need a way to predict % e& - maybe assume all hh not with gas on e7?
nGas = {}

with open(gas,'rU',encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        nGas[row[5]] = int(row[-3])

e7 = {}
avKWh = {}
with open(elec,'rU',encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        lsoa = row[5]#[1:-1]
        mean = row[-2]#[1:-1]
        if len(mean) < 2:
            continue
        '''
        if len(mean) < 4:
            m = float(mean)
        else:
            m = float(mean[-3:])+1000*float(mean[:-4])
        '''
        n = int(row[-3])
        try:
            e7[lsoa] = round((n-nGas[lsoa])/n,3)
        except:
            e7[lsoa] = 0
        avKWh[lsoa] = float(mean)


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
        
