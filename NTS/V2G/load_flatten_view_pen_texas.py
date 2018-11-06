import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.filters as filt

plt.figure(figsize=(6,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'

lbls = {'':'UK','texas_':'Texas'}

for loc in ['texas_']:#,'texas_']:
    bnft = []
    cost = []
    bnft_u = []
    cost_u = []
    bnft_l = []
    cost_l = []

    conf = 0.75
    for pen in [2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100]:
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
        
    bnft = filt.gaussian_filter1d([0]+bnft,0.5)
    cost = filt.gaussian_filter1d([0]+cost,0.5)
        
    bnft_u = filt.gaussian_filter1d([0]+bnft_u,0.5)
    cost_u = filt.gaussian_filter1d([0]+cost_u,0.5)
        
    bnft_l = filt.gaussian_filter1d([0]+bnft_l,0.5)
    cost_l = filt.gaussian_filter1d([0]+cost_l,0.5)
    plt.subplot(2,1,1)
    plt.xlim(0,100)
    plt.ylim(0,60)
    plt.fill_between([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
                     bnft_l,bnft_u,color='#CCFFCC')
    plt.plot([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],bnft,
             c='g')
    plt.ylabel('% Reduction in\nPeak Demand')
    plt.grid()
    plt.subplot(2,1,2)
    plt.xlim(0,100)
    plt.ylim(0,130)
    plt.fill_between([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
                     cost_l,cost_u,color='#CCFFCC')
    plt.plot([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
             cost,label=lbls[loc],c='g')
    plt.ylabel('% Increase in\nBattery Throughput')
    plt.grid()
    plt.xlabel('% EV Penetration')
    plt.tight_layout()
plt.savefig('../../../Dropbox/papers/PES-GM-19/img/results2.eps',
            format='eps', dpi=1000)
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
