import csv

rawData = '../../Documents/UKDA-5340-tab/csv/householdsWithCars.csv'
awData = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'
chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
grid = '../ng-data/Demand_Data2016.csv'
newTrips = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'
newCharges = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges.csv'
features = '../../Documents/My_Electric_avenue_Technical_Data/constance/features.csv'

with open(features,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print row

