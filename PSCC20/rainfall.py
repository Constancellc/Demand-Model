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
        r[int(5*res[s][i][0])] += (res[s][i][3]-res[s][i][2])
        n[int(5*res[s][i][0])] += 1

    for i in range(len(n)):
        if n[i] > 0:
            r[i] = float(r[i])/n[i]
        

    plt.plot(np.linspace(0,20,num=100),filt.gaussian_filter1d(r[:100],25),
             color=blue2(float(s)*0.999/60000))
plt.xlim(0,20)

top = 0.9
btm = 0.5

plt.grid(zorder=0)

for i in range(100):
    y1 = btm+(top-btm)*(i/100)
    y2 = btm+(top-btm)*((i+1)/100)
    plt.plot([6.8,6.8],[y1,y2],lw=6,c=blue2(i/100))

tcks = ['0','20','40','60']
for i in range(4):
    y_ = btm+(top-btm)*(i/3)-0.01
    plt.annotate('- '+tcks[i]+' GW',(6.9,y_))
p = patches.Rectangle(
    (5.6,0.42), 4.17, 0.7,color='lightgray',zorder=2)


ax.add_patch(p)
plt.annotate('Installed Solar',(5.67,1.02))
plt.xlabel('Rainfall (mm)')
plt.ylabel('$\Delta  f(x)$')
plt.savefig('../../Dropbox/papers/PSCC-20/img/rainfall.eps', format='eps', dpi=300,
            bbox_inches='tight', pad_inches=0)
plt.show()


