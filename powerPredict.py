# install matplot

import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# CLASS DEFINITIONS SECTION

class Day:
    def __init__(self, n):
        self.usage = [0.0] * n
        self.chargin = [0.0] * n
        
class Month:
    def __init__(self, n):
        self.mon = Day(n)
        self.tue = Day(n)
        self.wed = Day(n)
        self.thu = Day(n)
        self.fri = Day(n)
        self.sat = Day(n)
        self.sun = Day(n)

class Region:
    def __init__(self, n):
        self.jan = Month(n)
        self.feb = Month(n)
        self.mar = Month(n)
        self.apr = Month(n)
        self.may = Month(n)
        self.jun = Month(n)
        self.jul = Month(n)
        self.aug = Month(n)
        self.sep = Month(n)
        self.oct = Month(n)
        self.nov = Month(n)
        self.dec = Month(n)

class Vehicle:
    def __init__(self,mass,Ta,Tb,Tc,eff):
        self.mass = mass
        self.Ta = Ta
        self.Tb = Tb
        self.Tc = Tc
        self.eff = eff
        
class Journey:
    def __init__(self):
        self.purpose = ''
        self.month = ''
        self.day = ''
        self.hour = ''
        self.regionType = ''
        self.region = ''
        
        
NE = Region(100)
NE.jan.tue.usage[4] = 0.0005
#plt.plot(NE.jan.tue.usage)
#plt.show()

# Ok, let's forget classes for now and just go free style with the sampling
array = []
        
with open('FINALpurposeMonth.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    months = next(reader)
    purposes = []
    for row in reader:
        if row == months:
            continue
        else:
            purposes.append(row[0])
            array.append(row[1:])
            
    months.remove('')


# now let sample
ran = random.random()

cdf = []
counter = 0
for i in range(0,7):
    for j in range(0,12):
        counter += float(array[i][j])
        cdf.append(counter)

normalised = []
for number in cdf:
    normalised.append(number/cdf[83])
cdf = normalised

ran = random.random()
i = 0
while cdf[i]<=ran and i < 83:
    i = i+1

c = i%12
r = (i-c)/12

journey = Journey()
journey.month = months[c]
journey.purpose = purposes[r]

with open('FINALregionTypePurpose.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    regionTypes = next(reader)
    regionTypes.remove("")
    for row in reader:
        if row[0] == journey.purpose():
            pdf = row[1:]

c = 0
for value in pdf:
    c += float(value)

normalised = []
for value in pdf:
    normalised.append(value/c)

pdf = normalised
cdf = []

for value in pdf:
    c += float(value)
    cdf.append(c)

ran = random.random()
i = 0
while cdf[i]<=ran and i < 4:
    i = i+1

journey.regionType = regionTypes[i]
