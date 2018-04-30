import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime

maxDemand = 0

profiles = {}
with open('../../Documents/gridwatch.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:

        time = int(int(row[1][12:14])*12+int(row[1][15:17])/5)
        
        year = int(row[1][:5])
        month = int(row[1][6:8])
        date = int(row[1][9:11])

        day = datetime.datetime(year,month,date)

        weekday = day.isoweekday()

        if month not in profiles:
            profiles[month] = {}

        if weekday not in profiles[month]:
            profiles[month][weekday] = {}

        if date not in profiles[month][weekday]:
            profiles[month][weekday][date] = [0.0]*(24*12)

        profiles[month][weekday][date][time] = int(row[2])

titles = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',
          9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

for month in profiles:
    for weekday in profiles[month]:
        incomplete = []
        for date in profiles[month][weekday]:
            skip = False
            for i in range(24*12):
                if profiles[month][weekday][date][i] < 1000:
                    skip = True
                if i > 1:
                    if (profiles[month][weekday][date][i]-
                        profiles[month][weekday][date][i-1]) > 5000:
                        skip = True
            if skip == True:
                incomplete.append(date)
        for date in incomplete:
            del profiles[month][weekday][date]
plt.figure(1)

day = 2
for month in profiles:
    plt.subplot(4,3,int(month))
    av = []
    h = []
    l = []

    N = len(profiles[month][day])
    Q1 = int(N/4)
    for t in range(24*12):
        x = []
        for date in profiles[month][day]:
            x.append(profiles[month][day][date][t])
        x = sorted(x)
        av.append(sum(x[Q1:-Q1])/(1000*(N-2*Q1)))
        l.append(sum(x[:Q1])/(Q1*1000))
        h.append(sum(x[-Q1:])/(Q1*1000))
    plt.plot(np.linspace(0,24,num=24*12),av)
    plt.fill_between(np.linspace(0,24,num=24*12),l,h,alpha=0.5)
    plt.ylim(20,60)
    plt.xlim(0,24)
    plt.xticks([4,12,20],['04:00','12:00','20:00'])
    plt.grid()
    plt.title(titles[month],y=0.65)
        
    # ok, I want to store the standard results somewhere
    with open('../ng-data/'+titles[month]+str(day)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time','low','medium','high'])
        for t in range(24*12):
            writer.writerow([10*t,l[t],av[t],h[t]])
plt.tight_layout()
plt.show()


        
            
