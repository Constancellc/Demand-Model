import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
import random
import plotly
#import plotly.plotly as py
import plotly.graph_objs as go
from operator import itemgetter

chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'

users = []
vehicles = ['GC04']#,'GC06','GC08','GC10']

plugIns = {}
months = {}

data = {'charge':chargeData, 'use':tripData}

with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        initialSOC = int(row[3])

        if row[0] not in users:
            users.append(row[0])
            months[row[0]] = []
            plugIns[row[0]] = {}

        month = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),1)

        if month not in months[row[0]]:
            months[row[0]].append(month)
            plugIns[row[0]][month] = [0]*13

        plugIns[row[0]][month][initialSOC] += 1       

allMonths = []

for ID in plugIns:
    for month in plugIns[ID]:
        if month not in allMonths:
            allMonths.append(month)

allMonths.sort()

#allMonths = allMonths[2:]

heatmap = []

for ID in plugIns:
    avs = []
    for month in allMonths:
        try:
            pdf = plugIns[ID][month]
        except KeyError:
            pdf = [0]*13
        N = sum(pdf)

        t = 0

        if N != 0:
            for i in range(0,13):
                t += float(pdf[i])*i/N
            avs.append(float(int(t*10))/10)
        else:
            avs.append(False)
    heatmap.append(avs)


heatmap = sorted(heatmap, key=itemgetter(13))
# sort the heatmap while maintaining data integrity
#heatmap.sort()

heatmapT = []

for i in range(0,len(allMonths)):
    row = []
    for j in range(0,len(heatmap)):
        row.append(heatmap[j][i])
    heatmapT.append(row)

data = [go.Heatmap(z=heatmapT,colorscale='Viridis')]
layout = go.Layout(title='Vehicle plug-in SOC with time',
                   xaxis=dict(title='vehicle'),
                   yaxis=dict(title='time (months)'))#vehicle, yaxis=dict(ticks = '', nticks=12))
fig = go.Figure(data=data, layout=layout)
        
plotly.offline.plot(fig, filename='basic-heatmap.html')
