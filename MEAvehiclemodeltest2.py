import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from cvxopt import matrix, spdiag, solvers, sparse
from vehicleModel import Drivecycle, Vehicle

results = []
#distances = []
#energies = []

distanceVsEnergy = {}

nissanLeaf = Vehicle(1705.0,29.92,0.076,0.02195,0.86035,32.0)
nissanLeaf.load += 75.0

#accessoryLoad = 0.2 # kW
cars = []

predicted = []
actual = []

predictions = {'01':[],'02':[],'03':[],'04':[],'05':[],'06':[],'07':[],'08':[],
               '09':[],'10':[],'11':[],'12':[]}
actuals = {'01':[],'02':[],'03':[],'04':[],'05':[],'06':[],'07':[],'08':[],
               '09':[],'10':[],'11':[],'12':[]}
titles = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
          '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}

trainingData = {'01':[],'02':[],'03':[],'04':[],'05':[],'06':[],'07':[],'08':[],
               '09':[],'10':[],'11':[],'12':[]}
testingData = {'01':[],'02':[],'03':[],'04':[],'05':[],'06':[],'07':[],'08':[],
               '09':[],'10':[],'11':[],'12':[]}

with open('../Documents/My_Electric_avenue_Technical_Data/EVTripData.csv') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        ran = random.random()
        '''
        if ran > 0.9:
            month = row[1][5:7]
            distance = float(row[3]) # m
            energy = float(row[4])/1000 # Wh

            testData[month].append([distance,enegy])
'''            
        if ran < 0.1:
                #        userID = row[0]        
    #        year = row[1][:4]
            month = row[1][5:7]
    #        day = row[1][8:10]
    #        outHour = int(row[1][11:13])
    #        outMins = int(row[1][14:16])
    #        outSecs = int(row[1][17:19])
    #        backHour = int(row[2][11:13])
    #        backMins = int(row[2][14:16])
    #        backSecs = int(row[2][17:19])
            distance = float(row[3]) # m
            energy = float(row[4])/1000 # Wh

            trainingData[month].append([distance,energy])
            
def error(accessoryLoad, month,plot=False):
    error = 0.0
    i = 0

    for row in trainingData[month]:

        distance = row[0]
        energy = row[1]

        if int(distance) == 0:
            continue

        cycleR = Drivecycle(distance,'rural')
        energyPR = nissanLeaf.getEnergyExpenditure(cycleR,accessoryLoad)

        if plot == True:
            predictions[month].append(energyPR)
            actuals[month].append(energy)

        d = energy-energyPR
        error += d*d
        i += 1

    return error/i

        #distances.append(distance)
        #energies.append(energy)

#distances = np.array(distances)
#energies = np.array(energies)
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
chosen = {}

for month in months:
    best = 10^20
    for accessory in np.arange(0.0,2.0,0.05):
        mse = error(accessory,month)
        if mse <= best:
            best = mse
            accessory_best = accessory

    chosen[month] = accessory_best

    print accessory_best
    
print chosen

for month in months:
    var = error(chosen[month],month,plot=True)
    print 'the variance is ',
    print var

# now testing
# for month in months:

    
plt.figure(1)
for month in months:
    plt.subplot(3,4,int(month))
    plt.plot(predictions[month],actuals[month],'x')
    plt.title(titles[month])
#plt.plot(predicted,actual,'x')
    #plt.xlabel('predicted')
    #plt.ylabel('actual')
    plt.plot([0,15],[0,15])

#plt.title('kWh energy expended over a given distance')


plt.show()


