import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

day1 = datetime.datetime(2013,01,01)
data = []
dataN = []

with open('GBPV_data.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        date = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),int(row[1][8:10]))
        day = (date-day1).days
        time = int(row[1][11:13])*2+int(row[1][14:16])/30
        try:
            generation = float(row[2])
            installed = float(row[10])
        except:
            generation = 0.0

        data.append([day,time,generation])
        dataN.append([day,time,generation/installed])

cmap = np.zeros((48,data[-1][0]+1))
cmapN = np.zeros((48,data[-1][0]+1))

for i in range(0,len(data)):
    try:
        cmap[data[i][1]][data[i][0]] = data[i][2]
        cmapN[dataN[i][1]][dataN[i][0]] = dataN[i][2]
    except:
        print data[i]
        print len(cmap)

x = np.linspace(0,1642,num=10)
x_ticks = ['Jan\n2013','Jul\n2013','Jan\n2014','Jul\n2014','Jan\n2015',
           'Jul\n2015','Jan\n2016','Jul\n2016','Jan\n2017','Jul\n2017']
y = np.arange(4,48,4)
y_ticks = ['02:00','04:00','06:00','08:00','10:00','12:00','14:00','16:00',
           '18:00','20:00','22:00']


plt.figure(1)
plt.subplot(2,1,1)
plt.title('UK PV Generation')
plt.imshow(cmap,aspect=15)
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)

plt.subplot(2,1,2)
plt.title('% of Potential Generated')
plt.imshow(cmapN,aspect=15)
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)

plt.show()
