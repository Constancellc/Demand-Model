import csv
import datetime
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import random

features = '../../Documents/My_Electric_avenue_Technical_Data/constance/features.csv'

testVehicle = 'GC08'

with open(features,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        if row[0] == testVehicle:
            wStartAv = float(row[1])
            wStartVar = float(row[2])
            weStartAv = float(row[3])
            weStartVar = float(row[4])
            wEndAv = float(row[5])
            wEndVar = float(row[6])
            weEndAv = float(row[7])
            weEndVar = float(row[8])
            wTrips = float(row[9])
            weTrips = float(row[10])
            wEnergy = float(row[11]) # Wh
            weEnergy = float(row[12]) # Wh
            wLength = float(row[13]) # log mins
            weLength = float(row[14]) # log mins

# ok now we're going to try and simulate a profile from these aggregate stats

numberDays = 500
startDate = datetime.datetime(2016,01,01)

heatmap = []
for i in range(0,24*60):
    heatmap.append([0]*numberDays)

for i in range(0,numberDays):
    date = startDate+datetime.timedelta(1)
    
    if date.isoweekday() > 5:
        weekend = True
    else:
        weekend = False

    # first get the number of journeys which occured that day

    if weekend == True:
        nTrips = np.random.poisson(weTrips)
    else:
        nTrips = np.random.poisson(wTrips)
    
    if nTrips == 0:
        continue

    if weekend == True:
        firstTripStart = int(np.random.normal(weStartAv,weStartVar))
    else:
        firstTripStart = int(np.random.normal(wStartAv,wStartVar))

    if weekend == True:
        firstTripLength = int(np.exp(np.random.normal(weLength,0.4)))+1
    else:
        firstTripLength = int(np.exp(np.random.normal(wLength,0.4)))+1


    for j in range(firstTripStart,firstTripStart+firstTripLength):
        try:
            heatmap[j][i] = 1
        except:
            heatmap[j-24*60][i+1]
    if nTrips == 1:
        continue

    if weekend == True:
        lastTripEnd = int(np.random.normal(weEndAv,weEndVar))
    else:
        lastTripEnd = int(np.random.normal(wEndAv,wEndVar))

    if weekend == True:
        lastTripLength = int(np.exp(np.random.normal(weLength,0.4)))+1
    else:
        lastTripLength = int(np.exp(np.random.normal(wLength,0.4)))+1


    for j in range(lastTripEnd-lastTripLength,lastTripLength):
        try:
            heatmap[j][i] = 1
        except:
            try:
                heatmap[j-24*60][i+1]
            except:
                print ':('
                continue

    if nTrips == 2:
        continue

    earliestStart = firstTripStart+firstTripLength
    latestFinish = lastTripEnd-lastTripLength

    avaliability = [1]*(latestFinish-earliestStart)

    for dummy in range(0,nTrips-2):
        if weekend == True:
            length = int(np.exp(np.random.normal(weLength,0.4)))+1
        else:
            length = int(np.exp(np.random.normal(wLength,0.4)))+1


        # what i need to do is find all the avaliable windows which are long enough

        possibleStarts = []

        ii = 0
        windowSize = 0
        windowStart = 0
        while ii < len(avaliability)-1:
            windowStart = ii
            while avaliability[ii] == 1 and ii < len(avaliability)-1:
                ii += 1
                windowSize += 1
                
            if windowSize < length:
                windowSize = 0
            else:
                for l in range(windowStart,ii+1-length):
                    possibleStarts.append(l+earliestStart)
                windowSize = 0
                
            while avaliability[ii] == 0 and ii < len(avaliability)-1:
                ii += 1

        if possibleStarts == []:
            continue
                
        tripStart = possibleStarts[int(random.random()*len(possibleStarts))]
        tripEnd = tripStart+length

        for j in range(tripStart,tripEnd):
            try:
                heatmap[j][i] = 1
            except:
                try:
                    heatmap[j-24*60][i+1]
                except:
                    print ':('
                    print tripStart,
                    print tripEnd
                    continue
            try:
                avaliability[j-earliestStart] = 0
            except:
                print j,
                print earliestStart
                
data = [go.Heatmap(z=heatmap,colorscale='Viridis')]
layout = go.Layout(title=testVehicle)
fig = go.Figure(data=data, layout=layout)
        
plotly.offline.plot(fig, filename='basic-heatmap.html')
    

