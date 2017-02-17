import matplotlib.pyplot as plt
import numpy as np
import csv
import random

regionType = 'Urban City and Town'
population = 150200
month = 'November'

days = ['Monday','Tuesday','Wednesday','Thursday','Friday']

files = ['nts-data/purposeDay.csv','nts-data/purposeMonth.csv',
         'nts-data/regionTypePurpose.csv']

counters = {'Monday':[0.0]*24,'Tuesday':[0.0]*24,'Wednesday':[0.0]*24,
            'Thursday':[0.0]*24,'Friday':[0.0]*24}


for day in days:

    with open('number.csv','rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['day'] == day:
                if row['month'] == month:
                    if row['region'] == regionType:
                        journeysPerPerson = float(row['number'])

    nJourneys = journeysPerPerson*population
    nSim = 1000
    scale = float(nJourneys)/nSim

    fixed = [day, month, regionType]
    out = []

    for k in range(0,nSim):

        for j in range(0,3):
            # first, find the purpose given the regionType, or maybe day of week, or month... FUCK
            with open(files[j],'rU') as csvfile:
                reader = csv.reader(csvfile)
                variables = next(reader)
                for i in range(0,len(variables)):
                    if variables[i] == fixed[j]:
                        index = i

                if index is False:
                    raise Error('pdf problems')

                purposes = []
                pdf = []
                
                for row in reader:
                    if row == variables:
                        continue
                    else:
                        purposes.append(row[0])
                        pdf.append(row[index])
            sumPdf = 0

            for number in pdf:
               sumPdf += float(number)

            distribution = [0]*7

            for i in range(0,7):
               distribution[i] = float(pdf[i])/sumPdf

            out.append(distribution)

        purposeday = out[0]
        purposemonth = out[1]
        purposeregion = out[2]

        pdf = [0]*7

        for i in range(0,7):
            pdf[i] = purposeday[i]*purposemonth[i]*purposeregion[i]

        pdf[1] = 0.5*pdf[1] # Assume all education trips are round trips

        sumPdf = sum(pdf)

        # This should be the cdf of purpose given all of day, month and region
        cdf = [pdf[0]/sumPdf]

        for i in range(1,7):
            cdf.append(cdf[i-1]+pdf[i]/sumPdf)

        ran = random.random()

        j = 0

        while cdf[j] <= ran and j < 6:
            j += 1

        purpose = purposes[j]
       
        # we now have purpose, we now need time of day, ok this is where changes happen

        if purpose == 'Commute' or purpose == 'Education':
            with open('nts-data/purposeStartAMPM.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                pdf = []
                for row in reader:
                    if row[0] == (purpose+'AM'):
                        pdfAM = row[1:]
                    elif row[0] == (purpose+'PM'):
                        pdfPM = row[1:]

                # first get morning commmute
                ran = 0.5*random.random()
                i = 0
                c = float(pdfAM[0])
                while c <= ran:
                    i += 1
                    c += float(pdfAM[i])

                outStartHour = i+4

                ran = 0.5*random.random()
                i = 0
                c = float(pdfPM[0])
                while c <= ran:
                    i += 1
                    c += float(pdfPM[i])

                backStartHour = i+4

                if backStartHour > 23:
                    backStartHour -= 24
                
        else:
            with open('nts-data/purposeStartHour.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                pdf = []
                for row in reader:
                    if row[0] == purpose:
                        pdf = row[1:]

                times = []

                for j in range(0,2):
                    ran = random.random()
                    i = 0
                    c = float(pdf[0])
                    while c <= ran and i<23:
                        i += 1
                        c += float(pdf[i])

                    times.append(i)

                if times[0] < times[1]:
                    outStartHour = times[0]
                    backStartHour = times[1]

                else:
                    outStartHour = times[1]
                    backStartHour = times[0]

        counters[day][outStartHour] += scale
        counters[day][backStartHour] += scale
        
total = []
plt.figure(1)
for day in days:
    total += counters[day]
plt.plot(total)

# now get the inrix data to compare against
counters = {'Monday':[0]*24,'Tuesday':[0]*24,'Wednesday':[0]*24,
            'Thursday':[0]*24,'Friday':[0]*24}

with open('inrix/inrix.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        counters[row[0]][int(row[1])] += 1
total = []
for day in days:
    total += counters[day]
plt.plot(total)
plt.show()
