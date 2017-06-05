import csv

with open('../../Documents/My_Electric_avenue_Technical_Data/constance/charges2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print row
