import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import datetime

hh = []
ev = []

with open('../../Documents/netrev/constance/charging_hh_profiles/hh.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        new = []
        for cell in row:
            new.append(float(cell))
        hh.append(new)
        
with open('../../Documents/netrev/constance/charging_hh_profiles/ev.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        new = []
        for cell in row:
            new.append(float(cell))
        ev.append(new)

hh_av = [0.0]*144
ev_av = [0.0]*144

print(len(hh))

for i in range(len(hh)):
    for t in range(144):
        hh_av[t] += float(hh[i][t+2])/len(hh)
        ev_av[t] += float(ev[i][t+2])/len(hh)

plt.figure(1)
plt.subplot(2,1,1)
plt.title('Average profiles',y=0.85)
plt.plot(hh_av,label='household')
plt.plot(ev_av,label='vehicle')
plt.legend(loc=[0.2,1.1],ncol=2)

ran = int(random.random()*len(hh))
plt.subplot(2,1,2)
plt.title('Sample individual\nprofiles',y=0.7)
plt.plot(hh[ran][2:])
plt.plot(ev[ran][2:])

# work out average correlation between same vehicle and household
same = [0]*100
rnd = [0]*100
for i in range(len(hh)):
    h1 = np.array(hh[i][2:])
    v1 = np.array(ev[i][2:])
    v2 = np.array(ev[int(random.random()*len(hh))][2:])

    h1 = h1/sum(h1)
    v1 = v1/sum(v1)
    v2 = v2/sum(v2)

    try:
        same[int(100*np.dot(h1,v1)/144)] += 1
        rnd[int(100*np.dot(h1,v2)/144)] += 1
    except:
        print('')
        print(np.dot(h1,v1))
        print(np.dot(h1,v2))
        continue


plt.figure(2)
plt.bar(range(len(same)),same)
plt.bar(range(len(rnd)),rnd)
plt.show()
