import csv
import matplotlib.pyplot as plt
import math
import numpy as np

tripData = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'
chargeData = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges.csv'

# checking energy balance
'''
energyOut = {}
energyIn = {}

with open(tripData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        ID = row[0]

        if ID not in energyOut:
            energyOut[ID] = 0
            energyIn[ID] = 0

        energyOut[ID] += int(row[5])

with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        energyIn[row[0]] += int(row[4])

for ID in energyOut:
    print float(energyOut[ID]-energyIn[ID])/energyOut[ID]
'''

# finding aggregate stats
outfile = '../../Documents/My_Electric_avenue_Technical_Data/constance/features.csv'

starts = {}
ends = {}
numTrips = {}
energy = {}
length = {}



with open(tripData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        ID = row[0]

        if ID not in starts:
            starts[ID] = {'weekday':{},'weekend':{}}
            ends[ID] = {'weekday':{},'weekend':{}}
            numTrips[ID] = {'weekday':{},'weekend':{}}
            energy[ID] = {'weekday':[0,0],'weekend':[0,0]}
            length[ID] = {'weekday':[0,0],'weekend':[0,0]}

        if row[6] == '1':
            flag = 'weekend'
        else:
            flag = 'weekday'

        day = row[1]

        start = int(row[2])
        end = int(row[3])

        if end < start:
            end += 24*60

        if day not in starts[ID][flag]:
            starts[ID][flag][day] = 24*60

        if start < starts[ID][flag][day]:
            starts[ID][flag][day] = start

        if day not in ends[ID][flag]:
            ends[ID][flag][day] = 0

        if end > ends[ID][flag][day]:
            ends[ID][flag][day] = end
            

        if day not in numTrips[ID][flag]:
            numTrips[ID][flag][day] = 1
        else:
            numTrips[ID][flag][day] += 1

        energy[ID][flag][0] += int(row[5])
        energy[ID][flag][1] += 1

        if end != start:
            length[ID][flag][0] += np.log(float(end-start))
            length[ID][flag][1] += 1

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID','start time av. (w)','start time var (w)',
                     'start time  av. (w/e)','start time var (w/e)',
                     'end time av. (w)','end time var (w)','end time av. (w/e)',
                     'end time var (w/e)','# trips (w)','# trips (w/e)',
                     'energy per trip (w)','energy per trip (w/e)',
                     'log trip length (w)','log trip length (w/e)'])
    for ID in energy:
        row = [ID]

        sumWeekdayStarts = 0
        for day in starts[ID]['weekday']:
            sumWeekdayStarts += starts[ID]['weekday'][day]

        if sumWeekdayStarts == 0:
            avWeekdayStart = 0
            varWeekdayStart = 0
        else:
            avWeekdayStart = sumWeekdayStarts/len(starts[ID]['weekday'])
            dWeekdayStarts = 0

            for day in starts[ID]['weekday']:
                d = starts[ID]['weekday'][day]-avWeekdayStart
                dWeekdayStarts += d*d

            varWeekdayStart = int(math.sqrt(dWeekdayStarts/len(starts[ID]['weekday'])))


        sumWeekendStarts = 0
        for day in starts[ID]['weekend']:
            sumWeekendStarts += starts[ID]['weekend'][day]

        if sumWeekendStarts == 0:
            avWeekendStart = 0
            varWeekendStart = 0
            
        else:
            avWeekendStart = sumWeekendStarts/len(starts[ID]['weekend'])           
            dWeekendStarts = 0

            for day in starts[ID]['weekend']:
                d = starts[ID]['weekend'][day]-avWeekendStart
                dWeekendStarts += d*d

            varWeekendStart = int(math.sqrt(dWeekendStarts/len(starts[ID]['weekend'])))

        
        sumWeekdayEnds = 0
        for day in ends[ID]['weekday']:
            sumWeekdayEnds += ends[ID]['weekday'][day]

        if sumWeekdayEnds == 0:
            avWeekdayEnd = 0
            varWeekdayEnd = 0
        else:
            avWeekdayEnd = sumWeekdayEnds/len(ends[ID]['weekday'])
            dWeekdayEnds = 0

            for day in ends[ID]['weekday']:
                d = ends[ID]['weekday'][day]-avWeekdayEnd
                dWeekdayEnds += d*d

            varWeekdayEnd = int(math.sqrt(dWeekdayEnds/len(ends[ID]['weekday'])))


        sumWeekendEnds = 0
        for day in ends[ID]['weekend']:
            sumWeekendEnds += ends[ID]['weekend'][day]

        if sumWeekendEnds == 0:
            avWeekendEnd = 0
        else:
            avWeekendEnd = sumWeekendEnds/len(ends[ID]['weekend'])
            dWeekendEnds = 0

            for day in ends[ID]['weekend']:
                d = ends[ID]['weekend'][day]-avWeekendEnd
                dWeekendEnds += d*d

            varWeekendEnd = int(math.sqrt(dWeekendEnds/len(ends[ID]['weekend'])))

            
        row += [avWeekdayStart, varWeekdayStart, avWeekendStart, varWeekendStart,
                avWeekdayEnd, varWeekdayEnd, avWeekendEnd, varWeekendEnd]

        sumWeekdayTrips = 0
        maxDay = 0
        for day in numTrips[ID]['weekday']:
            if int(day) > maxDay:
                maxDay = int(day)
            sumWeekdayTrips += numTrips[ID]['weekday'][day]
        
        sumWeekendTrips = 0
        for day in numTrips[ID]['weekend']:
            if int(day) > maxDay:
                maxDay = int(day)
            sumWeekendTrips += numTrips[ID]['weekend'][day]

        avWeekdayTrips = float(int(float(100*sumWeekdayTrips*7)/(5*maxDay)))/100
        
        avWeekendTrips = float(int(float(100*sumWeekendTrips*7)/(2*maxDay)))/100

        row += [avWeekdayTrips, avWeekendTrips]

        try:
            row += [energy[ID]['weekday'][0]/energy[ID]['weekday'][1]] # Wh
        except:
            row += [0]
            
        try:
            row += [energy[ID]['weekend'][0]/energy[ID]['weekend'][1]] # Wh
        except:
            row += [0]

        try:
            row += [float(int(1000*length[ID]['weekday'][0]/length[ID]['weekday'][1]))/1000] # log mins
        except:
            row += [0]

        try:
            row += [float(int(1000*length[ID]['weekend'][0]/length[ID]['weekend'][1]))/1000] # log mins
        except:
            row += [0]
            
        writer.writerow(row)
        
            
            
        
