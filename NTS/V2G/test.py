import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag, sparse, solvers

hh30 = []
for t in range(48):
    hh30.append(random.random()*50)

hh = []
for t1 in range(48):
    for t2 in range(30):
        hh.append(hh30[t1])

eV = 60
# kWh
e0 = sum(hh)/60 + eV

print(e0)

def v2g_eval(hh,e0,delta):
    over = 0
    p = (e0+delta)/24
    for t in range(1440):
        if hh[t] > p:
            over += hh[t]/60
    return over

def flatten_v2g(hh,eV):
    e0 = sum(hh)/60 + eV
    delta = 0
    for i in range(10):
        over = v2g_eval(hh,e0,delta)
        delta = over*(1/0.81-1)

    return [over,[(e0+delta)/24]*1440]

def g2v_fill(tot,y):
    en = 0
    for t in range(1440):
        if tot[t] < y:
            en += (y-tot[t])/60
            tot[t] = y

    return [tot,en]

def flatten_g2v(hh,eV):
    total = copy.deepcopy(hh)
    p = min(total)+0.1
    while eV > 0:
        [total,en] = g2v_fill(total,p)
        eV -= en
        p += 0.01

    return total

[over,t1] = flatten_v2g(hh,eV)
t2 = flatten_g2v(hh,eV)

plt.figure()
plt.plot(hh,'k',ls=':')
plt.plot(t1,'r',alpha=0.5)
plt.plot(t2,'b',alpha=0.5)
#plt.plot([0,1440],[e0/24,e0/24],ls=':')
#plt.plot([0,1440],[(e0+delta)/24,(e0+delta)/24])
plt.show()
