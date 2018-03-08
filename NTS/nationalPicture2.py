# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from NTSenergyPrediction2 import NationalEnergyPrediction

day = '2'
deadline = 16
resultsStem = '../../Documents/simulation_results/NTS/national/'

for month in ['1','4','7','10']:
    # starting simulation
    run = NationalEnergyPrediction(day,month,car='teslaS60D',smoothTimes=True)

    # getting charging profiles
    dumb = run.getDumbCharging(3.5,nHours=48+deadline) # kW

    psuedo = run.getApproximateLoadFlattening(deadline=deadline)
    
    smart = getOptimalLoadFlattening(7,deadline=deadline)[1]
    

    # interpolating smart and clustered
    intSmart = [0]*len(dumbProfile)
    for t in range(len(intSmart)):
        p1 = int(t/6)
        p2 = p1+1

        if p2 == len(smart):
            p2 -= 1

        f = float(t%(60/optPPH))/(60/optPPH)
        intSmart[t] = (1-f)*smart[p1] + f*smart[p2]
    smart = intSmart
    
    # getting base load used
    base = run.baseLoad

    for i in range(0,len(dumbProfile)):
        dumb[i] += base[i]
        psuedo[i] += base[i]
        smart[i] += base[i]

        dumbProfile[i] = dumbProfile[i]/1000000 # kW -> GW
        smartProfile[i] = smartProfile[i]/1000000
        psuedo[i] = psuedo[i]/1000000
        base[i] = base[i]/1000000

    with open(resultsStem+month+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t','base','dumb','smart','psuedo'])
        for t in range(len(dumbProfile)):
            writer.writerow([t,base[t],dumbProfile[t],smartProfile[t],psuedo[t]])

