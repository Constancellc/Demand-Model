import csv

rawData = '../../Documents/UKDA-5340-tab/tab/tripeul2015.tab'
outfile = '../../Documents/UKDA-5340-tab/csv/carDriverTrips.csv'

data = []
with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    i = 0
    for row in reader:
        if i < 1:
            data.append(row)
        else:
            if row[16] != '5':
                continue
            data.append(row)
        i += 1

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for line in data:
        row = []
        row += line[0] # trip id
        row += line[1] # survey year
        row += line[2] # day id
        row += line[3] # individual id
        row += line[4] # household id
        row += line[6] # person number in household
        row += line[7] # day of the week
        row += line[8] # journey number of the day
        row += line[19] # trip purpose from
        row += line[20] # trip purpose to
        row += line[24] # trip start - minutes past midnight
        row += line[29] # trip end - minutes past midnight
        row += line[32] # trip time - minutes
        row += line[38] # trip distance - miles

        writer.writerow(row)


        
