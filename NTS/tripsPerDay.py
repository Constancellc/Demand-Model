import csv
import matplotlib.pyplot as plt

trips = '../../Documents/UKDA-5340-tab/csv/carDriverTrips.csv'
recordedDays = '../../Documents/UKDA-5340-tab/csv/days.csv'
houses = '../../Documents/UKDA-5340-tab/csv/householdsWithCars.csv'
noCars = '../../Documents/UKDA-5340-tab/csv/carLessHouseholds.csv'

days = {}
weekdays = {}

IDs = []

nWeekendTrips = [0]*100
nWeekdayTrips = [0]*100

households = []

#with open(houses,'rU') as csvfile:
#    reader = csv.reader(csvfile)
#    reader.next()
#    for row in reader:
#        households.append(int(row[0]))

'''
carLess = []

with open(noCars,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        carLess.append(int(row[0]))
       
print 'got households'
'''
with open(recordedDays,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        # skip households without vehicles
        #if int(row[3]) in carLess:
#            continue
        
        days[int(row[2])] = 0
        if int(row[7]) < 6:
            weekdays[int(row[2])] = 1
        else:
            weekdays[int(row[2])] = 0

print 'got days'



with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        dayID = int(row[3])
        days[dayID] += 1


for day in days:
    if weekdays[day] == 1:
        nWeekdayTrips[days[day]] += 1
    elif weekdays[day] == 0:
        nWeekendTrips[days[day]] += 1

plt.figure(1)
plt.bar(range(0,100),nWeekdayTrips)
plt.bar(range(0,100),nWeekendTrips,bottom=nWeekdayTrips)
plt.xlim(-1,15)
plt.show()
            
