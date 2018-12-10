import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

outstem = '../../Documents/simulation_results/NTS/clustering/power/E06000013/'

u_m = []
u_l = []
u_u = []
d_m = []
d_l = []
d_u = []

ov_l = []
ov_u = []

with open(outstem+'0.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        u_m.append(float(row[1]))
        u_l.append(float(row[2]))
        u_u.append(float(row[3]))
        d_m.append(float(row[4]))
        d_l.append(float(row[5]))
        d_u.append(float(row[6]))
        if u_u[-1] > d_u[-1]:
            if u_l[-1] < d_u[-1]:
                ov_u.append(d_u[-1])
                ov_l.append(u_l[-1])
            else:
                ov_u.append(d_u[-1])
                ov_l.append(d_u[-1])
        else:
            if d_l[-1] < u_u[-1]:
                ov_u.append(u_u[-1])
                ov_l.append(d_l[-1])
            else:
                ov_u.append(u_u[-1])
                ov_l.append(u_u[-1])

plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'
plt.subplot(2,1,2)
plt.plot(np.linspace(0,24,num=1440),d_m,c='g',label='(a)')
plt.fill_between(np.linspace(0,24,num=1440),d_l,d_u,color='#CCFFCC')
plt.plot(np.linspace(0,24,num=1440),u_m,c='b',label='(b)')
plt.fill_between(np.linspace(0,24,num=1440),u_l,u_u,color='#CCCCFF')
plt.fill_between(np.linspace(0,24,num=1440),ov_l,ov_u,color='#99CCCC')
plt.xlim(0,24)
plt.ylim(0,55)
plt.legend(ncol=2,loc=2)
plt.title('Varied set of vehicles',y=0.7)
plt.grid()
plt.ylabel('Power (kW)')
plt.xticks([2,6,10,14,18,22],
           ['02:00','06:00','10:00','14:00','18:00','22:00'])

u_m = []
u_l = []
u_u = []
d_m = []

with open(outstem+'single.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        u_m.append(float(row[1]))
        u_l.append(float(row[2]))
        u_u.append(float(row[3]))
        d_m.append(float(row[4]))

plt.subplot(2,1,1)
plt.fill_between(np.linspace(0,24,num=1440),u_l,u_u,color='#CCCCFF')
plt.plot(np.linspace(0,24,num=1440),d_m,c='g')
plt.plot(np.linspace(0,24,num=1440),u_m,c='b')
plt.xlim(0,24)
plt.ylim(0,55)
plt.grid()
plt.title('Single set of vehicles',y=0.75)
plt.ylabel('Power (kW)')
plt.xticks([2,6,10,14,18,22],
           ['02:00','06:00','10:00','14:00','18:00','22:00'])
plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/mc_power.eps',
            format='eps', dpi=1000)
plt.show()
