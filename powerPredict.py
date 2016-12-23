# install matplot

import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# ------------------------------------------------------------------------------
# CLASS DEFINITIONS SECTION
# ------------------------------------------------------------------------------

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

        self.running = running
        self.charging = charging

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
        
class Drivecycle:
    def __init__(self, distance):
        
        # First, import artemis
        v0 = []
        with open('artemis_urban.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                v0.append(float(row[0])*0.277778)

        # Then, calculate distance covered by one cycle
        s0 = 0
        for value in v0:
            s0 += value

        v = []
        if s0 >= distance:
            # If the distance covered by one cycle is greater than the trip
            s = 0
            i = 0
            while s <= distance:
                v.append(v0[i])
                s += v0[i]
                i += 1

        else:
            for i in range(0,int(distance/s0)):
                for value in v0:
                    v.append(value)
            s = int(distance/s0)*s0
            
            while s <= distance:
                v.append(v0[i])
                s += v0[i]
                i += 1

        self.velocity = v

        a = [0]

        for i in range(0,len(v)-1):
            a.append(v[i+1]-v[i])

        self.acceleration = a

class Vehicle:
    def __init__(self,mass,Ta,Tb,Tc,eff):
        self.mass = mass
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
        
        with open('FINALregionTypePurposeLength.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array.append(row)

            regions = array[0]
            
            array = array[1:]

            for row in array:
                purpose = row[0]

                for i in range(1,len(regions)):
                    distance = float(row[i])*1609.34 # in m
                    cycle = Drivecycle(distance)
                    v = cycle.velocity 
                    a = cycle.acceleration

                    F = []
                    for value in v:
                        F.append(self.Ta + self.Tb*value + self.Tc*value*value)

                    for j in range(0,len(a)):
                        F[j] += self.mass*a[j]

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
        
        files = ['FINALregionTypePurpose.csv','FINALpurposeDay.csv',
                 'FINALpurposeStartHour.csv']
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
        self.hour = out[2]

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
            

# ------------------------------------------------------------------------------
# INITIALIZATION SECTION
# ------------------------------------------------------------------------------

nissanLeaf = Vehicle(1705,33.78,0.0618,0.02282,0.7)
nissanLeaf.loadEnergies()

UC = Region(60)
UT = Region(60)
RT = Region(60)
RV = Region(60)
regions = {'Urban Conurbation':UC,'Urban City and Town':UT,
           'Rural Town and Fringe':RT,
           'Rural Village, Hamlet and Isolated Dwelling':RV}


for i in range(0,10000):
    trip = Journey(nissanLeaf)
    trip.generate()
    trip.addToDataset(regions)

days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
months = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']
regionz = [UC,UT,RT,RV]
x = np.linspace(0,24,num=24*60)

monthPlot = raw_input("Please enter a month to plot: ")

with open('uc.csv', 'w') as csvfile:
    fieldnames = ['time', 'Monday','Tuesday','Wednesday','Thursday','Friday',
                  'Saturday','Sunday']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    j = 0
    for j in range(0,len(UC.running[monthPlot]['Monday'])):
        row = {'time': j}
        for day in days:
            row[day] = UC.running[monthPlot][day][j]
        writer.writerow(row)

fig = plt.figure(1)
i = 1
for day in days:
    fig.add_subplot(4,2,i)
    for region in regionz:
        plt.plot(x,region.running[monthPlot][day])
    i += 1
plt.show()



