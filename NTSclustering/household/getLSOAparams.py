import csv
import matplotlib.pyplot as plt
import random
import numpy as np

cens = '../../../Documents/census/'
stem = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'

nCars = {}
with open(cens+'cars-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3:
            continue
        try:
            a = float(row[2])
        except:
            continue
        
        lsoa = row[1]

        avCars = (float(row[3])+float(row[4])*2+float(row[5])*3+float(row[6])*4)\
                 /(float(row[2])+float(row[3])+float(row[4])+float(row[5])+
                   float(row[6]))
        nCars[lsoa] = avCars

driveToWork = {}
with open(cens+'methodToWork-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3:
            continue
        try:
            a = float(row[2])
        except:
            continue
        
        lsoa = row[1]

        per = round((float(row[3])+float(row[4]))/float(row[2]),2)
        driveToWork[lsoa] = per

distToWork = {}
with open(cens+'distToWork-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3:
            continue
        try:
            a = float(row[2])
        except:
            continue
        
        lsoa = row[1]
        distToWork[lsoa] = round(0.621371*float(row[3])/float(row[2]),2)

pop = {}
with open(cens+'population-LSOA.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
