import csv

rawData = '../../Documents/UKDA-5340-tab/csv/tripsWithVehicleNosAndMonths.csv'

with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print row

