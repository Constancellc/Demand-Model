import csv
import matplotlib.pyplot as plt
import random
import numpy as np

rawData = '../../Documents/UKDA-5340-tab/constance-trips.csv'

profiles = {}
vehicles = []

chosen = ['2014007827','2014008246','2014004729']

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
            for i in range(start,end):
                profiles[vehicle][i] = 1
        else:
            for i in range(start,24*60*7):
                profiles[vehicle][i] = 1
            for i in range(0,end):
                profiles[vehicle][i] = 1

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
plt.savefig('../../Dropbox/thesis/chapter3/img/example_nts.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()
