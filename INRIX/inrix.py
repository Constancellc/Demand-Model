
import matplotlib.pyplot as plt
import numpy as np
import csv
import random


infiles = ['20131111_Oxford_2.csv','20131112_Oxford_2.csv',
           '20131113_Oxford_2.csv','20131114_Oxford_2.csv',
           '20131115_Oxford_2.csv']

outfile = 'inrix.csv'
days = ['Monday','Tuesday','Wednesday','Thursday','Friday']

results = []

for i in range(0,5):
    with open(infiles[i],'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # people neither starting or ending in Oxford are easy to ignore
            if row['start_external'] == '1' and row['end_external'] == '1':
                continue

            # if the time isn't recorded ignore it
            hour = row['day_hour']
            if hour == 'NULL':
                continue
            hour = int(hour)

            # if it starts not in Ox in the morning they probs don't live there
            if row['start_external'] == '1' and hour < 10:
                continue

            if row['end_external'] == '1' and hour > 20:
                continue

            quarter = int(row['time_period'])
            
            start = row['origin_zone_number']
            end = row['destination_zone_number']

            time = hour

            results.append([days[i],time,start,end])

counters = {'Monday':[0]*24,'Tuesday':[0]*24,'Wednesday':[0]*24,
            'Thursday':[0]*24,'Friday':[0]*24}

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in results:
        counters[row[0]][row[1]] += 1
        writer.writerow(row)

total = []
plt.figure(1)
for day in days:
    total += counters[day]
plt.plot(total)
plt.show()
