# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

day = '6'
month = '2'


run = EnergyPrediction(day,month)
dumbProfile = run.getDumbChargingProfile(3.5,tmax=36*60,logOutofCharge=True,
                                         highUseWorkCharging=False,
                                         highUseHomeCharging=False,
                                         highUseShopCharging=False)

missing1 = run.getMissingCapacity(36)

run2 = EnergyPrediction(day,month)
dumbProfile2 = run2.getDumbChargingProfile(3.5,tmax=36*60,logOutofCharge=True,
                                           highUseWorkCharging=False,
                                           highUseShopCharging=False)
missing2 = run2.getMissingCapacity(36)

run3 = EnergyPrediction(day,month)
dumbProfile3 = run3.getDumbChargingProfile(3.5,tmax=36*60,logOutofCharge=True,
                                           highUseShopCharging=False)
missing3 = run3.getMissingCapacity(36)

run4 = EnergyPrediction(day,month)
dumbProfile4 = run4.getDumbChargingProfile(3.5,tmax=36*60,logOutofCharge=True)
missing4 = run4.getMissingCapacity(36)

plt.figure(1)
plt.plot(dumbProfile,label='without')
plt.plot(dumbProfile2,label='home only')
plt.plot(dumbProfile3,label='home + work')
plt.plot(dumbProfile4,label='home, work + shops')
plt.ylabel('Power')
plt.legend()

plt.figure(2)
plt.bar(range(0,len(missing2)),missing1,label='without mid-day')
plt.bar(range(0,len(missing2)),missing2,label='home only')
plt.bar(range(0,len(missing2)),missing3,label='home + work')
plt.bar(range(0,len(missing2)),missing4,label='home, work + shopping')
plt.legend()
plt.ylabel('number of vehicles')
plt.xlabel('missing capacity (kWh)')
plt.show()