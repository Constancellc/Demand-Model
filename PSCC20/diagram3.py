import datetime
import csv
import random
import matplotlib.pyplot as plt
import numpy as np
from scenarios import generate, generate_control, get_single
from cvxopt import matrix, spdiag, sparse, solvers, spmatrix


day = datetime.datetime(2016,7,12)

solar = 12000
en = 200000
r,t,actual = get_single(day,solar=solar)

scen = generate(r,t,solar=solar,skip=day)
scen2 = generate_control(solar=solar,skip=day)

def optimise(scen,en):
    Q = spdiag([1.0]*48)
    
    p = [0.0]*48
    for i in range(len(scen)):
        for t in range(48):
            p[t] += scen[i][0]*scen[i][t+1]
    p = matrix(p)

    A = matrix(1.0/2,(1,48))
    b = matrix([float(en)])

    G = spdiag([-1.0]*48)
    h = matrix([0.0]*48)

    sol=solvers.qp(Q,p,G,h,A,b)
    x = sol['x']

    return x

def get_range(profiles,offset=0,new=[0]*48):
    _p1 = []
    _p2 = []
    _p3 = []
    _p4 = []
    _p5 = []
    for t in range(48):
        y = []
        for i in range(len(profiles)):
            y.append(profiles[i][t+offset])
        y = sorted(y)
        _p1.append(y[int(len(y)*0.1)]+new[t])
        _p2.append(y[int(len(y)*0.3)]+new[t])
        _p3.append(y[int(len(y)*0.5)]+new[t])
        _p4.append(y[int(len(y)*0.7)]+new[t])
        _p5.append(y[int(len(y)*0.9)]+new[t])

    return _p1,_p2,_p3,_p4,_p5
        
x = optimise(scen,en)
x2 = optimise(scen2,en)

plt.figure()
plt.figure(figsize=(5,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.plot(actual,c='k',ls=':',label='Existing Demand')
p = []
for t in range(48):
    p.append(actual[t]+x[t])
plt.plot(p,label='Weighted Scenarios',c='b')
print(np.linalg.norm(p))
p = []
for t in range(48):
    p.append(actual[t]+x2[t])
plt.plot(p,label='Un-weighted Scenarios',c='r',ls='--')
print(np.linalg.norm(p))
plt.legend()
plt.xlim(0,47)
plt.yticks([20000,30000,40000,50000],['20','30','40','50'])
plt.xticks([7.5,23.5,39.5],['04:00','12:00','20:00'])
plt.ylim(20000,40000)
plt.grid(ls=':')
plt.ylabel('Power (GW)')
plt.title(str(day)[:10])
plt.tight_layout()
plt.savefig('../../Dropbox/papers/PSCC-20/img/single_day.eps', format='eps', dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()
#def optimise(scenarios,en):
    
    
    
