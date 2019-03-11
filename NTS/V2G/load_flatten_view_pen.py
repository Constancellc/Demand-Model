import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.filters as filt

plt.figure(figsize=(6,6))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'

lbls = {'':'UK','texas_':'Texas'}

for loc in ['']:#,'texas_']:
    pk = []
    tp = []
    ls = []
    pk_u = []
    tp_u = []
    ls_u = []
    pk_l = []
    tp_l = []
    ls_l = []

    conf = 0.8
    for pen in [2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100]:
        a = []
        b = []
        c = []
        with open('../../../Documents/simulation_results/NTS/v2g/'+loc+\
                  'v2g_lf'+str(pen)+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                a.append(100*(float(row[1])-float(row[4]))/float(row[1]))
                try:
                    b.append(100*(float(row[5])-float(row[2]))/float(row[2]))
                except:
                    b.append(0.0)
                c.append(100*(float(row[6])-float(row[3]))/float(row[3]))
        '''           
        bnft.append(sum(a)/len(a))
        cost.append(sum(b)/len(b))
        '''
        a = sorted(a)
        b = sorted(b)
        c = sorted(c)
        pk.append(a[int(0.5*len(a))])
        tp.append(b[int(0.5*len(b))])
        ls.append(c[int(0.5*len(c))])
        pk_u.append(a[int(conf*len(a))])
        tp_u.append(b[int(conf*len(b))])
        ls_u.append(c[int(conf*len(c))])
        pk_l.append(a[int((1-conf)*len(a))])
        tp_l.append(b[int((1-conf)*len(b))])
        ls_l.append(c[int((1-conf)*len(c))])
        
    #bnft = filt.gaussian_filter1d(bnft,1)
    #cost = filt.gaussian_filter1d(cost,1)
    plt.subplot(3,1,1)
    plt.xlim(0,100)
    plt.ylim(0,40)
    plt.fill_between([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
                     [0]+pk_l,[0]+pk_u,color='#CCCCFF')
    plt.plot([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],[0]+pk,
             c='b')
    plt.ylabel('% Reduction in\nPeak Demand')
    if loc == '':
        plt.grid()
        
    plt.subplot(3,1,2)
    plt.xlim(0,100)
    plt.ylim(-4,6)
    plt.fill_between([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
                     [0]+ls_l,[0]+ls_u,color='#CCCCFF')
    plt.plot([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
             [0]+ls,label=lbls[loc],c='b')
    plt.ylabel('% Increase in\nEnergy Losses')
    if loc == '':
        plt.grid()
    
    plt.subplot(3,1,3)
    plt.xlim(0,100)
    plt.ylim(0,250)
    plt.fill_between([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
                     [0]+tp_l,[0]+tp_u,color='#CCCCFF')
    plt.plot([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
             [0]+tp,label=lbls[loc],c='b')
    plt.ylabel('% Increase in\nBattery Throughput')
    if loc == '':
        plt.grid()
    plt.xlabel('% EV Penetration')
    plt.tight_layout()
#plt.savefig('../../../Dropbox/papers/PES-GM-19/img/results.eps',
#            format='eps', dpi=1000)
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
