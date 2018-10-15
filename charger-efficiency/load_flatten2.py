import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag, sparse, solvers

simulationDay = 3
nH = 50
nV = 5
#capacity = 30 # kWh
pMax = 7.0 # kW
t_int = 30 # mins

T = int(1440/t_int)

# I need to get household load
totalH = []
for t in range(48):
    totalH.append(random.random()*40)

# And vehicle requirements
av = []
for v in range(nV):
    av.append([0.0]*T)
    '''
    for t in range(10,14):
        av[v][t] = 1.0
    '''
    t1 = int(random.random()*48)
    t2 = int(random.random()*(48-t1))
    for t in range(t2+1):
        av[v][t1+t] = 1.0
        
# there will be 2 nV T + 1 decision variables

#b = matrix([5.0]*nV+[0.09]*(nV*T))
#A = matrix(0.0,(nV+nV*T,2*nV*T+1))
#b = matrix([5.0]*nV+[0.0]*nV+[0.09]*(nV*T))
#A = matrix(0.0,(2*nV+nV*T,2*nV*T+1))
b = matrix([5.0]*nV+[0.0]*nV)
A = matrix(0.0,(2*nV,2*nV*T+1))
G = matrix(0.0,(T,2*nV*T+1))
q = matrix([0.0]*(2*nV*T)+[1.0])
P = spdiag([0.0001]*(2*nV*T+1))
'''
P0 = sparse([[spdiag([0.001]*T)]*nV]*nV)
P1 = matrix(0.0,(nV*T,nV*T+1))
P2 = matrix(0.0,(nV*T+1,2*nV*T+1))
P = sparse([[P0],[P1]])
P = sparse([P,P2])
del P0
del P1
del P2
'''

for v in range(nV):
    for t in range(T):
        A[v,v*T+t] = pMax*t_int/60 # charging
        A[v,(nV+v)*T+t] = -pMax*t_int/60 # losses

        A[v+nV,T*v+t] = av[v][t]# availability 
        A[v+nV,T*(v+nV)+t] = av[v][t]# availability

        #A[2*nV+v*T+t,v*T+t] = -0.04
        #A[2*nV+v*T+t,(v+nV)*T+t] = 1.0

        #A[nV+v*T+t,v*T+t] = -0.04 if no avaliaility
        #A[nV+v*T+t,(v+nV)*T+t] = 1.0

        G[t,T*v+t] = pMax
                
h0 = []
for t in range(T):
    G[t,2*T*nV] = -pMax
    h0.append(-1.0*totalH[t])

G0 = matrix(0.0,(nV*T,2*nV*T+1))
for v in range(nV):
    for t in range(T):
        G0[v*T+t,v*T+t] = 0.09
        G0[v*T+t,(v+nV)*T+t] = -1.0
        
        h0.append(-0.09)
        
G1 = sparse([[spdiag([-1.0]*(2*nV*T))],[matrix([0.0]*(2*nV*T))]])
G2 = sparse([[spdiag([1.0]*(nV*T))],[matrix(0.0,(nV*T,nV*T))],
             [matrix([0.0]*(nV*T))]])

G = sparse([G,G0,G1,G2])
h = matrix(h0+[0.0]*(2*nV*T)+[1.0]*(nV*T))

sol=solvers.qp(P,q,G,h,A,b)

x = sol['x']

individual = []
total = [0]*T

for t in range(T):
    total[t] += totalH[t]

for v in range(nV):
    individual.append([0]*T)
    for t in range(T):
        individual[v][t] = x[v*T+t]*pMax
        total[t] += x[v*T+t]*pMax

plt.figure()
plt.plot(total)
plt.plot(totalH)

plt.figure()
for v in individual:
    plt.plot(v)
plt.show()
                  

