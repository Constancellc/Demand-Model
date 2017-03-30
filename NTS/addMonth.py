import csv


# This section extracts the trip data

trips = '../../Documents/UKDA-5340-tab/csv/carDriverTrips.csv'
houses = '../../Documents/UKDA-5340-tab/csv/householdsWithCars.csv' 
outfile = '../../Documents/UKDA-5340-tab/csv/carDriverTripsWithMonths.csv'

data = []

households = []

with open(houses, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        households.append(row)

with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        if i < 1:
            data.append(row+['Month'])
        else:
            ID = row[5]
            startMonth = ''
            for entry in households:
                if startMonth != '':
                    continue
                if entry[0] == ID:
                    startMonth = entry[2]
            if startMonth == '':
                print 'start month not found'
            data.append(row+[startMonth])
        i += 1

print data
with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)

