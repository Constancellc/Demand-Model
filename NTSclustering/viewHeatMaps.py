import csv
import matplotlib.pyplot as plt
from matplotlib import colors
import random
import numpy as np
import copy
import scipy.ndimage.filters as filt

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '9'
fig, axs = plt.subplots(3,1,figsize=(6,3))
for i in range(3):
    heatmap = np.zeros((6,48))
    with open(stem+'jointPdfW'+str(i+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        s = 0
        for row in reader:
            for t in range(48):
                heatmap[5-s][t] = float(row[t])*100
            s += 1

    im = axs[i].imshow(heatmap,aspect='auto',vmin=0,vmax=100,cmap='magma')
    axs[i].set_yticks([0,2,4])
    axs[i].set_yticklabels(['6','4','2'])
    axs[i].set_xticks([7.5,15.5,23.5,31.5,39.5])
    axs[i].set_ylabel('SOC')
    if i == 2:
        axs[i].set_xticklabels(['04:00','08:00','12:00','16:00','20:00'])
    else:
        axs[i].set_xticklabels(['','','','',''])

    axs[i].set_title(str(i+1),color='w',y=0.55)
#plt.tight_layout()
fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.87, 0.15, 0.02, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.ax.set_yticklabels(['0%','20%','40%','60%','80%','100%'])

plt.xticks([7.5,15.5,23.5,31.5,39.5],['04:00','08:00','12:00','16:00','20:00'])
#plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/weekdayHM.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)

fig, axs = plt.subplots(3,1,figsize=(6,3))
for i in range(3):
    heatmap = np.zeros((6,48))
    with open(stem+'jointPdfWE'+str(i+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        s = 0
        for row in reader:
            for t in range(48):
                heatmap[5-s][t] = float(row[t])*100
            s += 1
    #plt.subplot(3,1,i+1)
    im = axs[i].imshow(heatmap,aspect='auto',vmin=0,vmax=100,cmap='magma')
    axs[i].set_yticks([0,2,4])
    axs[i].set_yticklabels(['6','4','2'])
    axs[i].set_xticks([7.5,15.5,23.5,31.5,39.5])
    axs[i].set_ylabel('SOC')
    if i == 2:
        axs[i].set_xticklabels(['04:00','08:00','12:00','16:00','20:00'])
    else:
        axs[i].set_xticklabels(['','','','',''])

    axs[i].set_title(str(i+1),color='w',y=0.55)
fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.87, 0.15, 0.02, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.ax.set_yticklabels(['0%','20%','40%','60%','80%','100%'])
#plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/weekendHM.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)
#fig.colorbar(im,ax=axs,fraction=.5)

#plt.xticks([7.5,15.5,23.5,31.5,39.5],['04:00','08:00','12:00','16:00','20:00'])

fig3, axs3 = plt.subplots(2,1,figsize=(6,2))
heatmap = np.zeros((6,48))
with open(stem+'jointPdfW_.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    s = 0
    for row in reader:
        for t in range(48):
            heatmap[5-s][t] = float(row[t])*100
        s += 1
axs3[0].imshow(heatmap,aspect='auto',vmin=0,vmax=20,cmap='magma')
axs3[0].set_yticks([0,2,4])
axs3[0].set_yticklabels(['6','4','2'])
axs3[0].set_xticks([7.5,15.5,23.5,31.5,39.5])
axs3[0].set_ylabel('SOC')
axs3[0].set_xticklabels(['','','','',''])

axs3[0].set_title('Weekday',color='w',y=0.55)

heatmap = np.zeros((6,48))
with open(stem+'jointPdfWE_.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    s = 0
    for row in reader:
        for t in range(48):
            heatmap[5-s][t] = float(row[t])*100
        s += 1
im = axs3[1].imshow(heatmap,aspect='auto',vmin=0,vmax=20,cmap='magma')
axs3[1].set_yticks([0,2,4])
axs3[1].set_yticklabels(['6','4','2'])
axs3[1].set_ylabel('SOC')
axs3[1].set_xticks([7.5,15.5,23.5,31.5,39.5])
axs3[1].set_xticklabels(['04:00','08:00','12:00','16:00','20:00'])
axs3[1].set_title('Weekend',color='w',y=0.55)

fig3.subplots_adjust(right=0.85)
cbar_ax = fig3.add_axes([0.87, 0.15, 0.02, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_ticks([0,4,8,12,16,20])
cbar.set_ticklabels(['0%','4%','8%','12%','16%','20%'])
#cbar.ax.set_yticks([0,4,8,12,16,20])
#cbar.ax.set_yticklabels(['0%','4%','8%','12%','16%','20%'])
#plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/randomHM.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)

#plt.xticks([7.5,15.5,23.5,31.5,39.5],['04:00','08:00','12:00','16:00','20:00'])
#plt.tight_layout()
plt.show()
