import csv
import matplotlib.pyplot as plt
import datetime
trips = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'
charges = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'

outStem = '../../Documents/My_Electric_avenue_Technical_Data/training/'
# okay let's keep things simpler and just get a time series for both charging
# and velocity for each vehicle.

day0 = datetime.datetime(2013,1,1)
usage = {}
charge = {}


with open(trips,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        carry = False
        vehicle = row[0]
        if vehicle not in usage:
            usage[vehicle] = {}

        day = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                int(row[1][8:10]))
        dayN = (day-day0).days

        if dayN not in usage[vehicle]:
            usage[vehicle][dayN] = [0.0]*48
            
        start = 60*int(row[1][11:13])+int(row[1][14:16])
        end = 60*int(row[2][11:13])+int(row[2][14:16])

        if start == end:
            continue
        if end < start:
            end += 1440
            if dayN+1 not in usage[vehicle]:
                usage[vehicle][dayN+1] = [0.0]*48
        
        dist = float(row[3])/1000 # m -> km
            
        speed = dist/(end-start) # km per min

        for t in range(start,end):
            if t < 1440:
                usage[vehicle][dayN][int(t/30)] += speed
            else:
                usage[vehicle][dayN+1][int((t-1440)/30)] += speed

          
with open(charges,'r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        vehicle = row[0]
        if vehicle not in charge:
            charge[vehicle] = {}

        day = datetime.datetime(int(row[1][:4]),int(row[1][5:7]),
                                int(row[1][8:10]))
        dayN = (day-day0).days

        if dayN not in charge[vehicle]:
            charge[vehicle][dayN] = [0.0]*48
            
        start = 60*int(row[1][11:13])+int(row[1][14:16])
        end = 60*int(row[2][11:13])+int(row[2][14:16])

        time = start-end

        if end < start:
            carry = True
            carryT = end-1439
            end -= carryT

        for t in range(start,end):
            charge[vehicle][dayN][int(t/30)] += 1/30

        if carry == True:
            dayN += 1
            if dayN not in charge[vehicle]:
                charge[vehicle][dayN] = [0.0]*48
            for t in range(carryT):
                charge[vehicle][dayN][int(t/30)] += 1/30

for vehicle in usage:
    if vehicle not in charge:
        continue
    earliest = 10000
    latest = 0
    for day in usage[vehicle]:
        if day < earliest:
            earliest = day
        if day > latest:
            latest = day

    x = []
    y = []

    for day in range(earliest,latest+1):
        try:
            x += usage[vehicle][day]
        except:
            x += [0.0]*48
        try:
            y += charge[vehicle][day]
        except:
            y += [0.0]*48

    with open(outStem+vehicle+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['av_speed','p_charge'])
        for i in range(len(x)):
            writer.writerow([x[i],y[i]])

