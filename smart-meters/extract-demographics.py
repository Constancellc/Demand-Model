import csv
import datetime
import matplotlib.pyplot as plt
from xlrd import open_workbook

months = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,
          'SEP':9,'OCT':10,'NOV':11,'DEC':12}

outfile = '../../Documents/sharonb/7591/csv/demographics.csv'
data = '../../Documents/sharonb/7591/csv/edrp_geography_data.xlsx'

demogs = []
wb = open_workbook(data)
for s in wb.sheets():
    for row in range(1,s.nrows):
        anonID = s.cell(row,0).value
        if anonID == 'anonID':
            continue
        ACORN1 = s.cell(row,3).value
        ACORN2 = s.cell(row,4).value
        ACORN3 = s.cell(row,5).value
        NUTS1 = s.cell(row,10).value
        
        demogs.append([anonID,ACORN1,ACORN2,ACORN3,NUTS1])
        
with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID','ACORN Category','ACORN Group','ACORN Type',
                     'NUTS1'])
    for row in demogs:
        writer.writerow(row)
