# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import sys

data = []

N = []

for i in range(1,58):
    with open('../../Documents/HH_demand_by_acorn_type/'+str(i)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        peaks = []
        avs = []
        c = 0
        for row in reader:
            h = 0
            m = 0
            c += 1
            for j in range(len(row)):
                if float(row[j]) > h:
                    h = float(row[j])
                m += float(row[j])/len(row)
            peaks.append(h)
            avs.append(m)
            
        N.append(c)
        data.append(avs)#peaks)
        
tot = sum(N)
for i in range(len(N)):
    N[i] = N[i]*100/tot

plt.figure(1)
plt.subplot(2,1,1)
plt.title('Average HH Power Consumption by ACORN Type')
plt.boxplot(data,0,'',whis=[5, 95])
plt.ylabel('Power (kW)')
plt.xlim(0,len(N)+1)
plt.grid()
plt.subplot(2,1,2)
plt.bar(range(1,len(N)+1),N)
plt.xlim(0,len(N)+1)
plt.ylabel('Percentage of data')
plt.xlabel('ACORN Type')
plt.grid()
'''
plt.subplot(2,1,2)
plt.boxplot(data[29:],0,'',whis=[5, 95])


plt.figure(2)
plt.subplot(2,1,1)
plt.bar(range(0,29),N[:29])
plt.subplot(2,1,2)
plt.bar(range(29,len(N)),N[29:])
'''
plt.show()

        



            
