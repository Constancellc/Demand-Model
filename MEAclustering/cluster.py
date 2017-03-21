import csv
from PCA import PCA
import sklearn.cluster as clst
import numpy as np
import matplotlib.pyplot as plt

Z, X, names = PCA('chargeRLPs.csv',0.99)
Z = Z.T

k = 4 # number of clusters

centroid, label, inertia = clst.k_means(Z,k)

clusters = {}
ids = {}

for i in range(0,k):
    clusters[i] = []
    ids[i] = []

for i in range(0,len(Z)):
    clusters[label[i]].append(Z[i])
    ids[label[i]].append(names[i])

plt.figure(1)
for i in range(0,k):
    x = []
    y = []
    for j in range(0,len(clusters[i])):
        x.append(clusters[i][j][0])
        y.append(clusters[i][j][1])
    plt.scatter(x,y)

means = {}
maxs = {}
mins = {}
for i in range(0,k):
    means[i] = [0.0]*(24*60)
    maxs[i] = [0.0]*(24*60)
    mins[i] = [1.0]*(24*60)

t = np.linspace(0,24,num=24*60)

plt.figure(2)
for i in range(0,k):
    plt.subplot(k,1,i+1)
    with open('chargeRLPs.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] in ids[i]:
                plt.plot(t,row[1:],label=row[0])
                for j in range(0,24*60):

                    means[i][j] += float(row[j+1])/len(ids[i])
                    if float(row[j+1]) > maxs[i][j]:
                        maxs[i][j] = float(row[j+1])
                    if float(row[j+1]) < mins[i][j]:
                        mins[i][j] = float(row[j+1])


plt.figure(3)
for i in range(0,k):
    plt.subplot(k,1,i+1)
    plt.plot(t,means[i])
    plt.fill_between(t,maxs[i],mins[i],alpha=0.5)


    
plt.show()
