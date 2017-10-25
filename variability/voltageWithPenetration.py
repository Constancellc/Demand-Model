# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

L = {0.0:[],0.1:[],0.3:[],0.5:[]}

with open('varying%ev_lowest_voltages.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row == []:
            continue
        L[0.0].append(float(row[0]))
        L[0.1].append(float(row[1]))
        L[0.3].append(float(row[2]))
        L[0.5].append(float(row[3]))

x_ticks = ['0%','10%','30%','50%']
plt.figure(1)
plt.boxplot([L[0.0],L[0.1],L[0.3],L[0.5]],0,'')
plt.xticks(range(1,5),x_ticks)
plt.show()
