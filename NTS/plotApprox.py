# packages
import matplotlib.pyplot as plt
import numpy as np
import csv


day = '3'
optPPH = 1
clstPPH = 15
nHours = 36
res = '../../Documents/simulation_results/NTS/national/wed/'

m = ['4','7','10','1']
ttls = ['Spring','Summer','Autumn','Winter']
plt.figure(figsize=(7.2,4.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
for f in range(4):
    b = []
    o = []
    p = []
    with open(res+m[f]+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            b.append(float(row[1]))
            o.append(float(row[-2]))
            p.append(float(row[-1]))
    plt.subplot(2,2,f+1)
    plt.plot(b[1440:2880],c='k',ls=':',label='No Charging')
    plt.plot(o[1440:2880],label='Optimal',c='r',ls='--')
    plt.plot(p[1440:2880],label='Approximate',c='g')
    plt.xticks(np.linspace(2*60,22*60,num=5),['02:00','07:00','12:00','17:00','22:00'])
    plt.xlim(0,1439)
    plt.ylim(20,55)
    plt.grid(ls=':')
    plt.title(ttls[f])

    if f in [0,2]:
        plt.ylabel('Power (GW)')
    elif f == 1:
        plt.legend(ncol=2)

plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter5/img/approx.eps', format='eps',
            dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()

    


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
