import csv
import matplotlib.pyplot as plt
import random
import numpy as np

rawData = '../../Documents/UKDA-5340-tab/constance-trips.csv'

profiles = {}
vehicles = []

chosen = ['2014004729']#,'2014008246','2014004729']

with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[8] != '2014':
            continue

        vehicle = row[2]

        if vehicle not in chosen:
            continue
        try:
            start = int(row[9])+(int(row[6])-2)*24*60
            end = int(row[10])+(int(row[6])-2)*24*60
            dist = float(row[11])
        except:
            continue

        
        if vehicle not in vehicles:
            vehicles.append(vehicle)
            profiles[vehicle] = [0]*(24*60*7)

        if start >= 24*60*7:
            start -= 24*60*7
        if end >= 24*60*7:
            end -= 24*60*7

        if start < end:
            d = dist/(end-start)
            d = d*60 # miles/min -> mph
            for i in range(start,end):
                profiles[vehicle][i] = d
        else:
            d = dist/(24*60*7+end-start)
            d = d*60
            for i in range(start,24*60*7):
                profiles[vehicle][i] = d
            for i in range(0,end):
                profiles[vehicle][i] = d

days = ['Mon','Tue','Wed']
plt.figure()
plt.rcParams["font.family"] = 'serif'
for day in range(3):
    plt.subplot(3,2,day*2+1)
    plt.title(days[day],y=0.7)
    p = profiles[chosen[0]][24*60*day:24*60*(day+1)]
    p2 = [0.0]*48
    for t in range(1440):
        p2[int(t/30)] += p[t]/sum(p)
    plt.plot(np.linspace(0,24,1440),p)
    plt.xticks([4,12,20],['04:00','12:00','20:00'])
    plt.xlim(0,24)
    plt.ylim(0,70)
    plt.grid(ls=':')
    plt.ylabel('Speed (mph)')

    plt.subplot(3,2,day*2+2)
    plt.title(days[day],y=0.7)
    plt.bar(range(1,49),p2,zorder=3)
    plt.xlim(0.5,48.5)
    plt.ylim(0,0.35)
    plt.grid(ls=':')
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/example_fv.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)

p = []
for i in range(3):
    p.append([0.0]*48)
p[0][14] = 0.5
p[0][36] = 0.5
p[1][15] = 0.5
p[1][37] = 0.5
p[2][24] = 0.5
p[2][25] = 0.5
plt.figure(figsize=(9,2))
ttls = ['(a)','(b)','(c)']
for i in range(3):
    plt.subplot(1,3,i+1)
    plt.bar(range(1,49),p[i])
    plt.title(ttls[i],y=0.8)
    plt.grid()
    plt.xlim(0.5,48.5)
    plt.xticks([1,12,24,36,48])
    plt.ylim(0,0.6)
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/example_dist_prob.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
num_plot = 3
plotted_profiles = {}
plt.rcParams["font.family"] = 'serif'
t = np.linspace(0,24*7,num=24*60*7)
x = np.linspace(120,1320,num=6)
x_ticks = ['02:00','06:00','10:00','14:00','18:00','22:00']

y_ticks = ['M','','W','','F','','S']
for i in range(0,num_plot):
    plt.subplot(num_plot,1,i+1)

    heatmap = []
    for j in range(0,7):
        heatmap.append([0]*24*60)
    ID = vehicles[i]#int(random.random()*len(vehicles))]
    plotted_profiles[i] = profiles[ID]

    c = 0
    for j in range(0,7):
        for k in range(0,1440):
            heatmap[j][k] = profiles[ID][c]
            c += 1
    plt.grid(ls=':')
    plt.imshow(heatmap,aspect=60,cmap='Blues')
    plt.yticks(range(0,7),y_ticks)
    plt.xticks(x,x_ticks)
    plt.ylabel('Weekday')
    
    #plt.title(ID)
plt.tight_layout()
#plt.savefig('../../Dropbox/thesis/chapter3/img/example_nts.eps', format='eps',
#            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
