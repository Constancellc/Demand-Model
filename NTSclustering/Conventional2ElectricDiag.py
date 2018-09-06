import csv
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

def normalise(pdf):
    s = sum(pdf)
    for i in range(len(pdf)):
        pdf[i] = pdf[i]/s

chargingPdf = {}
for i in range(3):
    chargingPdf[i] = []

with open(stem+'chargePdfW.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(3):
            for t in range(30):
                chargingPdf[i].append(float(row[i+1])/3000)
pdf = chargingPdf[1][15:-15]
normalise(pdf)

usage = [[456,501],[1010,1055]]
use = [0]*1440

for u in usage:
    for t in range(u[0],u[1]):
        use[t] = 1
        


x = [4,12,20,28,36,44]
x_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']
t = np.linspace(0,48,num=1440)

fig = plt.figure(figsize=(5,4))

plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'

ax1 = fig.add_subplot(3,1,1)
ax1.set_title('(a)',y=0.65)
ax1.plot(t,pdf)
ax1.set_ylim(0,0.004)
plt.xticks(x,x_ticks)
ax1.set_yticks([0,0.001,0.002,0.003,0.004])#,['0%','0.1%','0.2%','0.3%'])

plt.grid()
ax2 = ax1.twinx()
ax2.plot(t,use,c='#808080',ls=':')
ax2.set_yticks([0,1])
ax2.set_ylim([0,1.333])
ax2.set_xlim(0,48)



for u in usage:
    for ti in range(u[0],u[1]):
        pdf[ti] = 0
        
normalise(pdf)

ax1 = fig.add_subplot(3,1,2)
ax1.set_title('(b)',y=0.65)
ax1.plot(t,pdf)
ax1.set_ylim(0,0.004)
plt.xticks(x,x_ticks)
ax1.set_yticks([0,0.001,0.002,0.003,0.004])

plt.grid()
ax2 = ax1.twinx()
ax2.plot(t,use,c='#808080',ls=':')
ax2.set_yticks([0,1])
ax2.set_ylim([0,1.333])
ax2.set_xlim(0,48)

ends = []
for u in usage:
    ends.append(u[1])
    ends.append(u[1]+1)
    ends.append(u[1]+2)
    ends.append(u[1]+3)
    ends.append(u[1]+4)

s1 = 0
s2 = 0
for ti in range(1440):
    if ti in ends:
        s1 += pdf[ti]
    else:
        s2 += pdf[ti]
        
for ti in range(1440):
    if ti in ends:
        pdf[ti] = pdf[ti]*0.7/s1
    else:
        pdf[ti] = pdf[ti]*0.3/s2

normalise(pdf)

ax1 = fig.add_subplot(3,1,3)
ax1.set_title('(c)',y=0.65)
ax1.plot(t,pdf)
ax1.set_ylim(0,0.08)
plt.xticks(x,x_ticks)
ax1.set_yticks([0,0.025,0.05,0.075])

plt.grid()
ax2 = ax1.twinx()
ax2.plot(t,use,c='#808080',ls=':')
ax2.set_yticks([0,1])
ax2.set_ylim([0,1.06666])
ax2.set_xlim(0,48)
plt.tight_layout()
plt.show()
