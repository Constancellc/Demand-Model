# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

# these are the csv files containing the data
# households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/csv/tripsUseful.csv'

class LocationPrediction:

    def __init__(self,day,month=None,regionType=None,region=None):

        self.dayb4 = str(int(day)-1)
        if self.dayb4 == '0':
            self.dayb4 = '7'
        self.day = day
        self.month = month
        self.regionType = regionType
        self.region = region

        # setting up counters which will be used to scale predictions
        self.nVehicles = 0

        self.tripLog = {}
        
        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            for row in reader:

                
                if month is not None:
                    if row[6] != self.month:
                        continue

                if self.regionType is not None:
                    if self.reg2[row[1]] != self.regionType:
                        continue

                if self.region is not None:
                    if self.reg3[row[1]] != self.region:
                        continue

                vehicle = row[2]

                if vehicle == ' ': # skip trips where the vehicle is missing
                    continue

                if vehicle not in self.tripLog:
                    self.tripLog[vehicle] = []
                    self.nVehicles += 1

                if row[5] == self.day:
                    dayNo = 1
                elif row[5] == self.dayb4:
                    dayNo = 0
                else:
                    continue

                try:
                    tripStart = int(row[8])+1440*dayNo
                    tripEnd = int(row[9])+1440*dayNo
                    tripPurpose = row[12]

                except:
                    if self.tripLog[vehicle] == []:
                        del self.tripLog[vehicle]
                        self.nVehicles -= 1
                    continue

                self.tripLog[vehicle].append([tripStart,tripEnd,tripPurpose])

        # now sort all triplogs chronologically
        for vehicle in self.tripLog:
            self.tripLog[vehicle] = sorted(self.tripLog[vehicle])

    def getVehicleLocations(self,showTransit=False):
        locations = {}
        
        locations['23'] = [0]*60*48
        
        if showTransit == True:
            transit = [0]*60*48
            locations['0'] = [0]*60*48

        for vehicle in self.tripLog:
            # assume vehicle initially at home
            log = self.tripLog[vehicle]
            N = len(log)

            if N == 0:
                for i in range(0,48*60):
                    locations['23'][i] += 1
                continue
            
            for i in range(0,log[0][0]):
                locations['23'][i] += 1

            n = 0
            while n < N:
                if showTransit == True:
                    for i in range(log[n][0],log[n][1]):
                        if i < 48*60:
                            locations['0'][i] += 1

                purpose = log[n][2]
                if purpose not in locations:
                    locations[purpose] = [0]*60*48

                if n == N-1:
                    for i in range(log[n][1],48*60):
                        try:
                            locations[purpose][i] += 1
                        except:
                            print i
                            continue
                else:
                    for i in range(log[n][1],log[n+1][0]):
                        try:
                            locations[purpose][i] += 1
                        except:
                            continue

                n += 1

        for p in locations:
            for i in range(0,48*60):
                locations[p][i] = float(locations[p][i])/self.nVehicles

        newLocations = {}

        newLocations['home'] = locations['23']
        newLocations['work'] = locations['1']

        # combine the two types of shopping
        for i in range(0,48*60):
            locations['4'][i] += locations['5'][i]

        newLocations['shops'] = locations['4']

        if showTransit == True:
            newLocations['in transit'] = locations['0']

        return newLocations

    def getPAvaliableToCharge(self,smooth=True):

        nActiveVehicles = 0
        p = [0.0]*48*60

        for vehicle in self.tripLog:
            log = self.tripLog[vehicle]

            N = len(log)

            if N == 0:
                continue

            nActiveVehicles += 1

            n = 0

            while n < N-1:
                if log[n][2] != '23':
                    n += 1
                else:
                    for i in range(log[n][1],log[n+1][0]):
                        p[i] += 1.0
                    n += 1

            if log[N-1][2] != '23':
                continue
            for i in range(log[N-1][1],len(p)):
                p[i] += 1.0

        # and normalise
        for i in range(0,48*60):
            p[i] = p[i]/nActiveVehicles

        # lose first 24 hours
        #p = p[24*60:]

        if smooth == True:
            p_downsample = [0.0]*2*24
            i = 0
            

        return p
                
        
