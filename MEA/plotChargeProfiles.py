import csv
import matplotlib.pyplot as plt
import numpy as np

# define the location for the output csv files to be stored
dumbStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/unchanged/'
nationalStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/national/'
householdStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/household/'
networkStem = '../../Documents/My_Electric_avenue_Technical_Data/profiles/network/'

# create arrays to store the final profiles
dumbProfiles = []
nationalProfiles = []
householdProfiles = []
networkProfiles = []

summedDumb = [0.0]*24*60
summedNational = [0.0]*24*60
summedHousehold = [0.0]*24*60
summedNetwork = [0.0]*24*60

# first get the profiles
for i in range(0,55):
    dumbProfile = []
    with open(dumbStem+str(i+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dumbProfile.append(float(row[0]))
            
    nationalProfile = []
    with open(nationalStem+str(i+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            nationalProfile.append(float(row[0]))
            
    householdProfile = []
    with open(householdStem+str(i+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            householdProfile.append(float(row[0]))
            
    networkProfile = []
    with open(networkStem+str(i+1)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            networkProfile.append(float(row[0]))

    dumbProfiles.append(dumbProfile)
    nationalProfiles.append(nationalProfile)
    householdProfiles.append(householdProfile)
    networkProfiles.append(networkProfile)

    for j in range(0,24*60):
        summedDumb[j] += dumbProfile[j]/55
        summedNational[j] += nationalProfile[j]/55
        summedHousehold[j] += householdProfile[j]/55
        summedNetwork[j] += networkProfile[j]/55


t = np.linspace(0,24,num=24*60)
x1 = [4,12,20]
x_ticks1 = ['04:00','12:00','20:00']
x2 = [2,6,10,14,18,22]
x_ticks2 = ['02:00','06:00','10:00','14:00','18:00','22:00']
# let's compare indinvidual profiles
plt.figure(1)
for i in range(0,16):
    plt.subplot(4,4,i+1)
    plt.plot(t,dumbProfiles[i])
    plt.plot(t,nationalProfiles[i])
    plt.plot(t,householdProfiles[i])
    plt.plot(t,networkProfiles[i],alpha=0.5)
    plt.xticks(x1,x_ticks1)
    plt.xlim(0,24)
    plt.ylim(0,8)


        
# and let's make sure the energy looks convincing
plt.figure(2)
plt.plot(t,summedDumb,label='dumb')
plt.plot(t,summedNational,label='national')
plt.plot(t,summedHousehold,label='household')
plt.plot(t,summedNetwork,alpha=0.5,label='network')

plt.legend()
plt.xticks(x2,x_ticks2)
plt.xlim(0,24)
plt.ylabel('Power per Vehicle (kW)')

plt.show()
