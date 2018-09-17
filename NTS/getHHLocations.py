import csv
import random


ind = '../../Documents/UKDA-7553-tab/tab/individualspecial2016_protect.tab'
households = '../../Documents/UKDA-7553-tab/tab/householdspecial2016_protect.tab'
outfile = '../../Documents/UKDA-7553-tab/constance/hh-loc.csv'


country = {} 
county = {}
UA = {}
LA = {}
ward = {}
with open(households, 'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    next(reader)
    for row in reader:
        country[row[1]] = row[42]
        county[row[1]] = row[43]
        UA[row[1]] = row[44]
        LA[row[1]] = row[139]
        ward[row[1]] = row[137]
        
hh = {}
with open(ind,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    next(reader)
    for row in reader:
        if row[4] in hh:
            continue
        hh[row[4]] = row[2]
        
with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['VehicleID','Ward','Local Authority','UA','County',
                     'Country'])
    for v in hh:
        try:
            writer.writerow([v,ward[hh[v]],LA[hh[v]],UA[hh[v]],county[hh[v]],
                             country[hh[v]]])
        except:
            continue
