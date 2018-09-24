import csv

data = '../../Documents/UKDA-5340-tab/constance-trips.csv'

with open(data,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
