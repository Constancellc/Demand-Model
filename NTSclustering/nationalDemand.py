import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from newChargingModel import MC_Simulation

#data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

outstem = '../../Documents/simulation_results/NTS/national/'

nV = 50
nMC = 40

population = 66020000
rt_perc = {'1':0.369,'2':0.446,'3':0.092,'4':0.093}

yearLim = 2015
hh = {'1':[],'2':[],'3':[],'4':[]}
nP = {'1':0,'2':0,'3':0,'4':0}
with open('../../Documents/UKDA-5340-tab/constance-households.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if int(row[-1]) > yearLim:
            try:
                hh[row[2]].append(row[0])
                nP[row[2]] += int(row[4])
            except:
                continue

new = [0]*1440
new_l = [0]*1440
new_u = [0]*1440
old = [0]*1440
for rt in hh:
    print(rt)
    if rt in ['1','2']:
        s = MC_Simulation(hh[rt],kWh_per_mile=[0.3161,0.3699])
    else:
        s = MC_Simulation(hh[rt],kWh_per_mile=[0.2533,0.3699])
    [m,l,u] = s.uncontrolledCharge(3.5,30,10)
    #c1 = s.uncontrolledCharge(3.5,60,1)
    print('done')
    c2 = s.dumbCharge(3.5,30)
    print('done2')
    for t in range(1440):
        new[t] += m[t+1440*2]*population*rt_perc[rt]/nP[rt]
        new_l[t] += l[t+1440*2]*population*rt_perc[rt]/nP[rt]
        new_u[t] += u[t+1440*2]*population*rt_perc[rt]/nP[rt]
        old[t] += c2[t+1440*2]*population*rt_perc[rt]/nP[rt]

with open(outstem+'uncontrolled.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','old','new','new-','new+'])
    for t in range(1440):
        writer.writerow([t,old[t],new[t],new_l[t],new_u[t]])
