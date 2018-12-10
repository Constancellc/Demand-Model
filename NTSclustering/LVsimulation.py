import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from newChargingModel import MC_Simulation2, MC_Simulation

#data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

outstem = '../../Documents/simulation_results/NTS/clustering/power/E06000013/'

nH = 50
nMC = 40

hh = []
l = 'E06000013'
# get the locations of all vehicles
lType = 2 # 1-ward, 2-la, 3-ua, 4-county, 5-country
with open('../../Documents/UKDA-7553-tab/constance/hh-loc.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:  
        if row[lType] == l:
            hh.append(row[0])
'''           
# for each location
for mc_ in range(40):
    sim = MC_Simulation2(hh,nH,nMC,kWh_per_mile=[0.3161,0.3699])
    sim.dumbAndUncontrolled(3.5,30,outstem+str(mc_+10)+'.csv')
    del sim
'''
sim = MC_Simulation(hh,nH,kWh_per_mile=[0.3161,0.3699])
d = sim.dumbCharge(3.5,30)[2*1440:3*1440]
[m,l,u] = sim.uncontrolledCharge(3.5,30,nSim=40)

with open(outstem+'single.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','u_m','u_l','u_u','d'])
    for t in range(1440):
        row = [t+1440*2]
        row += [m[t+1440*2]]
        row += [l[t+1440*2]]
        row += [u[t+1440*2]]
        row += [d[t]]
        writer.writerow(row)
