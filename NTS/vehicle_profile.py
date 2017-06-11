import csv
import matplotlib.pyplot as plt
import random
import numpy as np

rawData = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

profiles = {}
vehicles = []

chosen = ['2014007827','2014008246','2014004729']

with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        if row[7] != '2014':
            continue

        vehicle = row[2]

        if vehicle not in chosen:
            continue


        try:
            start = int(row[8])+(int(row[5])-1)*24*60
            end = int(row[9])+(int(row[5])-1)*24*60
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
plt.figure(1)
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
    plt.grid()
    plt.imshow(heatmap,aspect=60,cmap='Blues')
    plt.yticks(range(0,7),y_ticks)
    plt.xticks(x,x_ticks)
    plt.ylabel('Weekday')
    if i == 2:
        plt.xlabel('Time')
    
    #plt.title(ID)


    #data = go.Heatmap(z=heatmap,x=np.linspace(0,24,num=24*60),y=range(0,7))

plt.figure(2)
for i in range(0,num_plot):
    plt.subplot(num_plot,1,i+1)
    plt.plot(plotted_profiles[i])
plt.show()
