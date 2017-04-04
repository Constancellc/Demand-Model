import csv

rawData = '../../Documents/UKDA-5340-tab/csv/tripsWithVehicleNosAndMonths.csv'
chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'


with open(chargeData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print row

