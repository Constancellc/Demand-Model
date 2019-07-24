import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv


stem = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'
stem2 = '../../../Documents/census/'
data = '../../../Documents/elec_demand/MSOA_domestic_electricity_2016.csv'

data2 = '../../../Documents/elec_demand/LSOA_domestic_electricity_2016.csv'


ruType = {}
with open(stem2+'LA_rural_urban.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        ruType[row[0]] = int(row[1])

e7 = {}
with open(stem2+'e7.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        e7[row[0]] = float(row[1])

with open(stem2+'ADMD.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LA Code','Max kW'])
    for la in ruType:
        if ruType[la] == 1:
            if e7[la] > 0.2:
                admd = 500*0.95
            else:
                admd = 315*0.95
        elif ruType[la] == 2:
            if e7[la] > 0.2:
                admd = 500*0.95
            else:
                admd = 315*0.95
        elif ruType[la] == 3:
            if e7[la] > 0.2:
                admd = 800*0.95
            else:
                admd = 800*0.95
                
        writer.writerow([la,admd])
