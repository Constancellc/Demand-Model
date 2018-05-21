import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

day0 = datetime.datetime(2017,5,1)

hh = {}
av = {1:[0.0]*8760,2:[0.0]*8760}

ms = {0:'may17',1:'jun17',2:'jul17',3:'aug17',4:'sep17',5:'oct17',6:'nov17',
      7:'dec17',8:'jan18',9:'feb18',10:'mar18',12:'apr18'}

y_ticks = ['22:00','18:00','14:00','10:00','06:00','02:00']
x_ticks = ['Jul 17','Oct 17','Jan 18','Apr 18']
for m in ms:    
    with open('../../Documents/pecan-street/evs-hourly/'+ms[m]+'.csv',
              'rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            date = datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                                     int(row[0][8:10]))
            dayNo = (date-day0).days
            hour = int(row[0][11:13])
            hhid = row[1]
            
            if hhid not in hh:
                hh[hhid] = {1:[0.0]*8760,2:[0.0]*8760}
                
            ev = float(row[2])
            solar = float(row[3])
            grid = float(row[4])

            hh[hhid][1][dayNo*24+hour] = ev
            hh[hhid][2][dayNo*24+hour] = grid+solar

toRemove = []
for hhid in hh:
    if max(hh[hhid][1]) < 1 or max(hh[hhid][2]) < 1:
        toRemove.append(hhid)

for hhid in toRemove:
    del hh[hhid]

for hhid in hh:
    for t in range(8760):
        av[1][t] += hh[hhid][1][t]/len(hh)
        av[2][t] += hh[hhid][2][t]/len(hh)

# first finding correlation of average both
ex = 0.0
ey = 0.0
exy = 0.0
ex2 = 0.0
ey2 = 0.0

for t in range(8760):
    ex += av[1][t]/8760
    ey += av[2][t]/8760
    ex2 += (av[1][t]*av[1][t])/8760
    ey2 += (av[2][t]*av[2][t])/8760
    exy += (av[1][t]*av[2][t])/8760
corr0 = (exy-ex*ey)/np.sqrt((ex2-ex*ex)*(ey2-ey*ey))
print(corr0)
less = [0.0]*10
more = [0.0]*10
# then finding each individual correlation
for hhid in hh:
    ex = 0.0
    ey = 0.0    
    exy = 0.0
    ex2 = 0.0
    ey2 = 0.0

    for t in range(8760):
        ex += hh[hhid][1][t]/8760
        ey += hh[hhid][2][t]/8760
        ex2 += (hh[hhid][1][t]*hh[hhid][1][t])/8760
        ey2 += (hh[hhid][2][t]*hh[hhid][2][t])/8760
        exy += (hh[hhid][1][t]*hh[hhid][2][t])/8760

    corr = (exy-ex*ey)/np.sqrt((ex2-ex*ex)*(ey2-ey*ey))
    if corr < 0.4:#corr0:
        less[int(10*corr)] += 1.0/len(hh)
    else:
        more[int(10*corr)] += 1.0/len(hh)

print(sum(more))
plt.figure(1)
plt.bar(np.arange(10)+0.5,less)
plt.bar(np.arange(10)+0.5,more)
plt.show()

            
        
