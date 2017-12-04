import csv
import datetime
import random
import matplotlib.pyplot as plt

months = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,
          'SEP':9,'OCT':10,'NOV':11,'DEC':12}

data = '../../Documents/sharonb/7591/csv/profiles.csv'


class HouseholdElectricityDemand:

    def __init__(self,region=None,regionType=None,ACORNCategory=None,
                 ACORNGroup=None,ACORNType=None):

        self.region = region
        self.regionType = regionType
        self.ACORNCategory = ACORNCategory
        self.ACORNGroup = ACORNGroup
        self.ACORNType = ACORNType

        
        NUTS = {'1':'UKC','2':'UKD','3':'UKE','4':'UKF','5':'UKG','6':'UKH',
                '7':'UKI','8':'UKJ','9':'UKK','10':'UKL','11':'UKM'}
        Types = {'R':['1.0','5.0','10.0','21.0','22.0','23.0','41.0']}
                 #'U':[2,7,8,9,11,14,15,16,17,20,24,25,26,27,28,29,34,35,36,37,38]}
        self.hh = []

        self.valid = []
        with open('../../Documents/sharonb/7591/csv/dates.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.valid.append(row[0]) 

        with open('../../Documents/sharonb/7591/csv/demographics.csv') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:

                if region != None:
                    # 1:NE, 2:NW, 3:Y+H, 4:EM, 5:WM, 6:E, 7:L, 8:SE, 9:SW,
                    # 10: Wales, 11: Scotland
                    if row[4] != NUTS[region]:
                        continue

                if regionType != None:
                    # 1:uc, 2:ut, 3:rt, 4:rv, 5:scotland
                    if regionType in ['1','2']:
                        if row[3] in Types['R']:
                            continue
                    else:
                        if row[3] not in Types['R']:
                            continue

                if self.ACORNCategory != None:
                    if row[1] != ACORNCategory:
                        continue
                    
                if self.ACORNGroup != None:
                    if row[2] != ACORNGroup:
                        continue

                if self.ACORNType != None:
                    if row[3] != ACORNType:
                        continue

                if str(int(float(row[0]))) not in self.valid:
                    continue

                self.hh.append(str(int(float(row[0]))))
                    
    def getProfile(self,startDay,startMonth,nProfiles=1,nDays=1):

        # startDay - int

        # NOTE: doesn't actually work for number of days != 1 yet

        # first randomly choose households
        chosen = []
        profiles = []

        if nProfiles > len(self.hh):
            chosen = self.hh
            print('changing number of profiles from '+str(nProfiles)+' to '+
                  str(len(self.hh)))
            nProfiles = len(self.hh)

        else:
            while len(chosen) < nProfiles:
                i = int(len(self.hh)*random.random())
                if self.hh[i] not in chosen:
                    chosen.append(self.hh[i])

        # then identify its possible dates
        starts = {}
        lens = {}
        with open('../../Documents/sharonb/7591/csv/dates.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] in chosen:
                    starts[row[0]] = datetime.datetime(int(row[1][:4]),
                                                       int(row[1][5:7]),
                                                       int(row[1][8:10]))
                    lens[row[0]] = int(row[2])

        possDays = {}
        for h in chosen:
            possDays[h] = []
            day = starts[h]

            for i in range(0,lens[h]):
                if day.isoweekday() == startDay and day.month == startMonth:
                    possDays[h].append(i)
                day += datetime.timedelta(1)

            #possDays[h] = possDays[h][1:len(possDays[h])-2]
        invalid = []
        
        for h in chosen:
            if len(possDays[h]) == 0:
                invalid.append(h)

        # randomly pick one of them
        chosenDay = {}
        for h in chosen:
            if h in invalid:
                continue
            ran = int(random.random()*len(possDays[h]))
            try:
                chosenDay[h] = possDays[h][ran]
            except:
                print(h)
                print(ran)
                print(len(possDays[h]))
           
        # return that profile
        with open(data,'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] not in chosen: # correct household?
                    continue
                if row[0] in invalid:
                    continue
                
                if int(row[1]) != chosenDay[row[0]]: # correct day?
                    continue

                p = row[2:50]
                for i in range(0,len(p)):
                    p[i] = float(p[i])

                if sum(p) != 0:
                    profiles.append(p)
                
        return profiles


