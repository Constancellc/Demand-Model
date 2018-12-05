import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from newChargingModel import MC_Simulation2

#data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

outstem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'

nH = 50
nMC = 40

locs = {}
# get the locations of all vehicles
lType = 2 # 1-ward, 2-la, 3-ua, 4-county, 5-country
with open('../../Documents/UKDA-7553-tab/constance/hh-loc.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:  
        if row[lType] not in locs:
            locs[row[lType]] = []
        locs[row[lType]].append(row[0])
            
# for each location
for l in locs:
    print(l)
    sim = MC_Simulation2(locs[l],nH,nMC,kWh_per_mile=[0.3161,0.3699])
    sim.dumbAndUncontrolled(3.5,30,outstem+l+'.csv')
    del sim

