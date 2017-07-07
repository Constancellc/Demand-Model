import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

day1 = datetime.datetime(2013,01,01)
data = []

months = {}

stem = '../../Documents/cornwall-pv-predictions/'

capacity = 560398 # kW

with open('GBPV_data.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        month = int(row[1][5:7])

        if month not in months:
            months[month] = {}
            
        date = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),int(row[1][8:10]))
        day = (date-day1).days

        if day not in months[month]:
            months[month][day] = [0]*48

        
        time = int(row[1][11:13])*2+int(row[1][14:16])/30
        try:
            generation = float(row[2])
            installed = float(row[10])
        except:
            generation = 0.0

        months[month][day][time] = int(generation/installed*capacity)

filenames = {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',8:'aug',
             9:'sep',10:'oct',11:'nov',12:'dec'}

for month in months:
    with open(stem+filenames[month]+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for day in months[month]:
            writer.writerow(months[month][day])

