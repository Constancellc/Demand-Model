import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

# Texas
data = '../../Documents/NHTS/constance/texas-trips.csv'
labels =  '../../Documents/simulation_results/NTS/clustering/labels2/'


w = {'t':[0]*3,'u':[0]*3,'m':[0]*3}
we = {'t':[0]*3,'u':[0]*3,'m':[0]*3}

# get the labels for both data types
with open(labels+'texasLabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            w['t'][int(row[1])] += 1
        except:
            continue

# get the labels for both data types
with open(labels+'texasLabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            we['t'][int(row[1])] += 1
        except:
            continue# get the labels for both data types
with open(labels+'NTSLabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            w['u'][int(row[1])] += 1
        except:
            continue

# get the labels for both data types
with open(labels+'NTSLabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            we['u'][int(row[1])] += 1
        except:
            continue
        
with open(labels+'MEALabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            w['m'][int(row[1])] += 1
        except:
            continue

# get the labels for both data types
with open(labels+'MEALabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            we['m'][int(row[1])] += 1
        except:
            continue

for k in ['t','u','m']:
    s1 = sum(w[k])
    s2 = sum(we[k])
    for i in range(3):
        w[k][i] = w[k][i]*100/s1
        we[k][i] = we[k][i]*100/s2
        
plt.figure(figsize=(5,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '14'
plt.bar(np.arange(3)-0.16,w['u'],width=0.3,label='UK')
plt.bar(np.arange(3)+0.16,w['t'],width=0.3,label='Texas')
plt.xticks([0,1,2],[1,2,3])
plt.grid(ls=':')
plt.ylabel('Composition (%)')
plt.xlabel('Cluster')
plt.ylim(0,80)
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/texas_uk_comp.eps',
            format='eps', dpi=1000)

plt.figure(figsize=(5,3))
plt.bar(np.arange(3)-0.16,we['u'],width=0.3,label='NTS')
plt.bar(np.arange(3)+0.16,we['t'],width=0.3,label='Texas')
plt.xticks([0,1,2],[1,2,3])
plt.grid(ls=':')
plt.ylabel('Composition (%)')
plt.xlabel('Cluster')
plt.tight_layout()
plt.legend()
plt.ylim(0,80)
plt.savefig('../../Dropbox/thesis/chapter3/img/texas_uk_comp_we.eps',
            format='eps', dpi=1000)
        
plt.figure(figsize=(5,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '14'
plt.bar(np.arange(3)-0.16,w['u'],width=0.3,label='UK')
plt.bar(np.arange(3)+0.16,w['m'],width=0.3,label='MEA')
plt.xticks([0,1,2],[1,2,3])
plt.grid(ls=':')
plt.ylabel('Composition (%)')
plt.xlabel('Cluster')
plt.ylim(0,70)
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/meaVnts.eps',
            format='eps', dpi=1000)

plt.figure(figsize=(5,3))
plt.bar(np.arange(3)-0.16,we['u'],width=0.3,label='UK')
plt.bar(np.arange(3)+0.16,we['m'],width=0.3,label='MEA')
plt.xticks([0,1,2],[1,2,3])
plt.grid(ls=':')
plt.ylabel('Composition (%)')
plt.xlabel('Cluster')
plt.tight_layout()
plt.legend()
plt.ylim(0,70)
plt.savefig('../../Dropbox/thesis/chapter3/img/meaVnts_we.eps',
            format='eps', dpi=1000)
plt.show()
