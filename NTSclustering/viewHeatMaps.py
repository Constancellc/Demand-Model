import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
import scipy.ndimage.filters as filt

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

plt.figure()
for i in range(3):
    heatmap = np.zeros((6,48))
    with open(stem+'jointPdfW'+str(i+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        s = 0
        for row in reader:
            for t in range(48):
                heatmap[5-s][t] = float(row[t])
            s += 1
    plt.subplot(3,1,i+1)
    plt.imshow(heatmap,aspect=2,vmin=0,vmax=0.8,cmap='magma')
    plt.yticks([-0.5,2.5,5.5],['100%','50%','0%'])
    plt.xticks([7.5,15.5,23.5,31.5,39.5],['','','',''])
    plt.title(str(i+1),color='w',y=0.7)

plt.xticks([7.5,15.5,23.5,31.5,39.5],['04:00','08:00','12:00','16:00','20:00'])
plt.tight_layout()

plt.figure()
for i in range(3):
    heatmap = np.zeros((6,48))
    with open(stem+'jointPdfWE'+str(i+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        s = 0
        for row in reader:
            for t in range(48):
                heatmap[5-s][t] = float(row[t])
            s += 1
    plt.subplot(3,1,i+1)
    plt.imshow(heatmap,aspect=2,vmin=0,vmax=0.8,cmap='magma')
    plt.yticks([-0.5,2.5,5.5],['100%','50%','0%'])
    plt.xticks([7.5,15.5,23.5,31.5,39.5],
               ['04:00','08:00','12:00','16:00','20:00'])

    plt.title(str(i+1),color='w',y=0.7)

#plt.xticks([7.5,15.5,23.5,31.5,39.5],['04:00','08:00','12:00','16:00','20:00'])
plt.tight_layout()
plt.figure()
heatmap = np.zeros((6,48))
with open(stem+'jointPdfW_.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    s = 0
    for row in reader:
        for t in range(48):
            heatmap[5-s][t] = float(row[t])
        s += 1
plt.subplot(2,1,1)
plt.imshow(heatmap,aspect=2,vmin=0,vmax=0.15,cmap='magma')
plt.yticks([-0.5,2.5,5.5],['100%','50%','0%'])
plt.xticks([7.5,15.5,23.5,31.5,39.5],
           ['04:00','08:00','12:00','16:00','20:00'])

heatmap = np.zeros((6,48))
with open(stem+'jointPdfWE_.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    s = 0
    for row in reader:
        for t in range(48):
            heatmap[5-s][t] = float(row[t])
        s += 1
plt.subplot(2,1,2)
plt.imshow(heatmap,aspect=2,vmin=0,vmax=0.15,cmap='magma')
plt.yticks([-0.5,2.5,5.5],['100%','50%','0%'])
plt.xticks([7.5,15.5,23.5,31.5,39.5],
           ['04:00','08:00','12:00','16:00','20:00'])


#plt.xticks([7.5,15.5,23.5,31.5,39.5],['04:00','08:00','12:00','16:00','20:00'])
plt.tight_layout()
plt.show()
