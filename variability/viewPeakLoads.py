# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8

ld = ['0%ev_total_load.csv','100%ev_total_load.csv','100%ev_opt_total_loads.csv']
x_ticks = ['No EVs','Uncontrolled\nCharging','Load Flattening\nCharging']

peaks = []
for sim in range(0,3):
    peaks.append([])
    
    with open(ld[sim],'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == []:
                continue
            x = []
            
            for i in range(0,1440):
                x.append(float(row[i]))

            peaks[sim].append(max(x)/55)

plt.boxplot(peaks,0,'')
plt.xticks(range(1,4),x_ticks)
plt.grid()
plt.ylabel('Peak Demand Per Household (kW)')

plt.show()
            
