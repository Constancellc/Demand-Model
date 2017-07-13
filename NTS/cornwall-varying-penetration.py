from NTSenergyPrediction import AreaEnergyPrediction, BaseLoad
import matplotlib.pyplot as plt
import numpy as np

#base = BaseLoad('3','5',36,unit='G')
#profile = base.getLoad(population=532273)

month = '5'
pph = 4 # points per hour for the optimization

stem = '../../Documents/cornwall-pv-predictions/'
solarData = {'1':stem+'jan.csv','2':stem+'feb.csv','3':stem+'mar.csv',
             '4':stem+'apr.csv','5':stem+'may.csv','6':stem+'jun.csv',
             '7':stem+'jul.csv','8':stem+'aug.csv','9':stem+'sep.csv',
             '10':stem+'oct.csv','11':stem+'nov.csv','12':stem+'dec.csv'}
months = {'1':'January','2':'February','3':'March','4':'April','5':'May',
          '6':'June','7':'July','8':'August','9':'September','10':'October',
          '11':'November','12':'December'}

n = 4

penetrationLevel = [1.0,0.3,0.1,0.03]

for level in penetrationLevel:
    cornwall = AreaEnergyPrediction('9',0,205591,146060,180622,'3',month,
                                    vehicle='teslaS60D',penetration=level)
    print 'in this simulation I had',
    print cornwall.getNumberOfVehicles(),
    print 'vehicles'
    '''
    smartProfiles = cornwall.getOptimalChargingProfiles(7,deadline=None,
                                                        perturbDeadline=True,
                                                        pointsPerHour=pph,
                                                        allowOverCap=False)
    '''
    smartProfiles2 = cornwall.getOptimalChargingProfiles(7,deadline=10,#
                                                         solar=solarData[month],
                                                         perturbDeadline=True,
                                                         pointsPerHour=pph,
                                                         allowOverCap=False)

    #smartProfiles.update(smartProfiles2)
    smartProfiles = smartProfiles2
    #dumb = cornwall.getDumbChargingProfile(3.5,36,sCharge=False)

    base = cornwall.baseLoad
    
    solar = {}
    net = {}
    for key in cornwall.solar:
        profile = cornwall.solar[key]
        for i in range(0,len(profile)):
            profile[i] = -1.0*profile[i]/1000 # kW -> MW
        solar[key] = profile
    

    smartProfile = {}

    for key in smartProfiles:
        smartProfile[key] = [0.0]*36*pph

        for sprofile in smartProfiles[key]:
            for i in range(0,len(smartProfiles[key][sprofile])):
                smartProfile[key][i] += smartProfiles[key][sprofile][i]
    '''
    for i in range(0,36*60):
        #dumb[i] += base[i]
        if i%(60/pph) == 0:
            for key in smartProfile:
                smartProfile[key][pph*i/60] += base[i]
    '''
    # convert from kW to MW
    for i in range(0,36*60):
        #dumb[i] = float(dumb[i])/1000
        base[i] = float(base[i])/1000
    for key in smartProfile:
        net[key] = []
        for i in range(0,len(smartProfile[key])):
            smartProfile[key][i] = float(smartProfile[key][i])/1000
            net[key].append(solar[key][i*60/pph]+base[i*60/pph]+smartProfile[key][i])

    x_ticks = ['12:00\nWed','15:00','18:00','21:00','00:00\nThu','03:00','06:00',
               '09:00']
    x = np.arange(12,36,3)

    clrs = {'h':'#f49842','m':'#83e041','l':'#4286f4'}
    lbls = {'h':'H solar generation','m':'M solar generation',
            'l':'L solar generation'}
    EVlbls = {'h':'EV demand (H)','m':'EV demand (M)',
              'l':'EV demand (L)'}
    netlbls = {'h':'net demand (H)','m':'net demand (M)','l':'net demand (L)'}
    plt.figure(1)
    plt.subplot(2,2,n)
    n -= 1
    for key in smartProfile:
        if key == '':
            plt.plot(np.linspace(0+float(pph)/60,36+float(pph)/60,num=36*pph),
                     smartProfile[key])
        else:
            plt.plot(np.linspace(0+float(pph)/60,36+float(pph)/60,num=36*pph),
                     smartProfile[key],color=clrs[key],label=EVlbls[key])
        
    for key in solar:
        plt.plot(np.linspace(0,36,num=60*36),solar[key],ls='--',c=clrs[key],
                 label=lbls[key])
        plt.plot(np.linspace(0,36,num=36*pph),net[key],color=clrs[key],ls=':',label=netlbls[key])
                 
    plt.plot(np.linspace(0,36,num=60*36),base,c='k',ls=':',alpha=0.8,
             label='base load')
    plt.xlim(11,35)
    plt.xticks(x,x_ticks)
    plt.ylabel('Power (MW)')
    plt.ylim(-500,500)
    plt.title(str(int(100*level))+'%',y=0.9)
    if n == 1:
        plt.legend(ncol=4,loc=[0.2,1.1])
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
