# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)

totals = {0:[],1:[]}
diffs = [0]*100

with open('results/lf_lm_losses.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row == []:
            continue
        diffs[int(1000*(float(row[0])-float(row[1]))/float(row[0]))] += 1
        for i in range(2):
            totals[i].append(100*float(row[i])/float(row[4]))
        #diffs[0].append(100*float(row[4])/float(row[4]))
        #diffs[1].append(100*float(row[5])/float(row[4]))

plt.figure(1)
plt.subplot(2,1,1)
plt.boxplot([totals[0],totals[1]],0,'',whis=[0.05, 99.5])
plt.xticks([1,2],['Load Flattening','Loss Minimising'])
plt.ylabel('Energy Lost (%)')
plt.grid()
plt.subplot(2,1,2)
plt.ylabel('Frequency')
plt.xlabel('% Saved by loss minimization over load flattening')
plt.bar(np.arange(0,10,0.1),diffs,0.1)
plt.grid()
plt.show()
