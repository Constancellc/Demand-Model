import numpy as np
import matplotlib.pyplot as plt
import random
import datetime
import csv

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges2.csv'

soc = {}

with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[6] == '1': # weekend
            continue
        iSOC = float(row[4])
        fSOC = float(row[5])

        if fSOC == iSOC:
            continue

        if int(iSOC*100) not in soc:
            soc[int(iSOC*100)] = 0

        soc[int(iSOC*100)] += 1

observed = []
for s in soc:
    observed.append(s)

observed = sorted(observed)

pdf = [0]*101
pdf[0] = soc[0]

c = 0
for i in range(1,101):
    if i in soc:
        pdf[i] = soc[i]
        c += 1
    else:
        f = (i-observed[c])/(observed[c+1]-observed[c])
        pdf[i] = (1-f)*soc[observed[c]]+f*soc[observed[c+1]]

s = sum(pdf)
for i in range(len(pdf)):
    pdf[i] = pdf[i]*100/s

# now working out the breaking up
i = 0
lines = []
text = []
carry = 0
for lim in [5,20,50,20,5]:
    total = carry
    while total < lim:
        total += pdf[i]
        i += 1
    carry = (total-lim)
    lines.append(i)
    if len(lines) == 1:
        text.append(0.5*i)
    else:
        text.append(0.5*(lines[-1]+lines[-2]))
    print(i)

text.append(0.5*(lines[-1]+100))
print(lines)
s = [5,20,50,20,5]   
plt.figure(figsize=(5,2))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
plt.grid()
plt.plot(np.arange(0,1.01,0.01),pdf)
plt.xlabel('SOC at plug in')
plt.ylabel('Probability density')
plt.ylim(0,1.6)
plt.xlim(0,1)
for line in lines:
    if line == 101:
        continue
    plt.plot([line/100,line/100],[0,pdf[line]],'k',ls=':')
for i in range(len(text)-1):
    plt.text(text[i]/100-0.03,0.35*pdf[int(text[i])],str(s[i])+'%',
             color='r',fontsize=9)
plt.tight_layout()
plt.savefig('../../Dropbox/papers/smart-charging/soc.eps', format='eps', dpi=1000)
plt.show()

av = 0
for i in range(0,lines[0]):
    av += pdf[i]*i/5
print(av)
av = 0
for i in range(lines[0],lines[1]):
    av += pdf[i]*i/20
print(av)
av = 0
for i in range(lines[1],lines[2]):
    av += pdf[i]*i/50
print(av)
av = 0
for i in range(lines[2],lines[3]):
    av += pdf[i]*i/20
print(av)
av = 0
for i in range(lines[3],lines[4]):
    av += pdf[i]*i/5
print(av)
