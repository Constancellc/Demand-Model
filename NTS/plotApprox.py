# packages
import matplotlib.pyplot as plt
import numpy as np
import csv


day = '3'
optPPH = 1
clstPPH = 15
nHours = 36
res = '../../Documents/simulation_results/NTS/national/wed/7.csv'

b = []
o = []
p = []
with open(res,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        b.append(float(row[1]))
        o.append(float(row[-2]))
        p.append(float(row[-1]))

t = np.linspace(0,24,num=1440)

fig=plt.figure(figsize=(5,3))
plt.rcParams["font.family"] = 'serif'
plt.plot(t,b[1440:2880],c='k',ls=':',label='Base')
plt.plot(t,o[1440:2880],ls='--',label='Optimal')
plt.plot(t,p[1440:2880],label='Psuedo')
plt.ylim(0,40)
plt.ylabel('Power (GW)')
plt.xlim(0,24)
plt.xticks([4,8,12,16,20],['04:00','08:00','12:00','16:00','20:00'])
plt.grid(ls=':')
plt.legend()
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter4/img/approx_accuracy.eps',
            format='eps',dpi=1000,bbox_inches='tight', pad_inches=0)
plt.show()
