import csv


trips9 = '../../Documents/NHTS/2009/DAYV2PUB.csv'
trips17 = '../../Documents/NHTS/2017/trippub.csv'
households9 = '../../Documents/NHTS/2009/HHV2PUB.csv'
households17 = '../../Documents/NHTS/2017/hhpub.csv'

outfile = '../../Documents/NHTS/constance/texas-hh.csv'
outfile2 = '../../Documents/NHTS/constance/texas-trips.csv'

# OK I'm Just going to ook for total distance by vehicle over the day 

# The below is for checking that the extraction has worked
'''
with open(outfile2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
#'''
        
hhs = {}
with open(households17,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[25] != 'TX':
            continue
        householdID = row[0]
        weekday = int(row[1])
        year = row[30][:4]
        month = int(row[30][4:6])
        
        hhs[householdID] = [weekday,month,year]

with open(households9,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[13] != 'TX':
            continue
        householdID = row[0]
        weekday = int(row[24])
        year = row[29][:4]
        month = int(row[29][4:6])
        
        hhs[householdID] = [weekday,month,year]

print(len(hhs))

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for hh in hhs:
        writer.writerow([hh]+hhs[hh])

trips = []
with open(trips17,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] not in hhs:
            continue
        hhID = row[0]
        if row[10] in ['-1','-9']:
            continue
        vID = hhID+row[10]
        try:
            start = int(row[3][:2])*60+int(row[3][2:])
            end = int(row[4][:2])*60+int(row[4][2:])
            distance = float(row[6])
        except:
            continue

        dates = hhs[hhID]
        purp = row[58]

        trips.append([vID,hhID]+dates+[start,end,distance,purp])
       
        
with open(trips9,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] not in hhs:
            continue
        
        householdID = row[0]
        vehType = row[-3]

        distance = row[-16] # miles

        if vehType not in ['01','02','03','04','05','06']: # ignoring bikes golf carts
            continue

        if distance == '-1':
            continue

        try:
            start = int(int(row[57][0:2])*60+int(row[57][2:]))
            end = int(int(row[40][0:2])*60+int(row[40][2:])) 
        except:
            continue
        vehicleID  = householdID+row[-29]
        purp = row[-26]

        dates = hhs[householdID]

        trips.append([vehicleID,householdID]+dates+[start,end,distance,purp])


with open(outfile2,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['vehicleID','householdID','weekday','month','year',
                     'start','end','distance','purpose'])
    for row in trips:
        writer.writerow(row)
