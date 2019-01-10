import csv
import matplotlib.pyplot as plt
import datetime

charges = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'

outStem = '../../Documents/My_Electric_avenue_Technical_Data/constance/ST1charges/'
# okay let's keep things simpler and just get a time series for both charging
# and velocity for each vehicle.

dayS = datetime.datetime(2014,10,23)
dayE = datetime.datetime(2015,7,3)

charge = {}
          
with open(charges,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0][:3] != 'ST1':
            continue
        vehicle = row[0][3:]

        if vehicle in ['015','017','051','095']:
            continue
        
        if vehicle not in charge:
            charge[vehicle] = []

        day = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                int(row[1][8:10]))
        if day < dayS:
            continue
        if day > dayE:
            continue
        dayN = (day-dayS).days
            
        start = 60*int(row[1][11:13])+int(row[1][14:16])
        kWh = 2*(float(row[4])-float(row[3]))

        charge[vehicle].append([day,start,kWh])
        

for vehicle in charge:
    with open(outStem+vehicle+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['day','start','kWh'])
        for i in range(len(charge[vehicle])):
            writer.writerow(charge[vehicle][i])


