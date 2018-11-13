import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# OK. This version I am controlling the charge INTO the battery not grid

'''
What am I comparing? The case where I optimized with knowledge of charging
losses and the case where I didn't know.
'''
power = [0,0.5,1,1.5,2,2.5,3,3.5]
eff = [0,0.3,0.5,0.6,0.8,0.85,0.89,0.9]
eff_ = {}
for i in range(8):
    eff_[power[i]] = eff[i]
grid = [0]
grid0 = [0]

t_int = 30 # mins
T = 16
for i in range(1,8):
    grid.append(power[i]/eff[i]) # power from grid
    grid0.append(power[i]/0.9)
    
    #charge.append(power[i]*eff[i]*t_int/60)
    #charge0.append(power[i]*0.9*t_int/60)
    
print(grid)
goal = 5 # kWh
tol = 0.5*0.5*t_int/60
                
possible = []
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
                                    energy = a*power[0]+b*power[1]+\
                                             c*power[2]+d*power[3]+\
                                             e*power[4]+f*power[5]+\
                                             g*power[6]+h*power[7]
                                    energy = energy*t_int/60
                        
                                    if energy > goal-tol and energy<goal+tol:
                                        possible.append([a,b,c,d,e,f,g,h])


print(len(possible))
        
'''
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
'''
Q = np.zeros((55,55))
p = np.zeros((55,1))
# now for each option I need to find the network losses
with open('p.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        for j in range(len(row)):
            Q[i][j] = float(row[j])
        i += 1
        
with open('q.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        p[i] = float(row[0])
        i += 1

with open('c.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        c = float(row[0])

losses = {0:0}
#losses_ = {0:0}

for i in range(1,8):
    x = np.array([-1000]*55)
    losses0 = np.matmul(x,np.matmul(Q,x)) + np.matmul(x,p) + c
    x[-1] -= grid[i]*1000
    losses1 = np.matmul(x,np.matmul(Q,x)) + np.matmul(x,p) + c
    losses[grid[i]] = losses1-losses0

print(losses)
def get_losses(p):
    l1 = 0
    l2 = 0
    for t in range(len(p)):
        l1 += losses[p[t]]/2000 # W -> kWh
        #l2 += (1-eff_[p[t]])*p[t]/2 # kW -> kWh

    return [l1,l2]

best = None
best_ = None
ev_en = None
lowest = 1000000
lowest_ = 1000000
for i in range(len(possible)):
    profile = []
    #profile0 = []
    for p in range(8):
        profile += [grid[p]]*possible[i][p]
    [l1,l2] = get_losses(profile)
    l = l1+l2
    if l < lowest:
        lowest = l
        best = profile
    if 

plt.figure()
plt.plot(best)
plt.show()
    


''''
# and choose the optimal in each case
best = None
ev_en = None
lowest = 1000000
lowest_ = 1
for i in range(len(possible)):
    profile = []
    ev = 0
    for p in range(8):
        profile += [power[p]]*possible[i][p]
        ev += charge[p]*possible[i][p]
    yy[int(sum(profile)/2)] += 1
    [l1,l2] = get_losses(profile)
    l = l1+l2
    if l < lowest:
        lowest = l
        lowest_ = l1
        best = profile
        ev_en = ev

       
best0 = None
ev_en0 = None
lowest0 = 1000000
lowest0_ = 1
for i in range(len(possible0)):
    profile = []
    ev = 0
    for p in range(8):
        profile += [power[p]]*possible0[i][p]
        ev += charge[p]*possible0[i][p]
    xx[int(sum(profile)/2)] += 1
    [l1,l2] = get_losses(profile)
    if l1 < lowest0:
        lowest0 = l1
        lowest0_ = l2
        best0 = profile
        ev_en0 = ev
x_ = []
best_ = []
best0_ = []
for i in range(len(best)):
    x_.append(i)
    x_.append(i+1)
    best_.append(best[i])
    best_.append(best[i])
    best0_.append(best0[i])
    best0_.append(best0[i])

plt.figure(figsize=(7,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'
plt.subplot(1,2,1)
plt.plot(x_,best0_,'r',label='Charger losses\nnot incorporated')
#plt.annotate(str(round(ev_en0,2))+'kWh',(4.5,0.2),color='r')
plt.plot(x_,best_,'g',label='Charger losses\nincorporated')
#plt.annotate(str(round(ev_en,2))+'kWh',(12.5,1.7),color='g')
#plt.plot(best0)
#plt.plot(best,'g',label='Charger losses\nincorporated')
plt.legend()
plt.ylim(0,3.5)
plt.xlim(0,16)
plt.xticks([4,8,12],[2,4,6])
plt.xlabel('Time (hours)')
plt.ylabel('Power (kW)')
plt.grid()

plt.subplot(1,2,2)
plt.bar([1,2],[lowest0+lowest0_,lowest],label='Charger\nlosses')
plt.bar([1,2],[lowest0,lowest_],label='Distribution\nlosses')
plt.legend()
plt.ylabel('Losses (kWh)')
plt.grid()
plt.xticks([1,2],['Charger losses\nnot incorporated','Charger losses\nincorporated'])
plt.tight_layout()
plt.show()



'''
