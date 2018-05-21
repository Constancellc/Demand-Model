import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

day0 = datetime.datetime(2017,5,1)

hh = {}

outfile = '../../Documents/pecan-street/heatmaps/'

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
                hh[hhid] = {1:[],2:[]}
                for t in range(24):
                    hh[hhid][1].append([0.0]*365)
                    hh[hhid][2].append([0.0]*365)
                
            ev = float(row[2])
            solar = float(row[3])
            grid = float(row[4])

            hh[hhid][1][23-hour][dayNo] = ev
            hh[hhid][2][23-hour][dayNo] = grid+solar


for hhid in hh:
    if max(max(hh[hhid][1])) < 1:
        continue
    plt.figure()
    for f in range(1,3):
        plt.subplot(2,1,f)
        if f == 1:
            plt.title(hhid)
        plt.imshow(hh[hhid][f],vmin=0,aspect=5)
        plt.yticks(np.arange(2,26,4),y_ticks)
        plt.xticks([61,153,245,334],x_ticks)
        plt.colorbar()

    plt.tight_layout()
    plt.savefig(outfile+hhid+'.pdf',format='pdf')
    plt.close()

            
        
