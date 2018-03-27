# packages
import matplotlib.pyplot as plt
import numpy as np
import csv

resultsStem = '../../Documents/simulation_results/NTS/national_stochastic/'

plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = 8

t = []
base = []
p1 = []
p2 = []
p3 = []
p4 = []
p5 = []

with open(resultsStem+'1_planned.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        t.append(float(row[0]))
        base.append(float(row[1]))
        p1.append(float(row[2]))
        p2.append(float(row[3]))
        p3.append(float(row[4]))
        p4.append(float(row[5]))
        p5.append(float(row[6]))

min1 = []
max1 = []
min2 = []
max2 = []

for i in range(len(base)):
    lowest = 100
    highest = 0
    for p in [p2,p3,p4]:
        if p[i] < lowest:
            lowest = p[i]
        if p[i] > highest:
            highest = p[i]
            
    min1.append(lowest)
    max1.append(highest)
    
    for p in [p1,p5]:
        if p[i] < lowest:
            lowest = p[i]
        if p[i] > highest:
            highest = p[i]
            
    min2.append(lowest)
    max2.append(highest)
#plt.subplot(1,2,1)
plt.plot(t,base,'k',ls=':')
plt.plot(t,p3,'b')
plt.fill_between(t,min1,max1,color='b',alpha=0.1)
plt.fill_between(t,min2,max2,color='b',alpha=0.1)

x = np.linspace(26*60,46*60,num=6)
x_ticks = ['02:00','08:00','12:00','16:00','18:00','22:00']
plt.xticks(x,x_ticks)
plt.xlim(24*60,48*60)
plt.grid()
'''

p1 = []
p2 = []
p3 = []
p4 = []
p5 = []

with open(resultsStem+'1_planned.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p1.append(float(row[2]))
        p2.append(float(row[3]))
        p3.append(float(row[4]))
        p4.append(float(row[5]))
        p5.append(float(row[6]))

min1 = []
max1 = []
min2 = []
max2 = []

for i in range(len(base)):
    lowest = 100
    highest = 0
    for p in [p2,p3,p4]:
        if p[i] < lowest:
            lowest = p[i]
        if p[i] > highest:
            highest = p[i]
            
    min1.append(lowest)
    max1.append(highest)
    
    for p in [p1,p5]:
        if p[i] < lowest:
            lowest = p[i]
        if p[i] > highest:
            highest = p[i]
            
    min2.append(lowest)
    max2.append(highest)
plt.subplot(1,2,2)
plt.plot(t,base,'k',ls=':')
plt.plot(t,p3,'g')
plt.fill_between(t,min1,max1,color='g',alpha=0.2)
plt.fill_between(t,min2,max2,color='g',alpha=0.1)

x = np.linspace(26*60,46*60,num=6)
x_ticks = ['02:00','08:00','12:00','16:00','18:00','22:00']
plt.xticks(x,x_ticks)
plt.xlim(24*60,48*60)
plt.grid()
'''
plt.show()
