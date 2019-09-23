import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.cluster import KMeans

meta = []
p = []
with open('../../Documents/solar_data_scenarios/net_profile_cleaned_60000.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        meta.append(row[:3])
        _p = []
        for i in range(3,len(row)):
            _p.append(float(row[i]))
        nm = sum(_p)
        for i in range(len(_p)):
            _p[i] = _p[i]/nm
        p.append(_p)


for i in range(2,11):
    plt.figure(1)
    plt.subplot(3,3,i-1)
    plt.title(i)
    kmeans = KMeans(n_clusters=i, random_state=0).fit(p)
    cent = kmeans.cluster_centers_
    labels = kmeans.labels_
    for j in range(i):
        plt.plot(cent[j])
    plt.figure(2)
    plt.subplot(3,3,i-1)
    plt.title(i)
    r = [0]*i
    t = [0]*i
    k = [0]*i
    for j in range(len(labels)):
        k[labels[j]] += 1
        r[labels[j]] += float(meta[j][1])
        t[labels[j]] += float(meta[j][2])
    for j in range(i):
        r[j] = r[j]/k[j]
        t[j] = t[j]/k[j]
        plt.scatter([r[j]],[t[j]],s=k[j])
    plt.xlim(1,5)
    plt.ylim(5,15)
plt.show()

        
