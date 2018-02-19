import csv


# This section extracts the trip data
#'''

trips = '../../Documents/UKDA-5340-tab/tab/tripeul2016.tab'
stages = '../../Documents/UKDA-5340-tab/tab/stageeul2016r.tab'
households = '../../Documents/UKDA-5340-tab/tab/householdeul2016.tab'
outfile = '../../Documents/UKDA-5340-tab/constance-trips.csv'


months = {} 
rType = {}
startDay = {}
region = {}
with open(households, 'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    next(reader)
    for row in reader:
        months[row[1]] = row[10]
        rType[row[1]] = row[161]
        region[row[1]] = row[29]
        startDay[row[1]] = int(row[14])
        
        
vehicleIDs = {}
numPeople =  {}
with open(stages,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    next(reader)
    for row in reader:
        tripID = row[2]
        vehicleID = row[7]

        try:
            people = int(row[24])
        except:
            people = 1

        if tripID not in vehicleIDs:
            vehicleIDs[tripID] = vehicleID
            
        if tripID not in numPeople:
            numPeople[tripID] = people
            
data = []
with open(trips,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    for row in reader:
        if row[20] != '5': # if trip by car
            continue
        data.append(row)
        

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['TripID','HouseholdID','VehicleID','PersNo','RegionType',
                     'Region','Weekday','Month','Year','TripStart','TripEnd',
                     'TripDistance','PurpFrom','PurpTo','NumParty'])
    for line in data:
        row = []
        row += [line[0]] # trip id
        row += [line[4]] # household id
        row += [vehicleIDs[line[0]]] # vehicle ID 
        row += [line[12]] # person number in household
        row += [rType[line[4]]] # region type
        row += [region[line[4]]] # region
        dayNo = int(line[7]) + startDay[line[4]]
        if dayNo > 7:
            dayNo -= 7
        row += [str(dayNo)] # week day
        row += [months[line[4]]] # month
        row += [line[1]] # survey year
        row += [line[34]] # trip start - minutes past midnight
        row += [line[39]] # trip end - minutes past midnight
        row += [line[26]] # trip distance - miles
        row += [line[30]] # trip purpose from
        row += [line[31]] # trip purpose to
        row += [numPeople[line[0]]]

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
'''       
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
            row += ['ConstanceDayID']
        else:
            row += [str(10*int(line[3])+int(line[6]))]

        row += [line[2]] # individual ID
        row += [line[3]] # household ID
        row += [line[5]] # person number
        row += [line[6]] # travel day
        row += [line[8]] # day of week

        i += 1
        writer.writerow(row)


'''   
