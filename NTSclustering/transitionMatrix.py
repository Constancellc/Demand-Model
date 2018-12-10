import csv
import matplotlib.pyplot as plt
from matplotlib import colors
import random
import numpy as np
import copy
import scipy.ndimage.filters as filt

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

labels = {}
with open(stem+'NTSlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        vehicle = row[0][:-1]
        if vehicle not in labels:
            labels[vehicle] = {}

        day = int(row[0][-1])-1
        
        if day > 4:
            continue
        
        labels[vehicle][day] = int(row[1])

M = np.zeros((4,4))

for vehicle in labels:
    for day in range(4):
        if day not in labels[vehicle]:
            k = 3
        else:
            k = labels[vehicle][day]

        if day+1 not in labels[vehicle]:
            k2 = 3
        else:
            k2 = labels[vehicle][day+1]

        M[k][k2] += 1

for k in range(4):
    S = sum(M[k])
    for k2 in range(4):
        M[k][k2] = M[k][k2]*100/S

print(M)

plt.figure()
plt.yticks([0,1,2,3],['1','2','3','N/A'])
plt.xticks([0,1,2,3],['1','2','3','N/A'])
plt.ylabel('Current cluster')
plt.xlabel('Next day cluster')
plt.imshow(M)
plt.colorbar()
plt.show()
