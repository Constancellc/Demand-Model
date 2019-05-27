import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from newChargingModelTexas import MC_Simulation

#data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

outstem = '../../Documents/simulation_results/NHTS/national/'

nV = 50
nMC = 40

spr = ['3','4','5']
smr = ['6','7','8']
atm = ['9','10','11']
wtr = ['12','1','2']

population = 28304596
households = 7393354

hh_data = '../../Documents/NHTS/constance/texas-hh.csv'
hh = []
with open(hh_data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[2] not in wtr:
            continue
        if row[1] in ['6','7']:
            continue
        hh.append(row[0])

print(len(hh))
new = [0]*1440
new_l = [0]*1440
new_u = [0]*1440
old = [0]*1440
s = MC_Simulation(hh,kWh_per_mile=[0.3161,0.3699])
m = s.uncontrolledCharge(3.5,60)

c = s.dumbCharge(3.5,30)
# cheat! wrap around + scale for consistency
m2 = [0.0]*1440
c2 = [0.0]*1440
for t in range(2880):
    m2[t%1440] += m[t]
    c2[t%1440] += c[t]
sf = sum(c2)/sum(m2)
for t in range(1440):
    m2[t] = m2[t]*sf
    
plt.plot(m2)
plt.plot(c2)
print('done2')
for t in range(1440):
    new[t] += m2[t]*households/len(hh)
    old[t] += c2[t]*households/len(hh)

with open(outstem+'uncontrolled_wt.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['t','old','new','new-','new+'])
    for t in range(1440):
        writer.writerow([t,old[t],new[t],new_l[t],new_u[t]])

plt.show()
