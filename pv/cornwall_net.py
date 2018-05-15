import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np


pv_months = {}
pwr_months = {}
day1 = datetime.datetime(2013,1,1)
capacity = 560398 # kW
sf = 1349.8/116997.9

# first get pv
with open('GBPV_data.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        month = int(row[1][5:7])

        if month not in pv_months:
            pv_months[month] = {}
            
        date = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),int(row[1][8:10]))
        day = (date-day1).days

        if day not in pv_months[month]:
            pv_months[month][day] = [0]*48
        
        time = int(int(row[1][11:13])*2+int(row[1][14:16])/30)
        try:
            generation = float(row[2])
            installed = float(row[11])
        except:
            generation = 0.0

        pv_months[month][day][time] = int(generation*capacity/installed)

ms = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,
      'Sep':9,'Oct':10,'Nov':11,'Dec':12,'JAN':1,'FEB':2,'MAR':3,'APR':4,
      'MAY':5,'JUN':6,'JUL':7,'AUG':8,'SEP':9,'OCT':10,'NOV':11,'DEC':12}

files = ['DemandData_2011-2016.csv','DemandData_2017.csv',
         'DemandData_2018_0.csv']

# then get electricity
for file in files:
    with open('../../Documents/'+file,'rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            date = datetime.datetime(int(row[0][7:]),ms[row[0][3:6]],int(row[0][:2]))
            dayNo = (date-day1).days
            if dayNo < 0:
                continue
            
            month = ms[row[0][3:6]]

            if month not in pwr_months:
                pwr_months[month] = {}

            if dayNo not in pwr_months[month]:
                pwr_months[month][dayNo] = [0]*48

            try:
                pwr_months[month][dayNo][int(row[1])-1] = float(row[2])*sf*1000
            except:
                print(int(row[1])-1)
        
net = {}
for month in pv_months:
    net[month] = {}
    for day in pv_months[month]:
        if day not in pwr_months[month]:
            continue
        net[month][day] = [0.0]*48
        for t in range(48):
            net[month][day][t] = pwr_months[month][day][t]-\
                                 pv_months[month][day][t]
        
stem = '../../Documents/cornwall-pv-predictions/'

filenames = {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',8:'aug',
             9:'sep',10:'oct',11:'nov',12:'dec'}

for month in net:
    with open(stem+filenames[month]+'-net.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for day in net[month]:
            writer.writerow(net[month][day])

for month in net:
    m = []
    l1 = []
    l2 = []
    u1 = []
    u2 = []
    for t in range(48):
        x = []
        for day in net[month]:
            x.append(net[month][day][t])
        x = sorted(x)
        l2.append(x[int(len(x)*0.05)])
        l1.append(x[int(len(x)*0.25)])
        m.append(x[int(len(x)*0.5)])
        u1.append(x[int(len(x)*0.75)])
        u2.append(x[int(len(x)*0.95)])

    with open(stem+'av-'+filenames[month]+'-net.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for p in [l2,l1,m,u1,u2]:
            writer.writerow(p)

