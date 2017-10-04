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

    smartProfiles = cornwall.getOptimalChargingProfiles(7,deadline=12,
                                                         solar=solarData[month],
                                                         pointsPerHour=pph,
                                                         allowOverCap=False,
                                                         chargeAtWork=False)

    smartProfilesWC = cornwall.getOptimalChargingProfiles(7,deadline=12,
                                                         solar=solarData[month],
                                                         pointsPerHour=pph,
                                                         allowOverCap=False,
                                                         chargeAtWork=True)

    #smartProfiles.update(smartProfiles2)
    #smartProfiles = smartProfiles2
    dumb = cornwall.getDumbChargingProfile(3.5,36,sCharge=False)

    base = cornwall.baseLoad

    solar = {}
    net = {}
    netWC = {}
    oldNet = {}
    for key in cornwall.solar:
        profile = cornwall.solar[key]
        for i in range(0,len(profile)):
            profile[i] = -1.0*profile[i]/1000 # kW -> MW
        solar[key] = profile

    smartProfile = {}
    smartProfileWC = {}

    for key in smartProfiles:
        smartProfile[key] = [0.0]*36*pph

        for sprofile in smartProfiles[key]:
            for i in range(0,len(smartProfiles[key][sprofile])):
                smartProfile[key][i] += smartProfiles[key][sprofile][i]
                
    for key in smartProfilesWC:
        smartProfileWC[key] = [0.0]*36*pph

        for sprofile in smartProfilesWC[key]:
            for i in range(0,len(smartProfilesWC[key][sprofile])):
                smartProfileWC[key][i] += smartProfilesWC[key][sprofile][i]

    '''

    for i in range(0,36*60):
        dumb[i] += base[i]
        if i%(60/pph) == 0:
            for key in smartProfile:
                smartProfile[key][pph*i/60] += base[i]

    '''

    # convert from kW to MW
    for i in range(0,len(dumb)):
        dumb[i] = float(dumb[i])/1000
        base[i] = float(base[i])/1000
        
    for key in smartProfile:
        net[key] = []
        oldNet[key] = []
        for i in range(0,len(smartProfile[key])):
            smartProfile[key][i] = float(smartProfile[key][i])/1000
            net[key].append(solar[key][int(i*60/pph)]+base[int(i*60/pph)]+
                            smartProfile[key][i])
            oldNet[key].append(solar[key][int(i*60/pph)]+base[int(i*60/pph)])

    for key in smartProfileWC:
        netWC[key] = []
        for i in range(0,len(smartProfileWC[key])):
            smartProfileWC[key][i] = float(smartProfileWC[key][i])/1000
            netWC[key].append(solar[key][int(i*60/pph)]+base[int(i*60/pph)]+
                            smartProfileWC[key][i])

    x_ticks = ['12:00\nWed','15:00','18:00','21:00','00:00\nThu','03:00','06:00',
               '09:00']
    x = np.arange(12,36,3)

    clrs = {'h':'#f49842','m':'#83e041','l':'#4286f4'}
    lbls = {'h':'Solar Generation (H)','m':'Solar Generation (M)',
            'l':'Solar Generation (L)'}
    EVlbls = {'h':'EV Demand (H)','m':'EV Demand (M)',
              'l':'EV Demand (L)'}
    netlbls = {'h':'Net Demand (H)','m':'Net Demand (M)','l':'Net Demand (L)'}

    '''
    plt.figure(1)
    plt.rcParams["font.family"] = 'serif'
    plt.subplot(2,2,n)
    n += 1
    plt.plot(np.linspace(0,36,num=36*pph),net['m'],color='b',label='With EVs')
    plt.fill_between(np.linspace(0,36,num=36*pph),net['h'],net['l'],alpha=0.2,
                     color='b')
    
    plt.plot(np.linspace(0,36,num=36*pph),netWC['m'],color='r',
             label='With EVs + Work Charging')
    plt.fill_between(np.linspace(0,36,num=36*pph),netWC['h'],netWC['l'],alpha=0.2,
                     color='r')
    
    plt.plot(np.linspace(0,36,num=36*pph),oldNet['m'],color='g',
             label='Without EVs')
    plt.fill_between(np.linspace(0,36,num=36*pph),oldNet['h'],oldNet['l'],
                     alpha=0.2,color='g')
    plt.plot(np.linspace(0,36,num=60*36),base,c='k',ls=':',alpha=0.8,
             label='Base Load')
    plt.xlim(11,35)
    plt.xticks(x,x_ticks)
    plt.ylabel('Power (MW)')
    plt.ylim(-200,550)
    plt.title(months[month],y=0.9)
    if n == 2:
        plt.legend(ncol=5,loc=[0.2,1.05])
    plt.grid()

    # The section below generates three plots, for use in presentations
    '''
    for fig in [1,2,3]:
        plt.figure(fig)
        plt.rcParams["font.family"] = 'serif'
        plt.subplot(2,2,n)

        if fig > 1:
            plt.plot(np.linspace(0,36,num=36*pph),net['m'],color='b',label='With EVs')
            plt.fill_between(np.linspace(0,36,num=36*pph),net['h'],net['l'],alpha=0.2,
                             color='b')

        if fig > 2:           
            plt.plot(np.linspace(0,36,num=36*pph),netWC['m'],color='r',
                     label='With EVs + Work Charging')
            plt.fill_between(np.linspace(0,36,num=36*pph),netWC['h'],netWC['l'],alpha=0.2,
                             color='r')
        
        plt.plot(np.linspace(0,36,num=36*pph),oldNet['m'],color='g',
                 label='Without EVs')
        plt.fill_between(np.linspace(0,36,num=36*pph),oldNet['h'],oldNet['l'],
                         alpha=0.2,color='g')
        plt.plot(np.linspace(0,36,num=60*36),base,c='k',ls=':',alpha=0.8,
                 label='Base Load')
        plt.xlim(11,35)
        plt.xticks(x,x_ticks)
        plt.ylabel('Power (MW)')
        plt.ylim(-200,550)
        plt.title(months[month],y=0.9)
        if n == 2:
            plt.legend(ncol=5,loc=[0.2,1.05])
        plt.grid()
    
    n += 1

        #'''
    


   

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
