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

        time = int(int(row[1][12:14])*12+int(row[1][15:17])/12)
        
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
            
