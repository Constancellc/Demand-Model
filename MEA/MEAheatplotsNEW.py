import numpy as np
import matplotlib.pyplot as plt
import random
import datetime
import csv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

#py.sign_in('constancellc','grM8GaLZ6QaGd4vyooJe')



tripData = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'#EVTripData.csv'
chargeData = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges.csv'#EVChargeData.csv'
ranges = '../../Documents/My_Electric_avenue_Technical_Data/constance/ranges.csv'

dates = {}

with open(ranges,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        user = row[0]
        startDay = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                     int(row[1][8:10]))
        endDay = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                     int(row[2][8:10]))
        
        dates[user] = [startDay,(endDay-startDay).days]
        
data = [tripData, chargeData]
labels = [1,-1]

def createHeatmap(vehicle):

    heatmap = []
    for i in range(0,24*60):
       heatmap.append([0]*(dates[vehicle][1]+2))
    
    for j in range(0,2):
        with open(data[j]) as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            for row in reader:
                userID =  row[0]

                if userID != vehicle:
                    continue

                dayNo = int(row[1])-1

                start = int(row[2])
                end = int(row[3])

                if end < 24*60:
                    for i in range(start,end):
                        heatmap[i][dayNo] = labels[j]

                else:
                    for i in range(start,24*60):
                        heatmap[i][dayNo] = labels[j]
                    for i in range(24*60,end):
                        heatmap[i-24*60][dayNo+1] = labels[j]

    # generating axis
    date_list = [dates[vehicle][0] + datetime.timedelta(days=x) for x in range(0,dates[vehicle][1]+2)]

    return heatmap, date_list


time_list = []
for hour in range(0,24):
    for minute in range(0,60):
        time_list.append(datetime.time(hour,minute))


vehicle = 'GC08'
run = createHeatmap(vehicle)
heatmap = run[0]
date_list = run[1]

data = [go.Heatmap(z=heatmap,x=date_list,y=time_list,colorscale='Viridis')]
layout = go.Layout(title=vehicle, yaxis=dict(ticks = '', nticks=12))
fig = go.Figure(data=data, layout=layout)
        
plotly.offline.plot(fig, filename='basic-heatmap.html')

