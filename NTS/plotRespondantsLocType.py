import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv
import copy

# first get the hosuehold file
file = '../../Documents/UKDA-5340-tab/constance-households.csv'
counter = [0]*4

with open(file,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        try:
            counter[int(row[2])-1] += 1
        except:
            continue


s = sum(counter)/100
for i in range(4):
    counter[i] = counter[i]/s


plt.figure(figsize=(4.5,4) )
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 10

plt.subplot(2,1,1)
plt.bar(np.arange(4)-0.2,counter,width=0.4,label='Sample',zorder=3)
plt.bar(np.arange(4)+0.2,[36.9,44.6,9.2,9.3],width=0.4,label='UK',zorder=3)
plt.xticks(range(4),['Urban\nConurbation','Urban\nTown','Rural\nTown',
                     'Rural\nVillage'])
plt.ylabel('Composition (%)')
plt.legend()
plt.grid(zorder=0.5)
plt.subplot(2,1,2)
plt.bar(np.arange(4),[100*(counter[0]-36.9)/36.9,
                      100*(counter[1]-44.6)/44.6,
                      100*(counter[2]-9.2)/9.2,
                      100*(counter[3]-9.3)/9.3],width=0.6,zorder=3)
plt.xticks(range(4),['Urban\nConurbation','Urban\nTown','Rural\nTown',
                     'Rural\nVillage'])
plt.ylabel('Sample Bias (%)')
plt.grid()
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/respondants_ltype.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0.1)
plt.show()
