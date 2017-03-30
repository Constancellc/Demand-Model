import csv


# This section extracts the trip data
'''

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
    i = 0
    for line in data:
        row = []
        row += [line[0]] # trip id
        row += [line[1]] # survey year
        row += [line[2]] # day id
        if i == 0:
            row += ['HouseholdDayID']
        else:
            row += [str(10*int(line[4])+int(line[7]))]
        row += [line[3]] # individual id
        row += [line[4]] # household id
        row += [line[6]] # person number in household
        row += [line[7]] # travel day
        row += [line[8]] # journey number of the day
        row += [line[19]] # trip purpose from
        row += [line[20]] # trip purpose to
        row += [line[24]] # trip start - minutes past midnight
        row += [line[29]] # trip end - minutes past midnight
        row += [line[32]] # trip time - minutes
        row += [line[38]] # trip distance - miles

        i += 1
        writer.writerow(row)
#'''
'''
# this section extracts the household info
rawData = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
outfile = '../../Documents/UKDA-5340-tab/csv/householdsWithCars.csv'

data = []
with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    i = 0
    for row in reader:
        if i < 1:
            data.append(row)
        else:
            if int(row[43]) == 1: # if the household has no car 
                continue
            data.append(row)
        i += 1

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for line in data:
        row = []
        row += [line[0]] # household id
        row += [line[1]] # survey year
        row += [line[10]] # month
        row += [line[23]] # income band
        row += [line[25]] # property type
        row += [line[26]] # tenancy type
        row += [line[28]] # region
        row += [line[30]] # number of adults
        row += [line[31]] # number of children
        row += [line[34]] # number of drivers licenses
        row += [line[36]] # number and type of employees
        row += [line[37]] # number of vehicles
        row += [line[39]] # number of lightweight cars
        row += [line[149]] # ONS rural / urban classification
        row += [line[156]] # 2011 census output area classification

        writer.writerow(row)
                
'''

'''
# this section extracts the household info
rawData = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
outfile = '../../Documents/UKDA-5340-tab/csv/carLessHouseholds.csv'

data = []
with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    i = 0
    for row in reader:
        if i < 1:
            data.append(row)
        else:
            if int(row[43]) == 1: # if the household has no car 
                data.append(row)
        i += 1

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for line in data:
        row = []
        row += [line[0]] # household id

        writer.writerow(row)
                
'''
#'''       
# this section extracts the day info
rawData = '../../Documents/UKDA-5340-tab/tab/dayeul2015.tab'
outfile = '../../Documents/UKDA-5340-tab/csv/days.csv'


data = []
with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    for row in reader:
        data.append(row)

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    i = 0
    for line in data:
        row = []
        row += [line[0]] # survey year
        row += [line[1]] # day ID
        if i == 0:
            row += ['HouseholdDayID']
        else:
            row += [str(10*int(line[3])+int(line[6]))]

        row += [line[2]] # individual ID
        row += [line[3]] # household ID
        row += [line[5]] # person number
        row += [line[6]] # travel day
        row += [line[8]] # day of week

        i += 1
        writer.writerow(row)


#'''   
