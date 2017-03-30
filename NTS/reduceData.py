import csv

recordedDays = '../../Documents/UKDA-5340-tab/csv/days.csv'
noCars = '../../Documents/UKDA-5340-tab/csv/carLessHouseholds.csv'
cars = '../../Documents/UKDA-5340-tab/csv/householdsWithCars.csv'
outfile = '../../Documents/UKDA-5340-tab/csv/daysCarOwnersOnly.csv'

carless = []

with open(cars,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        houses.append(row[0])
        
with open(noCars,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        carless.append(row[0])

fullData = {}
reducedData = []

with open(recordedDays,'rU') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        if i == 0:
            reducedData.append(row)
        else:
            householdID = row[4]
            if householdID not in carless:
                reducedData.append(row)

        i += 1

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in reducedData:
        writer.writerow(row)
