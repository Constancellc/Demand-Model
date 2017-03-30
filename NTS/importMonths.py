import csv

households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/csv/tripsWithVehicleNos.csv'
outfile = '../../Documents/UKDA-5340-tab/csv/tripsWithVehicleNosAndMonths.csv'

months = {}
with open(households,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    reader.next()
    for row in reader:
        householdID = row[0]
        month = row[10]

        if householdID not in months:
            months[householdID] = month

data = []

with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        if i == 0:
            data.append(row+['Month'])
        else:
            try:
                data.append(row+[months[row[5]]])
            except KeyError:
                print 'problem with household '+row[4]
                data.append(row+['0'])
                
        i += 1

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)

        
    
