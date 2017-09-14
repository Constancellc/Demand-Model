import csv


trips = '../../Documents/NHTS/DAYV2PUB.csv'
households = '../../Documents/NHTS/HHV2PUB.csv'

outfile = '../../Documents/NHTS/constance/trips_useful.csv'
outfile2 = '../../Documents/NHTS/constance/households_useful.csv'

# The below is for checking that the extraction has worked
'''
with open(outfile,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
'''
        
surveyTimes = {}
HHinfo = {}

with open(households,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        householdID = row[0]

        weekday = row[24]
        year = row[29][:4]
        month = int(row[29][4:6])

        nPeople = int(row[12])
        CENSUS_D = row[5]
        CENSUS_R = row[6]
        state = row[13]
        rururb = row[27]

        HHinfo[householdID] = [nPeople,CENSUS_D,CENSUS_R,state,weekday,month,rururb]
        
        surveyTimes[householdID] = [weekday,month,year]

with open(outfile2,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['householdID','numResidents','CENSUS_D','CENSUS_R',
                     'state','day','month','rurUrb'])
    for HH in HHinfo:
        writer.writerow([HH]+HHinfo[HH])

with open(outfile,'w') as csvout:
    writer = csv.writer(csvout)
    writer.writerow(['vehicleID','householdID','individualID','rural/urban',
                     'regionType','startTime (mins past 0:00)',
                     'endTime (mins past 0:00)','weekday','month','year',
                     'distance (miles)','numPassengers','purposeTo'])
                    
    with open(trips,'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            
            vehType = row[-3]

            distance = row[-16] # miles

            if vehType != '01': # only cars
                continue

            if distance == '-1':
                continue

            try:
                start = int(int(row[57][0:2])*60+int(row[57][2:]))      
                end = int(int(row[40][0:2])*60+int(row[40][2:])) 
            except:
                continue
            
            householdID = row[0]
            individualID = row[1]
            vehicleID  = householdID+row[-29]
            regionType = int(row[-32])
            purposeTo = row[-26]

            numPassengers = row[50]
            purpose = row[32]
            regionType2 = row[-12] # C = Second City, S = Surburban, TC = Town and Country, U = Urban

            [weekday,month,year] = surveyTimes[householdID]

            writer.writerow([vehicleID,householdID,individualID,regionType,
                             regionType2,start,end,weekday,month,year,distance,
                             numPassengers])
