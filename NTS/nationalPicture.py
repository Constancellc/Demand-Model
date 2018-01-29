# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
#from vehicleModelCopy import Drivecycle, Vehicle
from NTSenergyPrediction import NationalEnergyPrediction

day = '3'
optPPH = 1
clstPPH = 15
nHours = 36
resultsStem = '../../Documents/simulation_results/NTS/national/'

for month in ['1','4','7','10']:
    # starting simulation
    run = NationalEnergyPrediction(day,month,vehicle='teslaS60D',smoothTimes=True)

    # getting charging profiles
    dumbProfile = run.getDumbChargingProfile(3.5,nHours) # kW

    psuedo = run.getPsuedoOptimalProfile(7.0,deadline=10)
    
    clustered = run.getClusteredOptimalProfiles(7.0,10,pointsPerHour=clstPPH)
    
    smart = run.getOptimalChargingProfiles(7,deadline=10)
    smartProfile = [0.0]*nHours*optPPH
    for vehicle in smart['']:
        for i in range(len(smartProfile)):
            smartProfile[i] += smart[''][vehicle][i]

    # interpolating smart and clustered
    intSmart = [0]*len(dumbProfile)
    for t in range(len(intSmart)):
        p1 = int(t*optPPH/60)
        p2 = p1+1

        if p2 == len(smartProfile):
            p2 -= 1

        f = float(t%(60/optPPH))/(60/optPPH)
        intSmart[t] = (1-f)*smartProfile[p1] + f*smartProfile[p2]
    smartProfile = intSmart

    intClst = [0]*len(dumbProfile)
    for t in range(len(intSmart)):
        p1 = int(t*clstPPH/60)
        p2 = p1+1

        if p2 == len(clustered):
            p2 -= 1

        f = float(t%int(60/clstPPH))/(60/clstPPH)

        intClst[t] = (1-f)*clustered[p1] + f*clustered[p2]
    clustered = intClst
    
    # getting base load used
    base = run.baseLoad

    for i in range(0,len(dumbProfile)):
        dumbProfile[i] += base[i]
        psuedo[i] += base[i]
        smartProfile[i] += base[i]
        clustered[i] += base[i]

        dumbProfile[i] = dumbProfile[i]/1000000 # kW -> GW
        smartProfile[i] = smartProfile[i]/1000000
        psuedo[i] = psuedo[i]/1000000
        clustered[i] = clustered[i]/1000000
        base[i] = base[i]/1000000

    with open(resultsStem+month+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t','base','dumb','smart','psuedo','clustered'])
        for t in range(len(dumbProfile)):
            writer.writerow([t,base[t],dumbProfile[t],smartProfile[t],psuedo[t],
                             clustered[t]])

