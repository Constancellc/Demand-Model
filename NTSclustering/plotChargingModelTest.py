import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

outstem = '../../Documents/simulation_results/NTS/clustering/power/'

d = []
dW = []
t = []
tW = []
u = []
uW = []

with open(outstem+'error.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        t.append(float(row[0]))
        d.append(float(row[1]))
        u.append(float(row[2]))
        tW.append(float(row[3]))
        dW.append(float(row[4]))
        uW.append(float(row[5]))

plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'
plt.subplot(2,1,1)
plt.plot(d,c='b',label='(a)')
plt.plot(u,c='r',ls='--',label='(b)')
plt.plot(t,ls=':',c='k',label='True')
plt.xlim(0,47)
plt.xticks([7,15,23,31,39],['04:00','08:00','12:00','16:00','20:00'])
plt.grid()
plt.ylabel('Likelihood of\nstarting charge')
plt.title('Weekday',y=0.7)
plt.legend()


plt.subplot(2,1,2)
plt.plot(dW,c='b',label='(a)')
plt.plot(uW,c='r',ls='--',label='(b)')
plt.plot(tW,ls=':',c='k',label='True')
plt.xlim(0,47)
plt.xticks([7,15,23,31,39],['04:00','08:00','12:00','16:00','20:00'])
plt.grid()
plt.ylabel('Likelihood of\nstarting charge')
plt.title('Weekend',y=0.7)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/error.eps',
            format='eps', dpi=1000)
plt.show()
