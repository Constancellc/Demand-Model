import matplotlib.pyplot as plt
import numpy as np
import random
from scenarios import generate
from cvxopt import matrix, spdiag, sparse, solvers, spmatrix

scen = generate(5,10)

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
        
x = optimise(scen,100000)

plt.figure()
plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.subplot(1,2,1)
_p1,_p2,_p3,_p4,_p5 = get_range(scen,offset=1)
plt.fill_between(range(48),_p1,_p5,color='#bfddff')
plt.fill_between(range(48),_p2,_p4,color='#80bbff')
plt.yticks([10000,20000,30000,40000,50000],['10','20','30','40','50'])
plt.xticks([7.5,23.5,39.5],['04:00','12:00','20:00'])
plt.plot(_p3,c='#0077ff')
plt.grid(ls=':')
plt.ylabel('Power (GW)')
plt.title('Before')
plt.xlim(0,47)
plt.ylim(20000,50000)
plt.subplot(1,2,2)
_p1,_p2,_p3,_p4,_p5 = get_range(scen,offset=1,new=x)
plt.fill_between(range(48),_p1,_p5,color='#bfddff')
plt.fill_between(range(48),_p2,_p4,color='#80bbff')
plt.yticks([20000,30000,40000,50000],['20','30','40','50'])
plt.xticks([7.5,23.5,39.5],['04:00','12:00','20:00'])
plt.plot(_p3,c='#0077ff')
plt.grid(ls=':')
plt.title('After')
plt.xlim(0,47)
plt.ylim(20000,50000)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/PSCC-20/img/optimise.eps', format='eps', dpi=300,
            bbox_inches='tight', pad_inches=0)



plt.figure()
plt.figure(figsize=(5,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.plot(scen[0][1:],c='k',ls=':',label='Existing Demand')
x = optimise([[1.0]+scen[15][1:]],10000)
p = []
for t in range(48):
    p.append(x[t]+scen[15][t+1])
plt.plot(p,c='b',label='With Smart Charging')
plt.grid(ls=':')
plt.legend()
plt.xlim(0,47)
plt.ylim(20000,50000)
plt.yticks([20000,30000,40000,50000],['20','30','40','50'])
plt.xticks([7.5,23.5,39.5],['04:00','12:00','20:00'])
plt.ylabel('Power (GW)')
plt.tight_layout()
plt.show()
#def optimise(scenarios,en):
    
    
    
