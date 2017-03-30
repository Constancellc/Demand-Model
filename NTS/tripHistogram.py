import csv
import matplotlib.pyplot as plt

trips = '../../Documents/UKDA-5340-tab/csv/carDriverTrips.csv'

labels = []
histogram = {}


i = 6 # index which you are plotting
with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        if row[i] not in labels:
            labels.append(row[i])
            histogram[row[i]] = 1
        else:
            histogram[row[i]] += 1


y = []
x = []

for label in labels:
    y.append(histogram[label])
    x.append(int(label))
plt.figure(1)
plt.bar(x,y)
plt.show()
