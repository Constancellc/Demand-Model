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
pdf = chargingPdf[2][15:-15]
normalise(pdf)

chargingPdf = {}
for i in range(3):
    chargingPdf[i] = []
with open(stem+'chargePdfW2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(3):
            for t in range(30):
                chargingPdf[i].append(float(row[i+1])/3000)
pdf2 = chargingPdf[2][15:-15]
normalise(pdf2)

print(len(pdf))
print(len(pdf2))
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
ax1.plot(t,pdf,label='After Journey')
ax1.plot(t,pdf2,label='Random')
plt.legend()
ax1.set_ylim(0,0.004)
plt.xticks(x,x_ticks)
ax1.set_yticks([0,0.001,0.002,0.003,0.004])#,['0%','0.1%','0.2%','0.3%'])

plt.grid()
plt.ylabel('Probability')

ax2 = ax1.twinx()
ax2.plot(t,use,label='Vehicle Use',c='#808080',ls=':')
ax2.set_yticks([0,1])
ax2.set_ylim([0,1.333])
ax2.set_xlim(0,48)

for u in usage:
    for ti in range(u[0],u[1]):
        pdf[ti] = 0
        pdf2[ti] = 0

for ti in range(usage[0][1],usage[1][0]):
    pdf[ti] = 0
    pdf2[ti] = 0
        
normalise(pdf)
normalise(pdf2)

ax1 = fig.add_subplot(3,1,2)
ax1.set_title('(b)',y=0.65)
ax1.plot(t,pdf)
ax1.plot(t,pdf2)
ax1.set_ylim(0,0.006)
plt.xticks(x,x_ticks)
ax1.set_yticks([0,0.002,0.004,0.006])
plt.ylabel('Probability')

plt.grid()
ax2 = ax1.twinx()
ax2.plot(t,use,label='Vehicle Use',c='#808080',ls=':')
plt.legend()
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
        s2 += pdf2[ti]
        
for ti in range(1440):
    if ti in ends:
        pdf[ti] = pdf[ti]*0.7/s1
    else:
        pdf[ti] = pdf2[ti]*0.3/s2

normalise(pdf)

t2 = []
p2 = []
for ti in range(1440):
    if ti not in ends:
        t2.append(t[ti])
        p2.append(pdf[ti])
        pdf[ti] = 0
ax1 = fig.add_subplot(3,1,3)
ax1.set_title('(c)',y=0.65)
ax1.plot(t,pdf)
ax1.plot(t2,p2)
ax1.set_ylim(0,0.08)
plt.xticks(x,x_ticks)
ax1.set_yticks([0,0.025,0.05,0.075])

plt.ylabel('Probability')

plt.grid()
ax2 = ax1.twinx()
ax2.plot(t,use,c='#808080',ls=':')
ax2.set_yticks([0,1])
ax2.set_ylim([0,1.06666])
ax2.set_xlim(0,48)
plt.tight_layout()

plt.savefig('../../Dropbox/papers/clustering/img/diagram.eps', format='eps', dpi=1000)


plt.show()
