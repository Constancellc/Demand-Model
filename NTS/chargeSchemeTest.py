# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
# my code
from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import EnergyPrediction, NationalEnergyPrediction

day = '3'
month = '2'


run = EnergyPrediction(day)
dumbProfile = run.getDumbChargingProfile(3.5,tmax=36*60,logOutofCharge=True,
                                         highUseWorkCharging=False,
                                         highUseHomeCharging=False,
                                         highUseShopCharging=False)

print float(run.nOutOfCharge)*100/run.nVehicles,
print '% out of charge in scenario 1'


run = EnergyPrediction(day)
dumbProfile = run.getDumbChargingProfile(3.5,tmax=36*60,logOutofCharge=True,
                                         highUseWorkCharging=False,
                                         highUseHomeCharging=True,
                                         highUseShopCharging=False)

print float(run.nOutOfCharge)*100/run.nVehicles,
print '% out of charge in scenario 2'


run = EnergyPrediction(day)
dumbProfile = run.getDumbChargingProfile(3.5,tmax=36*60,logOutofCharge=True,
                                         highUseWorkCharging=True,
                                         highUseHomeCharging=True,
                                         highUseShopCharging=False)

print float(run.nOutOfCharge)*100/run.nVehicles,
print '% out of charge in scenario 3'


run = EnergyPrediction(day)
dumbProfile = run.getDumbChargingProfile(3.5,tmax=36*60,logOutofCharge=True,
                                         highUseWorkCharging=False,
                                         highUseHomeCharging=True,
                                         highUseShopCharging=True)

print float(run.nOutOfCharge)*100/run.nVehicles,
print '% out of charge in scenario 4'


run = EnergyPrediction(day)
dumbProfile = run.getDumbChargingProfile(3.5,tmax=36*60,logOutofCharge=True,
                                         highUseWorkCharging=True,
                                         highUseHomeCharging=True,
                                         highUseShopCharging=True)

print float(run.nOutOfCharge)*100/run.nVehicles,
print '% out of charge in scenario 5'

