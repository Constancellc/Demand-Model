import matplotlib.pyplot as plt
import numpy as np
import csv

"""
THIS IS GOING TO BE A FUNCTION TO PLOT THE PREDICTED LIVE POWER DEMAND OF A CITY
OR AREA, SHOWING ITS VARIATION THROUGHOUT THE YEAR, WEEK AND DAY
"""

regionType = 'Urban City and Town'
#regionType = 'Rural Village, Hamlet and Isolated Dwelling'
population = 64.1# million

months = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']

uc = {'January':'uk-wide/ucJAN.csv','February':'uk-wide/ucFEB.csv',
      'March':'uk-wide/ucMAR.csv','April':'uk-wide/ucAPR.csv',
      'May':'uk-wide/ucMAY.csv','June':'uk-wide/ucJUN.csv',
      'July':'uk-wide/ucJUL.csv','August':'uk-wide/ucAUG.csv',
      'September':'uk-wide/ucSEP.csv','October':'uk-wide/ucOCT.csv',
      'November':'uk-wide/ucNOV.csv','December':'uk-wide/ucDEC.csv'}

ut = {'January':'uk-wide/utJAN.csv','February':'uk-wide/utFEB.csv',
      'March':'uk-wide/utMAR.csv','April':'uk-wide/utAPR.csv',
      'May':'uk-wide/utMAY.csv','June':'uk-wide/utJUN.csv',
      'July':'uk-wide/utJUL.csv','August':'uk-wide/utAUG.csv',
      'September':'uk-wide/utSEP.csv','October':'uk-wide/utOCT.csv',
      'November':'uk-wide/utNOV.csv','December':'uk-wide/utDEC.csv'}

rt = {'January':'uk-wide/rtJAN.csv','February':'uk-wide/rtFEB.csv',
      'March':'uk-wide/rtMAR.csv','April':'uk-wide/rtAPR.csv',
      'May':'uk-wide/rtMAY.csv','June':'uk-wide/rtJUN.csv',
      'July':'uk-wide/rtJUL.csv','August':'uk-wide/rtAUG.csv',
      'September':'uk-wide/rtSEP.csv','October':'uk-wide/rtOCT.csv',
      'November':'uk-wide/rtNOV.csv','December':'uk-wide/rtDEC.csv'}

rv = {'January':'uk-wide/rvJAN.csv','February':'uk-wide/rvFEB.csv',
      'March':'uk-wide/rvMAR.csv','April':'uk-wide/rvAPR.csv',
      'May':'uk-wide/rvMAY.csv','June':'uk-wide/rvJUN.csv',
      'July':'uk-wide/rvJUL.csv','August':'uk-wide/rvAUG.csv',
      'September':'uk-wide/rvSEP.csv','October':'uk-wide/rvOCT.csv',
      'November':'uk-wide/rvNOV.csv','December':'uk-wide/rvDEC.csv'}

regions = {'Urban Conurbation':uc,'Urban City and Town':ut,
           'Rural Town and Fringe':rt,
           'Rural Village, Hamlet and Isolated Dwelling':rv}

fig = plt.figure()

xaxis = np.linspace(5,29,num=4)
my_xticks = ['08:00','14:00','20:00','02:00']

for i in range(0,12):
    if i == 0:
        ax1 = fig.add_subplot(3,4,i+1)
    else:
        ax2 = fig.add_subplot(3,4,i+1, sharey=ax1)
    #plt.subplot(3,4,i+1)
    # first find the relevant data set
    with open(regions[regionType][months[i]]) as csvfile:
        mon = []
        tue = []
        wed = []
        thu = []
        fri = []
        sat = []
        sun = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            mon.append(float(row['Monday'])*population)
            tue.append(float(row['Tuesday'])*population)
            wed.append(float(row['Wednesday'])*population)
            thu.append(float(row['Thursday'])*population)
            fri.append(float(row['Friday'])*population)
            sat.append(float(row['Saturday'])*population)
            sun.append(float(row['Sunday'])*population)

        if False: # if you want to plot cumulative
            for j in range(1,len(mon)):
                mon[j] = mon[j-1] + mon[j]
                tue[j] = tue[j-1] + tue[j]
                wed[j] = wed[j-1] + wed[j]
                thu[j] = thu[j-1] + thu[j]
                fri[j] = fri[j-1] + fri[j]
                sat[j] = sat[j-1] + sat[j]
                sun[j] = sun[j-1] + sun[j]
        
        x = np.linspace(5,29,num=24*60)
        plt.plot(x,mon,label='Monday')
        plt.plot(x,tue,label='Tuesday')
        plt.plot(x,wed,label='Wednesday')
        plt.plot(x,thu,label='Thursday')
        plt.plot(x,fri,label='Friday')
        plt.plot(x,sat,label='Saturday')
        plt.plot(x,sun,label='Sunday')
        if i == 1:
            plt.legend(loc=[-1,-2.7],ncol=7)
        plt.xticks(xaxis, my_xticks)
        if i == 0 or i == 4 or i == 8:
            plt.ylabel('power (GW)')
        plt.title(months[i],y=0.9)
plt.show()
