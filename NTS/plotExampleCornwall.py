# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import scipy.ndimage
import copy

resultsStem = '../../Documents/simulation_results/NTS/cornwall2/'


def fill(p,en):
    p_ = copy.deepcopy(p)
    p_2 = [0.0]*len(p)

    delta = 1

    while en > 0:
        t_ = np.argmin(p_)
        p_[t_] += delta
        p_2[t_] += delta
        en -= delta

    return [p_,p_2]
plt.figure(figsize=(10,5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = 14


n = 1
t = []
base2 = []
base5 = []

for m in ['7']:
    with open(resultsStem+m+'-solar.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            t.append(float(row[0]))
            base2.append(float(row[1]))
            base5.append(float(row[5]))

base5 = base5[24*6:48*6]
base2 = base2[24*6:48*6]
t = t[24*6:48*6]
solar = []
for i in range(len(base2)):
    solar.append(base5[i]-base2[i])

[p_,p_2] = fill(base2,10000)

plt.subplot(1,2,1)
plt.plot(t,base2,c='k',ls=':',label='Base',lw=2)
plt.plot(t,p_,c='b',label='After EVs',lw=2)
plt.xlim(24*60,48*60)
plt.ylim(-50,500)
plt.ylabel('Power Demand (MW)')
plt.xticks([26*60,30*60,34*60,38*60,42*60,46*60],['02:00','06:00','10:00',
                                                  '14:00','18:00','22:00'])
plt.legend()
plt.grid()

new = []
for i in range(144):
    new.append(base5[i]+p_2[i])
    
plt.subplot(1,2,2)
plt.plot(t,base5,c='k',ls=':',label='Base',lw=2)
plt.plot(t,new,c='b',label='After EVs',lw=2)
plt.xlim(24*60,48*60)
plt.ylim(-50,500)
plt.xticks([26*60,30*60,34*60,38*60,42*60,46*60],['02:00','06:00','10:00',
                                                  '14:00','18:00','22:00'])
plt.ylabel('Power Demand (MW)')
plt.grid()
plt.tight_layout()
plt.show()
