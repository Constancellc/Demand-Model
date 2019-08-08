import numpy as np
import matplotlib.pyplot as plt
import csv
import copy

file = '../../Documents/UKDA-7553-tab/constance/hh-loc.csv'
file2 = '../../Documents/census/dwellingType-MSOA.csv'

m2l = {}
file3 = '../../Documents/census/Output_Area_to_Lower_Layer_Super_Output_Area_to_Middle_Layer_Super_Output_Area_to_Local_Authority_District_December_2017_Lookup_in_Great_Britain__Classification_Version_2.csv'
with open(file3,'rU',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        msoa = row[7]
        la = row[9]
        m2l[msoa] = la

LAs = {}
with open(file,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        la = row[2]
        if la not in LAs:
            LAs[la] = 1
        else:
            LAs[la] += 1

LAs2 = {}
with open(file2,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    for row in reader:
        if len(row) < 2:
            continue
        m = row[0][:9]
        try:
            la = m2l[m]
        except:
            continue
        if la not in LAs:
            continue
        if la not in LAs2:
            LAs2[la] = 0
        LAs2[la] += float(row[1])

sf = {}
for la in LAs2:
    sf[la] = LAs2[la]/LAs[la]
    print(sf[la])
        
            
