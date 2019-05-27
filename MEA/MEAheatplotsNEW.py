import numpy as np
import matplotlib.pyplot as plt
import random
import datetime
import csv
#import plotly
#import plotly.plotly as py
#import plotly.graph_objs as go

#py.sign_in('constancellc','grM8GaLZ6QaGd4vyooJe')



tripData = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'#EVTripData.csv'
chargeData = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges.csv'#EVChargeData.csv'
ranges = '../../Documents/My_Electric_avenue_Technical_Data/constance/ranges.csv'

dates = {}

with open(ranges,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
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
            next(reader)
            for row in reader:
                userID =  row[0]

                if userID != vehicle:
                    continue

                dayNo = int(row[1])-1

                start = int(row[2])
                end = int(row[3])

                if end < 24*60:
                    for i in range(start,end):
                        heatmap[24*60-1-i][dayNo] = labels[j]

                else:
                    for i in range(start,24*60):
                        heatmap[24*60-1-i][dayNo] = labels[j]
                    for i in range(24*60,end):
                        heatmap[24*60-1-(i-24*60)][dayNo+1] = labels[j]

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

y = np.linspace(0,24*60,num=7)
x = np.linspace(1,len(date_list),num=10)
                
y_ticks = ['23:59','20:00','16:00','12:00','08:00','04:00','00:00']
x_ticks = ['Jan\n\'14','Mar\n\'14','May\n\'14','Jul\n\'14','Sep\n\'14',
           'Nov\n\'14','Jan\n\'15','Mar\n\'15','May\n\'15','Jul\n\'15']



plt.rcParams["font.family"] = 'serif'
plt.imshow(heatmap, cmap='bwr', aspect=0.2, interpolation='nearest')
plt.yticks(y,y_ticks)
plt.xticks(x,x_ticks)
plt.grid(ls=':')
plt.tight_layout()
plt.savefig('../../Dropbox/thesis/chapter3/img/example_mea.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)
plt.show()

