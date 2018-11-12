import matplotlib.pyplot as plt
import numpy as np
import csv
import random

power = [0,0.5,1,1.5,2,2.5,3,3.5]
eff = [0,0.3,0.5,0.6,0.8,0.85,0.89,0.9]
charge = []
charge0 = []

t_int = 30 # mins
T = 16
for i in range(8):
    charge.append(power[i]*eff[i]*t_int/60)
    charge0.append(power[i]*0.9*t_int/60)

goal = 5 # kWh
tol = 0.5*0.5*t_int/60

possible = []
possible0 =[]
for a in range(T):
    if a > T:
        continue
    for b in range(T+1-a):
        if a+b > T:
            continue
        for c in range(T+1-a-b):
            if a+b+c > T:
                continue
            for d in range(T+1-a-b-c):
                if a+b+c+d > T:
                    continue
                for e in range(T+1-a-b-c-d):
                    if a+b+c+d+e > T:
                        continue
                    for f in range(T+1-a-b-c-d-e):
                        if a+b+c+d+e+f > T:
                            continue
                        for g in range(T+1-a-b-c-d-e-f):
                            if a+b+c+d+e+f+g > T:
                                continue
                            for h in range(T+1-a-b-c-d-e-f-g):
                                if a+b+c+d+e+f+g+h == T:
                                    energy = a*charge[0]+b*charge[1]+\
                                             c*charge[2]+d*charge[3]+\
                                             e*charge[4]+f*charge[5]+\
                                             g*charge[6]+h*charge[7]
                                    energy0 = a*charge0[0]+b*charge0[1]+\
                                              c*charge0[2]+d*charge0[3]+\
                                              e*charge0[4]+f*charge0[5]+\
                                              g*charge0[6]+h*charge0[7]
                                    if energy > goal-tol and energy<goal+tol:
                                        #possible.append([a,b,c,d,e,f,g,h])
                                        possible.append([power[0]]*a+\
                                                        [power[1]]*b+\
                                                        [power[2]]*c+\
                                                        [power[3]]*d+\
                                                        [power[4]]*e+\
                                                        [power[5]]*f+\
                                                        [power[6]]*g+\
                                                        [power[7]]*h)
                                    if energy0 > goal-tol and energy0<goal+tol:
                                        #possible0.append([a,b,c,d,e,f,g,h])
                                        possible0.append([power[0]]*a+\
                                                         [power[1]]*b+\
                                                         [power[2]]*c+\
                                                         [power[3]]*d+\
                                                         [power[4]]*e+\
                                                         [power[5]]*f+\
                                                         [power[6]]*g+\
                                                         [power[7]]*h)

print(len(possible))
print(len(possible0))

best = [10]*T
for i in range(len(possible)):
    if max(possible[i]) < max(best):
        best = possible[i]
        losses = sum(best)/2-goal
        
best0 = [10]*T
for i in range(len(possible0)):
    if max(possible0[i]) < max(best0):
        best0 = possible0[i]
        losses0 = sum(best0)/2-goal
        
    
plt.figure()
plt.subplot(1,2,1)
plt.plot(best)
plt.plot(best0)
plt.ylim(0,3.75)

plt.subplot(1,2,2)
plt.bar([1],[losses])
plt.bar([2],[losses0])
plt.show()

# now for each option I need to find the network losses


# and choose the optimal in each case





