import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.filters as filt

plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'

lbls = {'':'UK','texas_':'Texas'}

for loc in ['','texas_']:
    bnft = []
    cost = []
    bnft_u = []
    cost_u = []
    bnft_l = []
    cost_l = []

    conf = 0.75
    for pen in range(10,110,10):
        a = []
        b = []
        with open('../../../Documents/simulation_results/NTS/v2g/'+loc+\
                  'v2g_lf'+str(pen)+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                a.append(100*(float(row[1])-float(row[3]))/float(row[1]))
                try:
                    b.append(100*(float(row[4])-float(row[2]))/float(row[2]))
                except:
                    b.append(0.0)
        '''           
        bnft.append(sum(a)/len(a))
        cost.append(sum(b)/len(b))
        '''
        a = sorted(a)
        b = sorted(b)
        bnft_u.append(a[int(conf*len(a))])
        cost_u.append(b[int(conf*len(b))])
        bnft_l.append(a[int((1-conf)*len(a))])
        cost_l.append(b[int((1-conf)*len(b))])
        bnft.append(a[int(0.5*len(a))])
        cost.append(b[int(0.5*len(b))])
        
    #bnft = filt.gaussian_filter1d(bnft,1)
    #cost = filt.gaussian_filter1d(cost,1)
    plt.subplot(2,1,1)
    plt.plot(range(10,110,10),bnft)
    plt.xlim(20,100)
    plt.ylim(0,35)
    plt.fill_between(range(10,110,10),bnft_l,bnft_u,alpha=0.2)
    plt.ylabel('% Reduction in\nPeak Demand')
    if loc == '':
        plt.grid()
    plt.subplot(2,1,2)
    plt.plot(range(10,110,10),cost,label=lbls[loc])
    plt.xlim(20,100)
    plt.ylim(0,500)
    plt.fill_between(range(10,110,10),cost_l,cost_u,alpha=0.2)
    plt.ylabel('% Increase in\nBattery Throughput')
    if loc == '':
        plt.grid()
    plt.xlabel('% EV Penetration')
    plt.tight_layout()
plt.legend()
plt.show()
        
'''
m1 = []
l1 = []
u1 = []

m2 = []
l2 = []
u2 = []

with open('../../../Documents/simulation_results/NTS/v2g_lf.csv',
          'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        m1.append(float(row[1])/50)
        u1.append(float(row[2])/50)
        l1.append(float(row[3])/50)
        m2.append(float(row[4])/50)
        u2.append(float(row[5])/50)
        l2.append(float(row[6])/50)

plt.figure()
plt.plot(m1)
plt.fill_between(range(1440),l1,u1,alpha=0.2)
plt.plot(m2)
plt.fill_between(range(1440),l2,u2,alpha=0.2)
plt.show()
'''
