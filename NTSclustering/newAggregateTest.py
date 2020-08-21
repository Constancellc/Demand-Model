import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

pred_charges = '../../Documents/My_Electric_Avenue_Technical_Data/pred_charges.csv'
mea_d_type = '../../Documents/My_Electric_Avenue_Technical_Data/d_type.csv'
charge_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'
trip_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

c_rate = 3.5 # kW
cap = 24 # kWh
n_mc = 1500

p = {}
all_vdays = []
with open(pred_charges,'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        vday = row[0]+'_'+row[1]
        if vday not in p:
            p[vday] = []
            all_vdays.append(vday)
        start = int(row[2])
        length = int(((1-0.69*float(row[3]))*cap)*60/(c_rate*0.9))
        p[vday].append([start,length])

mc_runs = {}
for t in range(48):
    mc_runs[t] = []
for mc in range(n_mc):
    p_ = [0.0]*48
    for v in range(50):
        vd = all_vdays[int(random.random()*len(all_vdays))]
        for c in p[vd]:
            for t in range(c[1]):
                try:
                    p_[int((c[0]+t)/30)] += c_rate/30
                except:
                    p_[int((c[0]+t)/30)-48] += c_rate/30
    for t in range(48):
        mc_runs[t].append(p_[t])

av = []
l = []
u = []

for t in range(48):
    x = sorted(mc_runs[t])
    av.append(sum(x)/len(x))
    l.append(x[int(0.16*len(x))])
    u.append(x[int(0.84*len(x))])


p = {}
all_vdays = []
with open(charge_data,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vday = row[0]+'_'+row[1]
        if vday not in p:
            p[vday] = []
            all_vdays.append(vday)
        start = int(row[2])
        length = int(((1-float(row[4]))*cap)*60/(c_rate*0.9))
        p[vday].append([start,length])

mc_runs = {}
for t in range(48):
    mc_runs[t] = []
for mc in range(n_mc):
    p_ = [0.0]*48
    for v in range(50):
        vd = all_vdays[int(random.random()*len(all_vdays))]
        for c in p[vd]:
            for t in range(c[1]):
                try:
                    p_[int((c[0]+t)/30)] += c_rate/30
                except:
                    p_[int((c[0]+t)/30)-48] += c_rate/30
    for t in range(48):
        mc_runs[t].append(p_[t])

av1 = []
l1 = []
u1 = []

for t in range(48):
    x = sorted(mc_runs[t])
    av1.append(sum(x)/len(x))
    l1.append(x[int(0.16*len(x))])
    u1.append(x[int(0.84*len(x))])





p = {}
all_vdays = []
mc_runs = {}
with open(trip_data,'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vday = row[0]+'_'+row[1]
        if vday not in p:
            p[vday] = [0,0]
            all_vdays.append(vday)
        end = int(row[2])
        kWh = float(row[-2])/1000
        if end > p[vday][0]:
            p[vday][0] = end
        p[vday][1] += kWh


for t in range(48):
    mc_runs[t] = []
for mc in range(n_mc):
    p_ = [0.0]*48
    for v in range(50):
        vd = all_vdays[int(random.random()*len(all_vdays))]
        start = p[vd][0]
        if p[vd][1] > 24:
            p[vd][1] = 24
            
        if start > 1440:
            start -= 1440
        length = int(60*p[vd][1]/(c_rate*0.9))
        for t in range(length):
            try:
                p_[int((start+t)/30)] += c_rate/30
            except:
                p_[int((start+t)/30)-48] += c_rate/30
    for t in range(48):
        mc_runs[t].append(p_[t])

av2 = []
l2 = []
u2 = []

for t in range(48):
    x = sorted(mc_runs[t])
    av2.append(sum(x)/len(x))
    l2.append(x[int(0.16*len(x))])
    u2.append(x[int(0.84*len(x))])


sf1 = sum(av1)/sum(av)
sf2 = sum(av1)/sum(av2)

for t in range(48):
    av[t] = av[t]*sf1
    av2[t] = av2[t]*sf2
    l[t] = l[t]*sf1
    l2[t] = l2[t]*sf2
    u[t] = u[t]*sf1
    u2[t] = u2[t]*sf2

plt.figure(figsize=(4.5,3.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
plt.subplot(2,1,1)
plt.title('Proposed Method',y=0.75)
plt.plot(av,c='b',label='Predicted')
plt.plot(av1,c='g',ls=':',label='Observed')
plt.legend(loc=2)
plt.fill_between(range(48),l1,u1,color='#CCFFCC')
plt.fill_between(range(48),l,u,color='#CCCCFF')
ov_u = []
ov_l = []
for t in range(48):
    ov_u.append(min([u1[t],u[t]]))
    ov_l.append(max([l1[t],l[t]]))
plt.fill_between(range(48),ov_l,ov_u,color='#CCEEEE')
plt.subplot(2,1,2)
plt.title('After Journey',y=0.75)
plt.plot(av2,c='b')
plt.plot(av1,c='g',ls=':',label='Observed')
plt.fill_between(range(48),l1,u1,color='#CCFFCC')
plt.fill_between(range(48),l2,u2,color='#CCCCFF')
ov_u = []
ov_l = []
for t in range(48):
    if u1[t] > u2[t]:
        if l1[t] > u2[t]:
            # no overlap
            ov_u.append(u2[t])
            ov_l.append(u2[t])
        else:
            ov_u.append(u2[t])
            ov_l.append(l1[t])
    else:
        if l2[t] > u1[t]:
            # no overlap
            ov_u.append(u1[t])
            ov_l.append(u1[t])
        else:
            ov_u.append(u1[t])
            ov_l.append(l2[t])
plt.fill_between(range(48),ov_l,ov_u,color='#CCEEEE')

for i in range(1,3):
    plt.subplot(2,1,i)
    plt.grid(ls=':')
    plt.ylabel('Power (kW)')
    plt.xlim(0,47)
    plt.ylim(0,120)
    plt.xticks(np.arange(4,52,8)-0.5,['02:00','06:00','10:00','14:00','18:00',
                                      '22:00'])
plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/aggregate.eps',
            format='eps', dpi=300, bbox_inches='tight', pad_inches=0)


plt.figure(figsize=(4.5,3.5))
plt.subplot(2,1,1)
plt.plot(av1,ls=':',c='k',label='True')
plt.plot(av,c='b',label='Proposed')
plt.plot(av2,c='r',ls='--',label='After journey')
plt.title('Average',y=0.75)
plt.ylim(0,120)
v1 = []
v2 = []
v = []

for t in range(48):
    v.append(np.power((u[t]-l[t])/2,2))
    v1.append(np.power((u1[t]-l1[t])/2,2))
    v2.append(np.power((u2[t]-l2[t])/2,2))
plt.subplot(2,1,2)
plt.plot(v1,ls=':',c='k',label='True')
plt.plot(v,c='b',label='Proposed')
plt.plot(v2,c='r',ls='--',label='After journey')
plt.title('Variance',y=0.75)
plt.ylim(0,800)
plt.legend()

for i in range(1,3):
    plt.subplot(2,1,i)
    plt.grid(ls=':')
    plt.xlim(0,47)
    plt.xticks(np.arange(4,52,8)-0.5,['02:00','06:00','10:00','14:00','18:00',
                                      '22:00'])
plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/aggregate2.eps',
            format='eps', dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()
