
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

from vehicleModel import Drivecycle

"""
THIS IS AN OVERARCHING PREDICTION FILE. IT WILL SIMULATE JOURNEYS RANDOMLY
DISTRIBUTED IN BOTH SPACE (REGIONS) AND TIME (MONTH, DAY ETC.)

THE RESULTS ARE SCALED TO REPRESENT THE POWER DEMAND PER PERSON DUE TO EV
DRIVING.
"""

# ------------------------------------------------------------------------------
# CLASS DEFINITIONS SECTION
# ------------------------------------------------------------------------------
class Vehicle:
    def __init__(self,mass,Ta,Tb,Tc,eff):
        self.mass = mass
        self.load = 0
        self.Ta = Ta
        self.Tb = Tb
        self.Tc = Tc
        self.eff = eff

    def loadEnergies(self):
        # first we're going to want to get the region specific lengths, then
        # scale the drive cycle and finally work out the energies
        energy = {'Urban Conurbation':{'Commute':0,'Education':0,'Business':0,
                               'Shopping':0,'Other escort + personal':0,
                               'Entertainment':0,'Other':0},
          'Urban City and Town':{'Commute':0,'Education':0,'Business':0,
                                 'Shopping':0,'Other escort + personal':0,
                                 'Entertainment':0,'Other':0},
          'Rural Town and Fringe':{'Commute':0,'Education':0,'Business':0,
                                   'Shopping':0,'Other escort + personal':0,
                                   'Entertainment':0,'Other':0},
          'Rural Village, Hamlet and Isolated Dwelling':{'Commute':0,
                                                         'Education':0,
                                                         'Business':0,
                                                         'Shopping':0,
                                                         'Other escort + personal':0,
                                                         'Entertainment':0,
                                                         'Other':0}}
        
        times = {'Urban Conurbation':{'Commute':0,'Education':0,'Business':0,
                               'Shopping':0,'Other escort + personal':0,
                               'Entertainment':0,'Other':0},
          'Urban City and Town':{'Commute':0,'Education':0,'Business':0,
                                 'Shopping':0,'Other escort + personal':0,
                                 'Entertainment':0,'Other':0},
          'Rural Town and Fringe':{'Commute':0,'Education':0,'Business':0,
                                   'Shopping':0,'Other escort + personal':0,
                                   'Entertainment':0,'Other':0},
          'Rural Village, Hamlet and Isolated Dwelling':{'Commute':0,
                                                         'Education':0,
                                                         'Business':0,
                                                         'Shopping':0,
                                                         'Other escort + personal':0,
                                                         'Entertainment':0,
                                                         'Other':0}}

        array = []
        
        with open('nts-data/regionTypePurposeLength.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array.append(row)

            regions = array[0]
            
            array = array[1:]

            passengers = {'Commute':0.2,'Education':1.1,'Business':0.25,
                          'Shopping':0.7,'Other escort + personal':0.4,
                          'Entertainment':0.75,'Other':0.8}
            for row in array:
                purpose = row[0]

                self.load = passengers[purpose]*60

                for i in range(1,len(regions)):
                    distance = float(row[i])*1609.34 # in m
                    if regions[i][0] == 'U':
                        cycle = Drivecycle(distance,'urban')
                    elif regions[i][0] == 'R':
                        cycle = Drivecycle(distance,'rural')
                    else:
                        raise Error('region not recognised')
                    v = cycle.velocity
                    a = cycle.acceleration

                    F = []
                    for value in v:
                        F.append(self.Ta + self.Tb*value + self.Tc*value*value)

                    for j in range(0,len(a)):
                        F[j] += (self.mass+self.load)*a[j]

                    E = 0
                    for j in range(0,len(a)):
                        if a[j] >= 0:
                            E += F[j]*v[j]/self.eff
                        else:
                            E += F[j]*v[j]*self.eff

                    energy[regions[i]][purpose] = E*2.77778e-7 # kWh
                    times[regions[i]][purpose] = float(len(v))/3600 # hours

        self.energy = energy
        self.times = times
        
class Region:
    def __init__(self, n):
        # n is the number of points per hour

        self.n = n
        n = n*24

        running = {'January':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'February':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'March':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'April':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'May':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'June':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'July':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'August':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'September':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'October':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'November':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'December':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},}

        charging = {'January':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'February':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'March':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'April':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'May':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'June':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'July':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'August':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'September':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'October':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'November':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},
                  'December':{'Monday':[0]*n,'Tuesday':[0]*n,'Wednesday':[0]*n,
                             'Thursday':[0]*n,'Friday':[0]*n,'Saturday':[0]*n,
                             'Sunday':[0]*n},}
        
        number = {'January':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'February':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'March':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'April':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'May':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'June':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'July':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'August':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'September':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'October':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'November':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0},
                  'December':{'Monday':0.0,'Tuesday':0.0,'Wednesday':0.0,
                             'Thursday':0.0,'Friday':0.0,'Saturday':0.0,
                             'Sunday':0.0}}

        self.running = running
        self.charging = charging
        self.number = number

    def plot(self,month):
        # hi
        days = ['Monday','Tuesday','Saturday']#'Wednesday','Thursday','Friday','Saturday',
                #'Sunday']
        
        x = np.linspace(0,24,num=24*self.n)

        figure = plt.figure(1)
        i = 1
        for day in days:
            fig.add_subplot(4,2,i)
            plt.plot(x,self.running[month][day])
            i += 1
        plt.show()
        
        print "you should probably finish this"

    def scale(self,value):

        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        months = ['January','February','March','April','May','June','July','August',
                  'September','October','November','December']
        
        for month in months:
            for day in days:

                if month in ['January', 'March', 'May', 'July', 'August', 'October',
                             'December']:
                    self.number[month][day] = self.number[month][day]/(value*31/7)
                    for j in range(0,len(self.charging[month][day])):
                        self.charging[month][day][j] = float(self.charging[month][day][j])/(value*31/7)
                        self.running[month][day][j] = float(self.running[month][day][j])/(value*31/7)
                    
                if month in ['April','June','September','November']:
                    self.number[month][day] = self.number[month][day]/(value*30/7)
                    for j in range(0,len(self.charging[month][day])):
                        self.charging[month][day][j] = float(self.charging[month][day][j])/(value*30/7)
                        self.running[month][day][j] = float(self.running[month][day][j])/(value*30/7)
                        
                if month == 'February':
                    self.number[month][day] = self.number[month][day]/(value*28/7)
                    for j in range(0,len(self.charging[month][day])):
                        self.charging[month][day][j] = float(self.charging[month][day][j])/(value*28/7)
                        self.running[month][day][j] = float(self.running[month][day][j])/(value*28/7)
                   
class Journey:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.purpose = ''
        self.month = ''
        self.day = ''
        self.hour = ''
        self.regionType = ''
        self.region = ''

    def generate(self):
        array = []
               
        with open('nts-data/purposeMonth.csv','rU') as csvfile:
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

        # now lets sample month and purpose
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

        self.month = months[c]
        self.purpose = purposes[r]


        # now sampling to find region day and start hour
        
        files = ['nts-data/regionTypePurpose.csv','nts-data/purposeDay.csv',
                 'nts-data/purposeStartHour.csv']
        out =  []

        for i in range(0,3):
            with open(files[i],'rU') as csvfile:
                pdf = []
                reader = csv.reader(csvfile)
                variables = next(reader)
                variables.remove("")
                for row in reader:
                    if row[0] == self.purpose:
                        pdf = row[1:]

            c = 0
            for value in pdf:
                c += float(value)

            normalised = []
            for value in pdf:
                normalised.append(float(value)/c)

            cdf = []
            c = 0

            for value in normalised:
                c += float(value)
                cdf.append(c)

            ran = random.random()
            i = 0
            while cdf[i]<=ran and i < len(variables):
                i = i+1

            out.append(variables[i])

        self.regionType = out[0]
        self.day = out[1]
        self.hour = str(int(out[2])-5)

    def addToDataset(self,regions):
        if self.region == '' and self.regionType == '':
            print 'help'
        else:
            # again, will need to come back to this
            e = self.vehicle.energy[self.regionType][self.purpose] 
            t = self.vehicle.times[self.regionType][self.purpose]

            n = len(regions[self.regionType].running['July']['Monday'])/24
            # n should be the number of points per hour

            l = int(t*n)

            offset = int(random.random()*(n+1))
            
            for i in range(0,l):
                j = int(n*float(self.hour)+i+offset)
                if j >= 24*n:
                    j -= 24*n
                regions[self.regionType].running[self.month][self.day][j] += e/t

            regions[self.regionType].number[self.month][self.day] += 1

# ------------------------------------------------------------------------------
# INITIALIZATION SECTION
# ------------------------------------------------------------------------------
fleet = [1]
nissanLeaf = Vehicle(1705,33.78,0.0618,0.02282,0.7)
nissanLeaf.loadEnergies()

vehicleFleet = {1.0:nissanLeaf}
pointsPerHour = 60

UC = Region(pointsPerHour)
UT = Region(pointsPerHour)
RT = Region(pointsPerHour)
RV = Region(pointsPerHour)
regions = {'Urban Conurbation':UC,'Urban City and Town':UT,
           'Rural Town and Fringe':RT,
           'Rural Village, Hamlet and Isolated Dwelling':RV}

populations = [12938,
13829,
2982,
2934] 
s = sum(populations)

scaledPopulations = []
for item in populations:
    si = float(item)/s
    scaledPopulations.append(si)


tripsPerPersonPerYear = int(590/1.6) # not sure about 1.6 - passengers vs drivers
numberResidents = 10000

numberJourneys = numberResidents*tripsPerPersonPerYear

#numberSimulatedJourneys = 100000

#print "PROGRESS:",
for i in range(0,numberJourneys):
    if i <= numberJourneys/fleet[0]:
        trip = Journey(nissanLeaf)
        trip.generate()
        trip.addToDataset(regions)
    # elif i <= numberJourneys/(fleet[0]+fleet[1])
    if i%(numberJourneys/10) == 0:
        print str(10*i/(numberJourneys/10))+"% COMPLETE"

UC.scale(numberResidents*scaledPopulations[0])
UT.scale(numberResidents*scaledPopulations[1])
RT.scale(numberResidents*scaledPopulations[2])
RV.scale(numberResidents*scaledPopulations[3])

days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
months = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']
regionz = [UC,UT,RT,RV]
#x = np.linspace(0,24,num=24*pointsPerHour)

uc = {'uk-wide/ucJAN.csv':'January','uk-wide/ucFEB.csv':'February',
      'uk-wide/ucMAR.csv':'March','uk-wide/ucAPR.csv':'April',
      'uk-wide/ucMAY.csv':'May','uk-wide/ucJUN.csv':'June',
      'uk-wide/ucJUL.csv':'July','uk-wide/ucAUG.csv':'August',
      'uk-wide/ucSEP.csv':'September','uk-wide/ucOCT.csv':'October',
      'uk-wide/ucNOV.csv':'November','uk-wide/ucDEC.csv':'December'}

ut = {'uk-wide/utJAN.csv':'January','uk-wide/utFEB.csv':'February',
      'uk-wide/utMAR.csv':'March','uk-wide/utAPR.csv':'April',
      'uk-wide/utMAY.csv':'May','uk-wide/utJUN.csv':'June',
      'uk-wide/utJUL.csv':'July','uk-wide/utAUG.csv':'August',
      'uk-wide/utSEP.csv':'September','uk-wide/utOCT.csv':'October',
      'uk-wide/utNOV.csv':'November','uk-wide/utDEC.csv':'December'}

rt = {'uk-wide/rtJAN.csv':'January','uk-wide/rtFEB.csv':'February',
      'uk-wide/rtMAR.csv':'March','uk-wide/rtAPR.csv':'April',
      'uk-wide/rtMAY.csv':'May','uk-wide/rtJUN.csv':'June',
      'uk-wide/rtJUL.csv':'July','uk-wide/rtAUG.csv':'August',
      'uk-wide/rtSEP.csv':'September','uk-wide/rtOCT.csv':'October',
      'uk-wide/rtNOV.csv':'November','uk-wide/rtDEC.csv':'December'}

rv = {'uk-wide/rvJAN.csv':'January','uk-wide/rvFEB.csv':'February',
      'uk-wide/rvMAR.csv':'March','uk-wide/rvAPR.csv':'April',
      'uk-wide/rvMAY.csv':'May','uk-wide/rvJUN.csv':'June',
      'uk-wide/rvJUL.csv':'July','uk-wide/rvAUG.csv':'August',
      'uk-wide/rvSEP.csv':'September','uk-wide/rvOCT.csv':'October',
      'uk-wide/rvNOV.csv':'November','uk-wide/rvDEC.csv':'December'}


fieldnames = ['time', 'Monday','Tuesday','Wednesday','Thursday','Friday',
              'Saturday','Sunday']
files = [uc,ut,rt,rv]

for i in range(0,4):
    for key in files[i]:
        with open(key,'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for j in range(0,24*pointsPerHour):
                row = {'time': j}
                for day in days:
                    month = files[i][key]
                    row[day] = regionz[i].running[month][day][j]
                    #row[day] = UC.running[monthPlot][day][j]
                writer.writerow(row)


fieldnames = ['region','day','month','number']
with open('number.csv','w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for key in regions:
        for month in months:
            for day in days:
                row = {'day':day}
                row['region'] = key
                row['month'] = month
                row['number'] = regions[key].number[month][day]
                writer.writerow(row)

