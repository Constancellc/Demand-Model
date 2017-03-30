import csv

rawData = '../../Documents/UKDA-5340-tab/tab/stageeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/csv/carDriverTrips.csv'
outfile = '../../Documents/UKDA-5340-tab/csv/tripsWithVehicleNos.csv'

vehicleIDs = {}
with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    reader.next()
    for row in reader:
        tripID = row[2]
        vehicleID = row[7]

        if tripID not in vehicleIDs:
            vehicleIDs[tripID] = vehicleID

data = []

with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        if i == 0:
            data.append(row+['VehicleID'])
        else:
            data.append(row+[vehicleIDs[row[0]]])
        i += 1

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)

        
    
