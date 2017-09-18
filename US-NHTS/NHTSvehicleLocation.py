# packages
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

# these are the csv files containing the data
# households = '../../Documents/UKDA-5340-tab/tab/householdeul2015.tab'
trips = '../../Documents/NHTS/constance/trips_useful.csv'
households = '../../Documents/NHTS/constance/households_useful.csv'

class LocationPrediction:

    def __init__(self,day,month=None, state=None, regionD=None, regionR=None,
                 rurUrb=None):

        self.day = day
        self.month = month
        self.rurUrb = rurUrb
        self.regionR = regionR
        self.regionD = regionD
        self.state = state

        if state is not None:
            self.regS = {}

        if regionD is not None:
            self.regD = {}

        if regionR is not None:
            self.regR = {}

        if rurUrb is not None:
            self.regRU = {}

        # setting up counters which will be used to scale predictions
        self.nVehicles = 0

        self.tripLog = {}

        if (regionD is not None) or (regionR is not None) or (state is not None) or (rurUrb is not None):

            with open(households,'rU') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                        
                    if month is not None:
                        if int(row[6]) != int(month):# skip households from the wrong month
                            continue

                    if day is not None: # and the wrong day
                        if int(row[5]) != int(day):
                            continue

                    if state is not None:
                        if row[0] not in self.regS:
                            self.regS[row[0]] = row[4]

                    if regionD is not None:
                        self.regD[row[0]] = row[2]

                    if regionR is not None:
                        self.regR[row[0]] = row[3]

                    if rurUrb is not None:
                        self.regRU[row[0]] = row[7]
            
        with open(trips,'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                
                if int(row[7]) != int(self.day):
                    continue
                
                if month is not None:
                    if int(row[8]) != int(self.month):
                        continue

                if self.rurUrb is not None:
                    if int(row[3]) != int(self.rurUrb):
                        continue

                if self.state is not None:
                    if self.regS[row[1]] != self.state:
                        continue

                if self.regionR is not None:
                    if self.regR[row[1]] != self.regionR:
                        continue

                if self.regionD is not None:
                    if self.regD[row[1]] != self.regionD:
                        continue

                vehicle = row[0]

                if vehicle == ' ': # skip trips where the vehicle is missing
                    continue

                if vehicle not in self.tripLog:
                    self.tripLog[vehicle] = []
                    self.nVehicles += 1

                try:
                    tripStart = int(row[5])
                    tripEnd = int(row[6])
                    tripPurpose = int(row[12])

                    if tripPurpose > 40 and tripPurpose < 50:
                        tripPurpose = 40 # combine all shopping

                    if tripPurpose > 10 and tripPurpose < 20:
                        tripPurpose = 10

                
                except:
                    print(row)
                    if self.tripLog[vehicle] == []:
                        del self.tripLog[vehicle]
                        self.nVehicles -= 1
                    continue


                self.tripLog[vehicle].append([tripStart,tripEnd,str(tripPurpose)])

        # now sort all triplogs chronologically
        for vehicle in self.tripLog:
            self.tripLog[vehicle] = sorted(self.tripLog[vehicle])

    def getVehicleLocations(self,showTransit=False):
        locations = {}
        
        locations['1'] = [0]*60*24 # home
        locations['10'] = [0]*60*24 # work
        locations['40'] = [0]*60*24 # shop
        locations['-'] = [0]*60*24 # other
        locations['0'] = [0]*60*24 # in transit

        for vehicle in self.tripLog:
            log = self.tripLog[vehicle]
            
            i = 0

            # assume starts at home
            while i < log[0][0]:
                locations['1'][i] += 1
                i += 1

            while len(log) > 1:
                for j in range(log[0][0],log[0][1]):

                    if i >= 1440:
                        continue
                    
                    try:
                        locations['0'][i] += 1
                    except:
                        print(i)
                    i += 1

                while i < log[1][0] and i < 1440:
                    if log[0][2] not in locations:
                        locations['-'][i] += 1
                    else:
                        locations[log[0][2]][i] += 1
                    i += 1
                    
                log = log[1:] # remove journey from log

                    
            # now on last journey

            if log[0][1] < 1440:
                for j in range(log[0][0],log[0][1]):
                    try:
                        locations['0'][i] += 1
                    except:
                        print(i,end='  ')
                        print(j)
                    i += 1
                    #print(i,end=' ')
                    #print(j)
                while i < 1440:
                    if log[0][2] not in locations:
                        locations['-'][i] += 1
                    else:
                        locations[log[0][2]][i] += 1
                    i += 1
            else:
                for j in range(log[0][0],1440):
                    locations['0'][i] += 1
                    i += 1

                for j in range(0,log[0][1]):
                    locations['0'][j] += 1
                    locations['1'][j] -= 1

                    # finsih later

        newLocations = {}
        
        # normalise
        for l in locations:
            newLocations[l] = [0.0]*48
            for i in range(0,1440):
                locations[l][i] = locations[l][i]/self.nVehicles
                newLocations[l][int(i/30)] += locations[l][i]/30

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
                
        
