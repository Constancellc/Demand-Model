import csv

with open('../../Documents/UKDA-5340-tab/csv/householdsWithCars.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    n = 0
    for row in reader:
        n += 1

print n
