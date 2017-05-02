import csv
import matplotlib.pyplot as plt

rawData = '../../Documents/UKDA-5340-tab/csv/householdsWithCars.csv'
awData = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'
chargeData = '../../Documents/My_Electric_avenue_Technical_Data/EVChargeData.csv'
tripData = '../../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv'
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
grid = '../ng-data/Demand_Data2016.csv'
newTrips = '../../Documents/My_Electric_avenue_Technical_Data/constance/trips.csv'
newCharges = '../../Documents/My_Electric_avenue_Technical_Data/constance/charges2.csv'
features = '../../Documents/My_Electric_avenue_Technical_Data/constance/features.csv'
starttimes = '../../Documents/My_Electric_avenue_Technical_Data/constance/ranges.csv'

profileStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/unchanged/'
profileStem2 = '../../Documents/My_Electric_avenue_Technical_Data/profiles/smart/'


smart = [0.0]*24*60
dumb = [0.0]*24*60

for i in range(1,56):
    with open(profileStem+str(i)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        j = 0
        for row in reader:
            print j
            dumb[j] += float(row[0])
            j += 1
    with open(profileStem2+str(i)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        j = 0
        for row in reader:
            smart[j] += float(row[0])
            j += 1

plt.figure(1)
plt.plot(smart)
plt.plot(dumb)
plt.show()

with open(newCharges,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        print row
        
