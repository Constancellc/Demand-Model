import csv

meanValues = {'energyConsumed':0.0, 'initialSOC':0.0, 'finalSOC':0.0,
              'chargesPerDay':0.0, 'tripsPerDay':0.0, 'tripLength':0.0}
maxValues = {'energyConsumed':0.0, 'initialSOC':0.0, 'finalSOC':0.0,
              'chargesPerDay':0.0, 'tripsPerDay':0.0, 'tripLength':0.0}
minValues = {'energyConsumed':0.0, 'initialSOC':0.0, 'finalSOC':0.0,
              'chargesPerDay':0.0, 'tripsPerDay':0.0, 'tripLength':0.0}

fieldnames = ['ID','energyConsumed','initialSOC','finalSOC','chargesPerDay',
              'tripsPerDay','tripLength']

with open('MEAaverages.csv','rU') as csvfile:
    c = 0
    reader = csv.DictReader(csvfile)
    for row in reader:
        c += 1
        for field in fieldnames:
            if field == 'ID':
                continue
            meanValues[field] += float(row[field])
            if c == 1:
                maxValues[field] = float(row[field])
                minValues[field] = float(row[field])
            else:
                if maxValues[field] < float(row[field]):
                    maxValues[field] = float(row[field])
                if minValues[field] > float(row[field]):
                    minValues[field] = float(row[field])

results = {}

for field in fieldnames:
    results[field] = []
    
with open('MEAaverages.csv','rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        results['ID'].append(row['ID'])
        for field in fieldnames:
            if field == 'ID':
                continue
            results[field].append((float(row[field])-(meanValues[field]/c))/
                                  (0.5*(maxValues[field]-minValues[field])))

with open('scaledAverages.csv','w') as csvfile:
    dw = csv.DictWriter(csvfile,fieldnames=fieldnames)
    dw.writeheader()
    for i in range(0,len(results['ID'])):
        row = {}
        for field in fieldnames:
            row[field] = results[field][i]
        dw.writerow(row)

