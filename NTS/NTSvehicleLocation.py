# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

# these are the csv files containing the data
# households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/UKDA-5340-tab/constance-trips.csv'
households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'

class LocationPrediction:

    def __init__(self,day,month=None,regionType=None,region=None):

        self.dayb4 = str(int(day)-1)
        if self.dayb4 == '0':
            self.dayb4 = '7'
        self.day = day
        self.month = month
        self.regionType = regionType
        self.region = region

        if regionType is not None or region is not None:
            self.reg2 = {} # 1:uc, 2:ut, 3:rt, 4:rv, 5:scotland

            self.reg3 = {} # 1:NE, 2:NW, 3:Y+H, 4:EM, 5:WM, 6:E, 7:L, 8:SE, 9:SW,
                      # 10: Wales, 11: Scotland
                      
        # setting up counters which will be used to scale predictions
        self.nVehicles = 0

        self.tripLog = {}

        if regionType is not None or region is not None:

            with open(households,'rU') as csvfile:
                reader = csv.reader(csvfile,delimiter='\t')
                next(reader)
                for row in reader:

                    if month is not None:
                        if row[9] != month:
                            continue

                    if row[0] not in self.reg2:
                        self.reg2[row[0]] = row[149]
                        self.reg3[row[0]] = row[28]
        
        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                
                if month is not None:
                    if row[6] != self.month:
                        continue
                    
                if regionType is not None:                   
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
                    tripStart = int(row[9])+1440*dayNo
                    tripEnd = int(row[10])+1440*dayNo
                    tripPurpose = row[13]

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
                            print(i)
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

        newLocations['home'] = locations['23'][24*60:]
        newLocations['work'] = locations['1'][24*60:]

        # combine the two types of shopping
        for i in range(0,48*60):
            locations['4'][i] += locations['5'][i]

        newLocations['shops'] = locations['4'][24*60:]

        if showTransit == True:
            newLocations['in transit'] = locations['0'][24*60:]

        return newLocations

    def getPHome(self,nHours,pointsPerHour):

        locations = self.getVehicleLocations()

        home = locations['home']
        
        if nHours > 24 and nHours < 48:
            home += home[:(nHours-24)*60]
        elif nHours > 48:
            for i in range(0,(nHours-24)/24):
                home += home
            home += home[:((nHours-24)%24)*60]

        # now downsample

        newHome = []

        for i in range(0,nHours*pointsPerHour):
            av = 0.0

            for j in range(0,60/pointsPerHour):
                av += float(home[(i*60/pointsPerHour)+j])

            newHome.append(av/(60/pointsPerHour))

        return newHome

    def getPFinished(self,nHours,pointsPerHour,deadline=9):
        tripEnds = [0]*48*60
        for vehicle in self.tripLog:
            log = self.tripLog[vehicle]

            if log == []:
                continue

            if log[-1][2] == '23':
                finalTripEnd = log[-1][1]-24*60

                if finalTripEnd < 0: # no trips on day concerned
                    continue

            else:
                continue
            
            for i in range(finalTripEnd,48*60):
                tripEnds[i] += 1

        # deadline day 1 - deadline day 2
        tripEnds = tripEnds[deadline*60:(deadline+24)*60]

        # and shift so midnight to midnight
        tripEnds = tripEnds[(24-deadline)*60:] + tripEnds[:(24-deadline)*60]

        # make right length
        if nHours > 24 and nHours < 48:
            tripEnds += tripEnds[:(nHours-24)*60]
        elif nHours > 48:
            for i in range(0,(nHours-24)/24):
                tripEnds += tripEnds
            tripEnds += tripEnds[:((nHours-24)%24)*60]

        # now downsample
        newP = []

        for i in range(0,int(nHours*pointsPerHour)):
            av = 0.0

            for j in range(0,int(60/pointsPerHour)):
                av += float(tripEnds[int((i*60/pointsPerHour)+j)])

            newP.append(av/(60/pointsPerHour))

        
        # and nornalise
        p = []
        total = float(max(newP))#*(24/float(nHours))
        for i in range(0,int(nHours*pointsPerHour)):
            p.append(float(newP[i])/total)

        return p

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
                
        
