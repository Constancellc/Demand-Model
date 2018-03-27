import csv
import matplotlib.pyplot as plt
import random
import numpy as np
from clustering import Cluster, ClusteringExercise



data = '../../Documents/clustered_points.csv'
points = []

with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        points.append([float(row[0]),float(row[1])])
        
CE = ClusteringExercise(points)

x = [8,24,40]
x_ticks = ['04:00','12:00','20:00']

css = []
plt.figure(figsize=(4,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'

for k in range(1,8):
    CE.k_means(k)
    css.append(CE.get_sum_of_squares())
    CE.reset_clusters()

for i in range(len(css)):
    css[i] = css[i]/1000000
    
plt.grid()
plt.plot(range(1,8),css)
plt.ylabel('Sum of squares')
plt.xlabel('Number of clusters')
plt.tight_layout()
plt.savefig('../../Dropbox/papers/smart-charging/choosingK.eps', format='eps', dpi=1000)

plt.show()
