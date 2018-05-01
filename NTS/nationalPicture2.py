# packages
import matplotlib.pyplot as plt
import numpy as np
import csv
# my code
from NTSenergyPrediction2 import NationalEnergyPrediction

day = '2'
deadline = 16
resultsStem = '../../Documents/simulation_results/NTS/national/'

simDay = {'1':'tue','2':'wed','3':'thu','4':'fri','5':'sat','6':'sun','7':'mon'}
for month in ['1','4','7','10']:
    # starting simulation
    run = NationalEnergyPrediction(day,month,car='teslaS60D',smoothTimes=True)

    # getting charging profiles
    dumb3 = run.getDumbCharging(3.5,nHours=48+deadline,allowOverCap=True) # kW
    dumb7 = run.getDumbCharging(7.0,nHours=48+deadline,allowOverCap=True) # kW

    #psuedo = run.getApproximateLoadFlattening(deadline=deadline)
    
    #smart = run.getOptimalLoadFlattening(7,deadline=deadline)[1]

    # interpolating smart and clustered
    '''
    intSmart = [0]*len(dumb3)
    for t in range(len(intSmart)):
        p1 = int(t/6)
        p2 = p1+1

        if p2 == len(smart):
            p2 -= 1

        f = float(t%(6))/(6)
        intSmart[t] = (1-f)*smart[p1] + f*smart[p2]
    smart = intSmart
    '''
    # getting base load used
    base = run.baseLoad

    for i in range(0,len(dumb3)):
        dumb3[i] += base[i]
        dumb7[i] += base[i]
        #psuedo[i] += base[i]
        #smart[i] += base[i]

        dumb3[i] = dumb3[i]/1000000 # kW -> GW
        dumb7[i] = dumb7[i]/1000000 
        #smart[i] = smart[i]/1000000
        #psuedo[i] = psuedo[i]/1000000
        base[i] = base[i]/1000000

    with open(resultsStem+simDay[day]+'/'+month+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t','base','dumb 3.5kW','dumb 7kW'])#,'smart','psuedo'])
        for t in range(len(dumb3)):
            writer.writerow([t,base[t],dumb3[t],dumb7[t]])#,smart[t],psuedo[t]])

