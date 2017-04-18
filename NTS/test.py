import csv

rawData = '../../Documents/UKDA-5340-tab/csv/householdsWithCars.csv'
awData = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'
chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
grid = '../ng-data/Demand_Data2016.csv'

with open(tripData,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print row

