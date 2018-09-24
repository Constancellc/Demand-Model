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
        

        
with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['HouseholdID','Ward','Local Authority','UA','County',
                     'Country'])
    for hh in country:
        try:
            writer.writerow([hh,ward[hh],LA[hh],UA[hh],county[hh],country[hh]])
        except:
            continue
