import csv
import datetime
import matplotlib.pyplot as plt

hhID = '5110'
profiles = {}
maxDay = 0
with open('../../Documents/sharonb/7591/csv/profiles.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] != hhID:
            continue
        p = []
        for i in range(2,50):
            p.append(float(row[i]))
        profiles[int(row[1])] = p
        if maxDay < int(row[1]):
            maxDay = int(row[1])

y = []
x = []
for i in range(maxDay):
    for t in range(48):
        try:
            y.append(profiles[i+1][t])
        except:
            continue
        x.append(i*48+t)

with open('../../Documents/sharonb/7591/csv/'+hhID+'.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(y)):
        writer.writerow([x[i],y[i]])

with open('../../Documents/sharonb/7591/csv/'+hhID+'.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
