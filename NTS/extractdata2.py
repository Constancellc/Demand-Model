import csv

# this is going to redefine a trip file containing only info i need

households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
infile = '../../Documents/UKDA-5340-tab/csv/tripsWithVehicleNosAndMonths.csv'
outfile = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

#dates = {}
days = {}
with open(households,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    reader.next()
    for row in reader:
        householdID = row[0]
        month = row[10]

        if householdID not in days:
            days[householdID] = row[14]

data = []

with open(infile,'rU') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        if i == 0:
            data.append(row+['WeekDay'])
        else:
            dayNo = int(days[row[5]])+int(row[7])
            if dayNo > 7:
                dayNo -= 7
            data.append(row+[str(dayNo)])
        i += 1

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for line in data:
        row = []

        row += [line[0]] # tripID
        row += [line[5]] # householdID
        row += [line[-3]] # vehicleID
        row += [line[6]] # personNo
        row += [line[3]] # ConstanceDayID - this is day and household specific
        row += [line[-1]] # day of week (code)
        row += [line[-2]] # month (code)
        row += [line[1]] # year
        row += [line[11]] # tripStart
        row += [line[12]] # tripEnd
        row += [line[14]] # tripDistance
        row += [line[10]] # purpose from
        row += [line[11]] # purpose to
        
                        
        writer.writerow(row)

        
    
