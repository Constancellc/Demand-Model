from NTSenergyPrediction import AreaEnergyPrediction, BaseLoad
import matplotlib.pyplot as plt
import numpy as np
import copy

#base = BaseLoad('3','5',36,unit='G')
#profile = base.getLoad(population=532273)

simulationMonth = ['1','4','7','10']#['2','5','8','11']#
pph = 4 # points per hour for the optimization

stem = '../../Documents/cornwall-pv-predictions/'
solarData = {'1':stem+'jan.csv','2':stem+'feb.csv','3':stem+'mar.csv',
             '4':stem+'apr.csv','5':stem+'may.csv','6':stem+'jun.csv',
             '7':stem+'jul.csv','8':stem+'aug.csv','9':stem+'sep.csv',
             '10':stem+'oct.csv','11':stem+'nov.csv','12':stem+'dec.csv'}
months = {'1':'January','2':'February','3':'March','4':'April','5':'May',
          '6':'June','7':'July','8':'August','9':'September','10':'October',
          '11':'November','12':'December'}

n = 1

for month in simulationMonth:
    cornwall = AreaEnergyPrediction('9',0,205591,146060,180622,'3',month,
                                    vehicle='teslaS60D')
    
    smartProfiles = cornwall.getOptimalChargingProfiles(7,deadline=10,
                                                        perturbDeadline=True,
                                                        pointsPerHour=pph)


    dumb = cornwall.getDumbChargingProfile(3.5,36,sCharge=False)

    base = cornwall.baseLoad

    smartProfile = {}

    for key in smartProfiles:
        smartProfile[key] = [0.0]*36*pph

        for sprofile in smartProfiles[key]:
            for i in range(0,len(smartProfiles[key][sprofile])):
                smartProfile[key][i] += smartProfiles[key][sprofile][i]



    for i in range(0,36*60):
        dumb[i] += base[i]
        if i%(60/pph) == 0:
            for key in smartProfile:
                smartProfile[key][int(pph*i/60)] += base[i]



    # convert from kW to MW
    for i in range(0,len(dumb)):
        dumb[i] = float(dumb[i])/1000
        base[i] = float(base[i])/1000
    for key in smartProfile:
        for i in range(0,len(smartProfile[key])):
            smartProfile[key][i] = float(smartProfile[key][i])/1000

    x_ticks = ['08:00\nWed','14:00','20:00','02:00','08:00\nThu']
    x = np.arange(8,38,6)

    clrs = {'h':'#f49842','m':'#83e041','l':'#4286f4'}
    plt.figure(1)
    plt.rcParams["font.family"] = 'serif'
    plt.subplot(2,2,n)
    n += 1
    plt.plot(np.linspace(0,36,num=60*36),base,c='g',ls=':',
             label='Base Load')
    plt.plot(np.linspace(0,36,num=60*36),dumb,label='Uncontrolled Charging')
    for key in smartProfile:
        if key == '':
            plt.plot(np.linspace(0+float(pph)/60,36+float(pph)/60,num=36*pph),
                 smartProfile[key],ls='--',label='Controlled Charging')
    plt.xlim(6,34)
    plt.xticks(x,x_ticks)
    plt.ylabel('Power (MW)')
    plt.ylim(150,800)
    plt.title(months[month],y=0.85)
    if n == 2:
        plt.legend(ncol=3,loc=[-0.3,1.1])
    plt.grid()

'''
plt.figure(2)#
plt.plot(np.linspace(0,36,num=60*36),dumb)
for key in smartProfile:
    if key != '':
        continue
    plt.plot(np.linspace(0+float(pph)/60,36+float(pph)/60,num=36*pph),
             smartProfile[key])
plt.plot(np.linspace(0,36,num=60*36),base,c='k',ls=':')
plt.xlim(11,35)
for key in solar:
    plt.plot(np.linspace(0,36,num=60*36),solar[key],ls='--',c=clrs[key])
plt.xticks(x,x_ticks)
plt.ylabel('Power (MW)')
plt.title(months[month],y=0.9)
'''
plt.show()
