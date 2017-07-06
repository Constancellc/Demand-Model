import matplotlib.pyplot as plt

from NTSvehicleLocation import LocationPrediction

test = LocationPrediction('3',month='5')
locations = test.getVehicleLocations()
p = test.getPAvaliableToCharge()

plt.figure(1)
for l in locations:
    plt.plot(locations[l][24*60:],label=l)
plt.legend()

plt.figure(2)
plt.plot(p)
plt.ylim(0,1)
plt.show()
