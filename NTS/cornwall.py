from NTSenergyPrediction import AreaEnergyPrediction, BaseLoad
import matplotlib.pyplot as plt
import numpy as np

#base = BaseLoad('3','5',36,unit='G')
#profile = base.getLoad(population=532273)

cornwall = AreaEnergyPrediction('9',0,205591,146060,180622,'3','5')
smartProfiles = cornwall.getOptimalChargingProfiles(4)
dumb = cornwall.getDumbChargingProfile(3.5,36)

base = cornwall.baseLoad

smartProfile = [0.0]*36

for sprofile in smartProfiles:
    for i in range(0,36):
        smartProfile[i] += smartProfiles[sprofile][i]

for i in range(0,36*60):
    dumb[i] += base[i]
    if i%60 == 0:
        smartProfile[i/60] += base[i]
        
plt.figure(1)
plt.plot(np.linspace(0,36,num=60*36),dumb)
plt.plot(smartProfile)
plt.show()
