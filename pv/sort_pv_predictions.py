import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

stem = '../../Documents/cornwall-pv-predictions/'

filenames = {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',8:'aug',
             9:'sep',10:'oct',11:'nov',12:'dec'}

for month in filenames:
    data = []
    with open(stem+filenames[month]+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)

    rankedData = []
    for row in data:
        total = 0
        for cell in row:
            total += float(cell)

        rankedData.append([total]+row)

    sortedData = sorted(rankedData)

    with open(stem+filenames[month]+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for row in sortedData:
            writer.writerow(row[1:])

