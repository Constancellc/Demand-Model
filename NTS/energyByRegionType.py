# packages
import matplotlib.pyplot as plt
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction

nissanLeaf = Vehicle(1521.0,29.92,0.076,0.02195,0.86035,24.0)

regionTypes = {'1':'Urban Conurbation', '2':'Urban City and Town',
               '3':'Rural Town', '4':'Rural Village'}

for rt in regionTypes:
    offset=float(int(rt)-1)/4
    test = EnergyPrediction('3','5',nissanLeaf,regionType=rt)
#test.plotMileage(wait=True)
    plt.figure(1)
    test.plotEnergyConsumption(newFigure=False,wait=True,label=regionTypes[rt],
                               normalise=True,offset=offset,width=0.25)
    
    plt.figure(2)
    test.plotEnergyConsumption(newFigure=False,wait=True,label=regionTypes[rt],
                               normalise=False,offset=offset,width=0.25)
plt.figure(1)
plt.legend()
plt.title('Normalised')
plt.ylabel('probability')
plt.xlabel('energy consumption (kWh)')


plt.figure(2)
plt.legend()
plt.title('Un-normalised')
plt.ylabel('# vehicles')
plt.xlabel('energy consumption (kWh)')
plt.show()
