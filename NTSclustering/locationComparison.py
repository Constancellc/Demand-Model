import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from chargingModel import MC_Sim

#data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

outstem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA/'

nV = 50
nMC = 40

locs = []
# get the locations of all vehicles
lType = 2 # 1-ward, 2-la, 3-ua, 4-county, 5-country
with open('../../Documents/UKDA-7553-tab/constance/hh-loc.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:  
        if row[lType] not in locs:
            locs.append(row[lType])
            
# for each location
for l in locs:
    sim = MC_Sim(nV,l,2)
    sim.run(nMC,outstem+l+'.csv')
    del sim
