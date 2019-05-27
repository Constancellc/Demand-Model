import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from scipy.stats.stats import pearsonr   
outstem = '../../Documents/simulation_results/NTS/clustering/power/'

def get_error(a,true):
    diff = 0
    total = 0
    for t in range(len(a)):
        diff += np.power(a[t]-true[t],1)
        #diff += abs(a[t]-true[t])
        total += true[t]
    print(diff)
    print(100*np.sqrt(diff/total))

def stretch(a,l):
    b = [0.0]*len(a)
    for i in range(len(a)):
        for j in range(l):
            if i+j < len(b):
                b[i+j] = a[i]
            else:
                b[i+j-len(a)] = a[i]
    s = sum(b)
    for i in range(len(b)):
        b[i] = b[i]/s
    return b

d = []
dW = []
t = []
tW = []
u = []
uW = []

with open(outstem+'error.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        t.append(float(row[0]))
        d.append(float(row[1]))
        u.append(float(row[2]))
        tW.append(float(row[3]))
        dW.append(float(row[4]))
        uW.append(float(row[5]))


plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'
plt.subplot(2,1,1)
plt.plot(d,c='b',label='After final journey')
plt.plot(u,c='r',ls='--',label='Proposed model')
plt.plot(t,ls=':',c='k',label='Ground truth')
print('')
print(pearsonr(d,t))
print(pearsonr(u,t))
print('')
u = stretch(u,2)
t = stretch(t,2)
d = stretch(d,2)

print('')
print(pearsonr(d,t))
print(pearsonr(u,t))
print('')
plt.xlim(0,47)
plt.xticks([7,15,23,31,39],['04:00','08:00','12:00','16:00','20:00'])
plt.grid()
plt.ylabel('Likelihood of\nstarting charge')
plt.title('Weekday',y=0.7)
plt.legend()


plt.subplot(2,1,2)
plt.plot(dW,c='b',label='(a)')
plt.plot(uW,c='r',ls='--',label='(b)')
plt.plot(tW,ls=':',c='k',label='True')
plt.xlim(0,47)
plt.xticks([7,15,23,31,39],['04:00','08:00','12:00','16:00','20:00'])
plt.grid()
plt.ylabel('Likelihood of\nstarting charge')
plt.title('Weekend',y=0.7)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/error.eps',
            format='eps', dpi=1000)


d2 = [0]*48
t2 = [0]*48
u2 = [0]*48
for ti in range(48):
    for ti2 in range(8):
        try:
            d2[ti+ti2] += d[ti]
            t2[ti+ti2] += t[ti]
            u2[ti+ti2] += u[ti]
        except:
            d2[ti+ti2-48] += d[ti]
            t2[ti+ti2-48] += t[ti]
            u2[ti+ti2-48] += u[ti]


get_error(d2,t2)
get_error(u2,t2)
plt.show()
