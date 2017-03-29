import csv
import matplotlib.pyplot as plt

outfile = '../../Documents/UKDA-5340-tab/csv/tripsWithVehicleNosAndMonths.csv'

vehicles = {}

testID = '2002000001'

with open(outfile,'rU') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        try:
            tripStart = int(row[-6])
            tripEnd = int(row[-5])

        except:
            continue
        
        vehicle = row[-2]

        if vehicle != testID:
            continue

        if vehicle not in vehicles:
            vehicles[vehicle] = [0]*24*60*7

        travelDay = int(row[6])-1 # will be different on other computer

        for i in range(tripStart,tripEnd):
            i += travelDay*24*60
            
            if i >= 24*60*7:
                i -= 24*60*7
                
            vehicles[vehicle][i] = 1


plt.figure(1)
for vehicle in vehicles:
    plt.plot(vehicles[vehicle])
plt.show()
        
    
