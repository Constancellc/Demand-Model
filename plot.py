import matplotlib.pyplot as plt
import numpy as np
import csv

s = []
population = 7000

day = raw_input('Enter day of the week: ')

with open('rvSEP.csv', 'rU') as csvfile:
     reader = csv.reader(csvfile)
     reader.next()
     for row in reader:
         if day == 'Monday':
             s.append(float(row[1])*population)
         elif day == 'Tuesday':
             s.append(float(row[2])*population)
         elif day == 'Wednesday':
             s.append(float(row[3])*population)
         elif day == 'Thursday':
             s.append(float(row[4])*population)
         elif day == 'Friday':
             s.append(float(row[5])*population)
         elif day == 'Saturday':
             s.append(float(row[6])*population)
         elif day == 'Sunday':
             s.append(float(row[7])*population)


plt.plot(s)
plt.ylabel('kWh')
plt.show()
