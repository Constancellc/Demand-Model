import csv
import random

trips = '../../Documents/UKDA-5340-tab/tab/tripeul2016.tab'
stages = '../../Documents/UKDA-5340-tab/tab/stageeul2016r.tab'
households = '../../Documents/UKDA-5340-tab/tab/householdeul2016.tab'
outfile = '../../Documents/UKDA-5340-tab/constance-trips.csv'
outfile2 = '../../Documents/UKDA-5340-tab/constance-households.csv'


months = {} 
rType = {}
startDay = {}
region = {}
size = {}
year = {}
with open(households, 'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    next(reader)
    for row in reader:
        months[row[1]] = row[10]
        try:
            rType[row[1]] = int(row[161])
        except: # 2016 didn't record these classifications so we must be sneaky
            if row[154] == '1':
                if random.random() <= 0.452768:
                    rType[row[1]] = 1
                else:
                    rType[row[1]] = 2
            elif row[154] == '2':
                if random.random() <= 0.497303:
                    rType[row[1]] = 3
                else:
                    rType[row[1]] = 4
            else:
                continue
            
        region[row[1]] = row[29]
        startDay[row[1]] = int(row[14])
        size[row[1]] = row[34]
        year[row[1]] = row[0]

with open(outfile2,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['HouseholdID','Month','RegionType','Region','NumPeople',
                     'Year'])
    for hh in size:
        writer.writerow([hh,months[hh],rType[hh],region[hh],size[hh],year[hh]])
        
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
        dayNo = int(line[13]) + startDay[line[4]]-1
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

