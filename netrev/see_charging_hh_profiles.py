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


plt.show()
