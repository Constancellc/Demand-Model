import csv

rawData = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'

with open(rawData,'rU') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    i = 0
    for row in reader:
        if i < 1:
            print row
        i += 1
    
