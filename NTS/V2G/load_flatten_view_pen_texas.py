import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.filters as filt
import matplotlib.patches as pat

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

    conf = 0.95
    for pen in [2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100]:
        a = []
        b = []
        with open('../../../Documents/simulation_results/NTS/v2g/'+loc+\
                  'v2g_lf'+str(pen)+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                a.append(100*(float(row[1])-float(row[4]))/(1167+float(row[1])))
                try:
                    b.append(100*(float(row[5])-float(row[2]))/float(row[2]))

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
    plt.ylim(0,300)
    plt.fill_between([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
                     cost_l,cost_u,color='#CCFFCC')
    plt.plot([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
             cost,label=lbls[loc],c='g')
    plt.ylabel('% Increase in\nBattery Throughput')
    plt.grid()
    plt.xlabel('% EV Penetration')
    plt.tight_layout()
plt.savefig('../../../Dropbox/papers/V2G/img/texas_results.eps',
            format='eps', dpi=1000)


fig,ax = plt.subplots(1,figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'


d = []
d_l = []
d_u = []
c = []
c_l = []
c_u = []

for pen in [2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100]:
    a = []
    b = []
    with open('../../../Documents/simulation_results/NTS/v2g/'+loc+\
              'v2g_lf'+str(pen)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            a.append(100*(-float(row[3])+float(row[6]))/float(row[3]))

            lb4 = float(row[3])+0.5*float(row[2])*0.111
            laft = float(row[6])+0.111*(float(row[5])-float(row[2]))

            b.append(100*(laft-lb4)/laft)
    a = sorted(a)
    b = sorted(b)

    d.append(a[int(0.5*len(a))])
    d_u.append(a[int(conf*len(a))])
    d_l.append(a[int((1-conf)*len(a))])
    c.append(b[int(0.5*len(b))])
    c_u.append(b[int(conf*len(b))])
    c_l.append(b[int((1-conf)*len(b))])


        
d = filt.gaussian_filter1d([0]+d,0.5)
c = filt.gaussian_filter1d([0]+c,0.5)        
d_l = filt.gaussian_filter1d([0]+d_l,0.5)
c_l = filt.gaussian_filter1d([0]+c_l,0.5)        
d_u = filt.gaussian_filter1d([0]+d_u,0.5)
c_u = filt.gaussian_filter1d([0]+c_u,0.5)
        
plt.xlim(0,100)
plt.fill_between([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
                 d_l,d_u,facecolor='#CCFFCC',hatch='//',edgecolor='grey',
                 linewidth=0.0)
plt.plot([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],d,c='g',ls='--')
plt.grid()
plt.xlim(0,100)
plt.fill_between([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
                 c_l,c_u,color='#CCFFCC')
plt.plot([0,2,4,6,8,10,12,14,16,18,20,30,40,50,60,70,80,90,100],
         c,label=lbls[loc],c='g')
plt.ylabel('% Increase in Losses')
plt.ylim(-10,60)
plt.xlabel('% EV Penetration')



def draw_box(x_l,y_l,x_u,y_u,c,ls):
    plt.plot([x_l,x_l],[y_l,y_u],c=c,ls=ls)
    plt.plot([x_u,x_u],[y_l,y_u],c=c,ls=ls)
    plt.plot([x_l,x_u],[y_l,y_l],c=c,ls=ls)
    plt.plot([x_l,x_u],[y_u,y_u],c=c,ls=ls)
    

rect = pat.Rectangle((57,35),38,20,facecolor='w',edgecolor='gray',zorder=2)
ax.add_patch(rect)
rect2 = pat.Rectangle((59,47),5,6,facecolor='#CCFFCC',edgecolor='none',zorder=2)
ax.add_patch(rect2)
rect3 = pat.Rectangle((59,37),5,6,facecolor='#CCFFCC',edgecolor='gray',
                      hatch='//',zorder=2,linewidth=0.0)
ax.add_patch(rect3)
plt.plot([59,64],[50,50],c='g')
plt.plot([59,64],[40,40],c='g',ls='--')
plt.annotate('Total Losses',(66,48))
plt.annotate('Distribution Losses',(66,38))

plt.tight_layout()
plt.savefig('../../../Dropbox/papers/V2G/img/texas_results2.eps',
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
