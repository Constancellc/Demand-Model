import csv
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.filters as filt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.patches as patches

res = {}
with open('res3.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    #next(reader)
    for row in reader:
        if row[2] not in res:
            res[row[2]] = []
        res[row[2]].append([float(row[0]),float(row[1]),float(row[3]),
                            float(row[4])])

blues = cm.get_cmap('Blues', 1000)
new = blues(np.linspace(0, 1, 1000))
new[:1,:] =  np.array([1,1,1,1])
blue2 = ListedColormap(new)
fig = plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 10
ax = fig.add_axes([0.1,0.15,0.85,0.8])
for s in res:
    print(s)
    r = [0]*500
    n = [0]*500
    for i in range(len(res[s])):
        r[50+int(5*res[s][i][1])] += (res[s][i][3]-res[s][i][2])
        n[50+int(5*res[s][i][1])] += 1

    for i in range(len(n)):
        if n[i] > 0:
            r[i] = float(r[i])/n[i]
        

    plt.plot(np.linspace(-5,25,num=150),filt.gaussian_filter1d(r[:150],15),
             color=blue2(float(s)*0.999/60000))
plt.xlim(-2,20)
plt.ylim(0,2.47)

top = 0.95
btm = 0.15

plt.grid(zorder=0)

for i in range(100):
    y1 = btm+(top-btm)*(i/100)
    y2 = btm+(top-btm)*((i+1)/100)
    plt.plot([11.8,11.8],[y1,y2],lw=6,c=blue2(i/100))

tcks = ['0','20','40','60']
for i in range(4):
    y_ = btm+(top-btm)*(i/3)-0.05
    plt.annotate('- '+tcks[i]+' GW',(11.9,y_))
p = patches.Rectangle(
    (10.6,0.08), 4.57, 1.15,color='lightgray',zorder=2)


ax.add_patch(p)
plt.annotate('Installed Solar',(10.67,1.1))
plt.xlabel('Temperature ($\degree$C)')
plt.ylabel('$\Delta  f(x)$')
plt.savefig('../../Dropbox/papers/PSCC-20/img/temperature.eps', format='eps', dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()


