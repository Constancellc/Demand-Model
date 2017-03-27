import numpy as np
import matplotlib.pyplot as plt
import random
import datetime
import csv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

#py.sign_in('constancellc','grM8GaLZ6QaGd4vyooJe')



tripData = '../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'
chargeData = '../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'

data = [tripData, chargeData]
labels = [1,-1]

def createHeatmap(vehicle):
    results = {0:[], 1:[]}

    earliest = None
    latest = None
    
    for j in range(0,2):
        with open(data[j]) as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            for row in reader:
                userID =  row[0]

                if userID != vehicle:
                    continue

                stampIn = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                            int(row[1][8:10]),int(row[1][11:13]),
                                            int(row[1][14:16]))

                stampOut = datetime.datetime(int(row[2][:4]),int(row[2][5:7]),
                                             int(row[2][8:10]),int(row[2][11:13]),
                                             int(row[2][14:16]))

                if earliest is None:
                    earliest = stampIn
                elif stampIn < earliest:
                    earliest = stampIn

                if latest is None:
                    latest = stampOut
                elif stampOut > latest:
                    latest = stampOut

                results[j].append([stampIn,stampOut])

    period = latest-earliest
    days = period.days

    heatmap = []
    for i in range(0,24*60):
       heatmap.append([0]*(days+2))

    for j in range(0,2):
        for row in results[j]:
            dayNo = (row[0]-earliest).days
            midnight = datetime.datetime(row[0].year,row[0].month,row[0].day,0,0)
            chargeTime = (row[1]-row[0]).seconds/60
                
            index = (row[0]-midnight).seconds/60
            for i in range(index,index+chargeTime):
                if i < 24*60:
                    heatmap[i][dayNo] = labels[j]
                else:
                    heatmap[i-24*60][dayNo+1] = labels[j]

    # generating axis
    date_list = [earliest + datetime.timedelta(days=x) for x in range(0,days+2)]

    return heatmap, date_list


time_list = []
for hour in range(0,24):
    for minute in range(0,60):
        time_list.append(datetime.time(hour,minute))


vehicle = 'ST1114'
run = createHeatmap(vehicle)
heatmap = run[0]
date_list = run[1]

data = [go.Heatmap(z=heatmap,x=date_list,y=time_list,colorscale='Viridis')]
layout = go.Layout(title=vehicle, yaxis=dict(ticks = '', nticks=12))
fig = go.Figure(data=data, layout=layout)
        
plotly.offline.plot(fig, filename='basic-heatmap.html')

