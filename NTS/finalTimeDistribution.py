import csv
import matplotlib.pyplot as plt

trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'


finishTimes = {}


with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        ID = row[2]

        try:
            endTime = int(float(row[9])/1)
        except:
            #print row[9]
            continue

        if ID not in finishTimes:
            finishTimes[ID] = endTime
        else:
            if finishTimes[ID] < endTime:
                finishTimes[ID] = endTime

y = [0]*2000

for ID in finishTimes:
    y[finishTimes[ID]] += 1

plt.figure(1)
plt.plot(y)
plt.show()
