import matplotlib.pyplot as plt
from SMenergyPrediction import HouseholdElectricityDemand

test = HouseholdElectricityDemand(region='7')

plt.figure(1)
for month in [1,4,7,10]:
    profiles = test.getProfile(3,12,nProfiles=1000)

    m = [0.0]*48
    #h = [0.0]*48
    #l = [4.0]*48

    for i in range(0,len(profiles)):
        for j in range(0,48):
            m[j] += profiles[i][j]/len(profiles)
            '''
            if profiles[i][j] > h[j]:
                h[j] = profiles[i][j]
            if profiles[i][j] < l[j]:
                l[j] = profiles[i][j]
            '''
    plt.plot(m,label=str(m))
plt.legend()
plt.show()
