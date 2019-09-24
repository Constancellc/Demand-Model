import datetime
import csv
import random
import matplotlib.pyplot as plt
import numpy as np
from scenarios import generate, generate_control, get_single
from cvxopt import matrix, spdiag, sparse, solvers, spmatrix


solvers.options['show_progress'] = False
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

day0 = datetime.datetime(2013,1,1)
slr = [12,16,20,24,28,32,36,40,44,48,52,56,60]
'''
n = 0
for s in slr:
    solar = s*1000
    f0 = 0
    f1 = 0
    for dd in range(2191):
        day = day0+datetime.timedelta(dd)
        if day.isoweekday()>5:
            continue
        en = 200000
        try:
            r,t,actual = get_single(day,solar=solar)
        except:
            #print(day)
            continue
        n += 1

        scen = generate(r,t,solar=solar,skip=day)
        scen2 = generate_control(solar=solar,skip=day)

        x = optimise(scen,en)
        x2 = optimise(scen2,en)

        p = []
        for t in range(48):
            p.append((actual[t]+x[t])/1000)
        f0 += np.linalg.norm(p)
        p = []
        for t in range(48):
            p.append((actual[t]+x2[t])/1000)
        f1 += np.linalg.norm(p)

    print(f0)
    print(f1)
    print('')'''


_f0 = [441907,437595,433627,429358,425112,420890,416695,412528,408401,404301,
       400248,396227,392250]
_f1 = [442074,437798,433874,429656,425470,421316,417199,413120,409091,405099,
       401165,397272,393434]
diff = []
for i in range(len(_f0)):
    _f0[i] = _f0[i]/1539
    _f1[i] = _f1[i]/1539
    diff.append(_f1[i]-_f0[i])

plt.figure()
plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.ylabel('$\Delta  f(x)$')
plt.xlabel('Installed Solar (GW)')
#plt.plot(slr,_f0,label='Weighted',c='b')
#plt.plot(slr,_f1,label='Un-weighted',c='r',ls='--')
plt.plot(slr,diff)
plt.legend()
plt.grid(ls='--')
plt.tight_layout()
plt.savefig('../../Dropbox/papers/PSCC-20/img/installed_solar.eps', format='eps', dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()
#def optimise(scenarios,en):'''
    
    
    
