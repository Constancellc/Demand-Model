import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# OK. This version I am controlling the charge INTO the battery not grid

# this is the power into the battery
#power = [0,0.5,1,1.5,2,2.5,3]
power = [0,0.5,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3]
# I will need to redo these
eff = [0,0.5,0.7,0.79,0.82,0.85,0.87,0.88,0.89,0.9,0.9]


nStates = len(power)
print(nStates)
grid = [0]
grid0 = [0]
eff_ = {0:0}
for i in range(1,nStates):
    grid.append(power[i]/eff[i])
    grid0.append(power[i]/0.9)
    eff_[power[i]] = eff[i]

t_int = 30 # mins
T = 20

goal = 9
              
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
                                if a+b+c+d+e+f+g+h > T:
                                    continue
                                for i in range(T+1-a-b-c-d-e-f-g-h):
                                    if a+b+c+d+e+f+g+h+i > T:
                                        continue
                                    for j in range(T+1-a-b-c-d-e-f-g-h-i):
                                        if a+b+c+d+e+f+g+h+i+j > T:
                                            continue
                                        for k in range(T+1-a-b-c-d-e-f-g-h-i-j):
                                            if a+b+c+d+e+f+g+h+i+j+k == T:
                                                energy = a*power[0]+b*power[1]+\
                                                         c*power[2]+d*power[3]+\
                                                         e*power[4]+f*power[5]+\
                                                         g*power[6]+h*power[7]+\
                                                         i*power[8]+j*power[9]+\
                                                         k*power[10]
                                                energy = energy/2
                                                if energy == goal:
                                                    possible.append([a,b,c,d,e,
                                                                     f,g,h,i,j,
                                                                     k])
print(len(possible))
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
losses0 = {0:0}
for i in range(1,nStates):
    # first the power we think the grid is experiencing
    x = np.array([-1000]*55)
    losses_ = np.matmul(x,np.matmul(Q,x)) + np.matmul(x,p) + c
    x[-1] -= grid0[i]*1000
    losses1 = np.matmul(x,np.matmul(Q,x)) + np.matmul(x,p) + c
    losses0[power[i]] = (losses1-losses_)[0]
    # then the power the grid is actually experiencing
    x = np.array([-1000]*55)
    x[-1] -= grid[i]*1000
    losses1 = np.matmul(x,np.matmul(Q,x)) + np.matmul(x,p) + c
    losses[power[i]] = (losses1-losses_)[0]

def get_losses(p):
    l1 = 0
    l2 = 0
    for t in range(len(p)):
        l1 += (losses[p[t]]*t_int)/(1000*60)
        if p[t] > 0:
            l2 += ((p[t]/eff_[p[t]])-p[t])*t_int/60
    return [l1,l2]
    
def get_losses0(p):
    l = 0
    for t in range(len(p)):
        l += losses0[p[t]]
    return l

best = None
best_ = None
best__ = None
lowest = 100000
lowest_ = 100000
lowest__ = 100000
for i in range(len(possible)):
    # first using actual losses 
    profile = []
    for j in range(nStates):
        profile += [power[nStates-1-j]]*possible[i][nStates-1-j]
    [l1,l2] = get_losses(profile)
    if (l1+l2) < lowest:
        lowest = (l1+l2)
        best = possible[i]

    if l1 < lowest__:
        lowest__ = l1
        best__ = possible[i]

    # then using predicted losses
    l = get_losses0(profile)
    if l < lowest_:
        lowest_ = l
        best_ = possible[i]

def zoh(p):
    x = []
    p_ = []
    for t in range(len(p)):
        x.append(t)
        x.append(t+1)
        p_.append(p[t])
        p_.append(p[t])
        
    return [x,p_]

plt.figure(figsize=(6,3.5))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'



profile_ = []
for j in range(nStates):
    profile_ += [power[nStates-1-j]]*best_[nStates-1-j]
    [l1_,l2_] = get_losses(profile_)
plt.subplot(1,2,1)
[x,p] = zoh(profile_)
plt.plot(x,p,'r',label='(a)')

profile_ = []
for j in range(nStates):
    profile_ += [grid[nStates-1-j]]*best_[nStates-1-j]
plt.subplot(1,2,2)
[x,p] = zoh(profile_)
plt.plot(x,p,'r',label='(a)')

plt.subplot(1,2,1)
plt.title('Power into battery')
# now investigate the best case
profile = []
for j in range(nStates):
    profile += [power[nStates-1-j]]*best[nStates-1-j]
    [l1,l2] = get_losses(profile)
[x,p] = zoh(profile)
plt.plot(x,p,'b',ls='--',label='(b)')
profile = []
for j in range(nStates):
    profile += [grid[nStates-1-j]]*best[nStates-1-j]

plt.subplot(1,2,2)
plt.title('Power from grid')
[x,p] = zoh(profile)
plt.plot(x,p,'b',ls='--',label='(b)')

profile__ = []
for j in range(nStates):
    profile__ += [power[nStates-1-j]]*best__[nStates-1-j]
    [l1__,l2__] = get_losses(profile__)
    
plt.subplot(1,2,1)
[x,p] = zoh(profile__)
plt.plot(x,p,'g',ls=':',label='(c)')
plt.grid()
plt.xlim(0,T)
plt.xticks([4,8,12,16],[2,4,6,8])
plt.xlabel('Time (hours)')
plt.ylim(0,3.5)
plt.ylabel('Power (kW)')
profile__ = []
for j in range(nStates):
    profile__ += [grid[nStates-1-j]]*best__[nStates-1-j]
plt.subplot(1,2,2)
[x,p] = zoh(profile__)
plt.plot(x,p,'g',ls=':',label='(c)')
plt.grid()
plt.xlim(0,T)
plt.xticks([4,8,12,16],[2,4,6,8])
plt.xlabel('Time (hours)')
plt.ylim(0,3.5)
plt.legend()
plt.tight_layout()
plt.savefig('../../Dropbox/papers/PowerTech/img/power.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)

plt.figure(figsize=(5,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'
plt.bar([1,2,3],[l1_+l2_,l1+l2,l1__+l2__],label='Charger losses',zorder=3)
plt.bar([1,2,3],[l1_,l1,l1__],label='Distribution losses',zorder=3)
plt.legend()
plt.xticks([1,2,3],['(a)','(b)','(c)'])
plt.grid(zorder=0)
plt.ylabel('Energy losses (kWh)')
plt.tight_layout()
plt.savefig('../../Dropbox/papers/PowerTech/img/losses.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
