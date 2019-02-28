import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

day1 = datetime.datetime(2013,1,1)
data = []
dataN = []

with open('GBPV_data.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        date = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),int(row[1][8:10]))
        day = (date-day1).days
        time = int(int(row[1][11:13])*2+int(row[1][14:16])/30)
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
        cmap[47-data[i][1]][data[i][0]] = data[i][2]
        cmapN[47-dataN[i][1]][dataN[i][0]] = dataN[i][2]
    except:
        print(data[i])
        print(len(cmap))

x = np.linspace(0,1825,num=11)
x_ticks = ['Jan\n2013','Jul\n2013','Jan\n2014','Jul\n2014','Jan\n2015',
           'Jul\n2015','Jan\n2016','Jul\n2016','Jan\n2017','Jul\n2017',
           'Jan\n2018']
y = np.arange(7,55,8)
y_ticks = ['20:00','16:00','12:00','08:00','04:00','00:00']


plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '12'

plt.subplot(2,1,1)
plt.title('UK PV Generation',y=0.85,color='white')
plt.imshow(cmap,aspect=15,vmax=10000)
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.xlim(90,data[-1][0])
cbar = plt.colorbar()
cbar.set_ticks([0,2000,4000,6000,8000,10000])
cbar.set_ticklabels(['0 GW','2 GW','4 GW','6 GW','8 GW','10 GW'])

plt.subplot(2,1,2)
plt.title('% of Potential Generated',y=0.85,color='white')
plt.imshow(cmapN,aspect=15,vmax=1)
plt.xticks(x,x_ticks)
plt.yticks(y,y_ticks)
plt.xlim(90,data[-1][0])
cbar = plt.colorbar()
cbar.set_ticks([0,0.2,0.4,0.6,0.8,1.0])
cbar.set_ticklabels(['0%','20%','40%','60%','80%','100%'])

plt.tight_layout()

plt.show()
