import csv

# this is going to redefine a trip file containing only info i need

stages = '../../Documents/UKDA-5340-tab/tab/stageeul2015.tab'
outfile = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

#dates = {}
numPeople = {}
with open(stages,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    reader.next()
    for row in reader:
        tripID = row[2]
        try:
            passengers = int(row[20])
        except:
            continue
            

        if tripID not in numPeople:
            numPeople[tripID] = passengers

data = []

with open(outfile,'rU') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        if i == 0:
            data.append(row+['NumParty'])
        else:
            try:
                passengers = str(numPeople[row[0]])
            except:
                passengers = 'unknown'
            data.append(row+[passengers])
        i += 1

with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row)
        
    
