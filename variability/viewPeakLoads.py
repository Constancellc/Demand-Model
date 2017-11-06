# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8



ld = ['0%ev_total_load.csv','100%ev_total_load.csv',
         '100%TOUev_total_load.csv','100%ev_opt_total_loads.csv']
x_ticks = ['No EVs','Uncontrolled\nCharging','TOU\nCharging','Load Flattening\nCharging']

res = [1,30]
for r in range(0,2):
    plt.subplot(2,1,r+1)
    peaks = []
    for sim in range(0,4):
        peaks.append([])
        
        with open(ld[sim],'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row == []:
                    continue
                x = [0.0]*int(1440/res[r])
                
                for i in range(0,1440):
                    x[int(i/res[r])] += float(row[i])/res[r]

                peaks[sim].append(max(x)/55)

    plt.boxplot(peaks,0,'',whis=[0.25, 97.5])
    if r == 1:
        plt.xticks(range(1,len(ld)+1),x_ticks)
    else:
        plt.xticks(range(1,len(ld)+1),['']*len(ld))
    plt.grid()
    plt.ylim(0.5,3.0)
    plt.ylabel('Peak Demand\nPer Household (kW)')
    plt.title(str(res[r])+'min resolution')
    #plt.ylim(0.5,2.2)

plt.savefig('../../papers/PES-GM/peak_load',format='eps')
plt.show()
            
