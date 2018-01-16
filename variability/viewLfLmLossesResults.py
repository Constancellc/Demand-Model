# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)

totals = {0:[],1:[]}

with open('results/lf_lm_losses.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        for i in range(len(row)-1):
            totals[i].append(float(row[i]))

x2_ticks = ['Load\nFlattening','Loss\nMinimizing']
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
plt.boxplot([totals[0],totals[1]],0,'',whis=[0.05, 99.5])
plt.xticks([1,2],x2_ticks)
plt.grid()
plt.ylabel('Losses')

plt.show()
            
