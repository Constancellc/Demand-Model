import csv
import matplotlib.pyplot as plt
import numpy as np

crest = [0.0]*1440
meter = [0.0]*48

with open('../../Documents/household_demand_pool.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    t = 0
    for row in reader:
        for cell in row:
            crest[t] += float(cell)/len(row)
        t += 1
            
with open('../../Documents/household_demand_pool_HH.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for t in range(len(row)):
            meter[t] += float(row[t])/1000


x = np.arange(4,24,4)
x_ticks = ['04:00','08:00','12:00','16:00','20:00']

plt.figure(1)
plt.plot(np.linspace(0,24,num=48),meter,label='smart meter')
plt.plot(np.linspace(0,24,num=1440),crest,label='crest')
plt.grid()
plt.xlim(0,24)
plt.xticks(x,x_ticks)
plt.title('Demand averaged over 1000 households')
plt.legend()
plt.ylabel('Power (kW)')
plt.show()
