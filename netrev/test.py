import numpy as np
import matplotlib.pyplot as plt
import random
import csv

# this contains half hourly data data
'''
base = '../../Documents/netrev/TC1a/TrialMonitoringDataHH.csv'

with open(base,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locID = row[0]
        dateTime = row[3] # e.g. 03/12/2011 00:00:00
        power = float(row[4])*2 # kWh pver half hour -> kWh
        
'''
# this contains half hourly data data

base = '../../Documents/netrev/TC1a/CustomerTestCellDefinition.csv'

with open(base,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        locID = row[0]
        inOut = row[3] # 1=In Northen Powergrid's region, 2= Out, 0=Undefined
        startDate = row[4] # e.g. 01/09/2010
        finDate = row[5]
        mosaicClass = row[7] # demographic class defined by experian (15 options)
        print(row)
