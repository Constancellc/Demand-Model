# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random


styles = ['NONE','DUMB','NATIONAL','HOUSEHOLD','NETWORK']
I = {}

for style in styles:
    I[style] = {1:[],2:[],3:[]}
    
    with open('../Downloads/openDSScurrents/currents-'+style+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            for i in range(1,4):
                try:
                    I[style][i].append(float(row[i]))
                except:
                    continue


t = np.linspace(0,24,num=1440)
xaxis2 = np.linspace(2,22,num=6)
my_xticks2 = ['02:00','06:00','10:00','14:00','18:00','22:00']

plt.figure(1)

for phase in range(1,4):
    plt.subplot(3,1,phase)
    for style in styles:
        plt.plot(t,I[style][phase],label=style)
    plt.ylabel('Current (A)')
    plt.xlim(0,24)
    plt.xticks(xaxis2, my_xticks2)
    plt.grid()
    if phase == 1:
        plt.legend()

    print 'PHASE ' + str(phase)


    for style in styles:
        print style
        print 'max: ',
        print max(I[style][phase])
        print 'min: ',
        print min(I[style][phase])
        print '-------'

plt.figure(2)

# physics
aluminium_density = 2700.0
aluminium_Cp = 910.0
air_density = 1.225

# line properties
L = 10.0863 # m 
R1 = 0.446 # per km

# climate properties
air_temp = 10 # celcius
#t0 = 11 # celcius

# cable properties - currently mole, with turkey commented out
aluminium_area = 0.0165#0.0206 # square inch
diameter = 0.177#0.198 # inch
emissivity = 0.23

aluminium_area = aluminium_area*0.00064516 # square inch -> square m
diameter = diameter*0.0254 # inch -> m
R = R1*L/1000 # per km -> actual resistance

mCp = aluminium_area*L*aluminium_density*aluminium_Cp

# ok i think i'll want a new approach

# first i'm going to need a rough s.s temperature

# we want qc +qr to equal I2R

# let's pick a ss current to use

I_ss = sum(I['NONE'][1])/len(I['NONE'][1])

print I_ss,
print 'A'
best = 0
gap = 10000000.0
for i in range(air_temp,60):
    temp = float(i)
    qr = 17.8*diameter*emissivity*(np.power((temp+273)/100,4)-
                                   np.power((air_temp+273)/100,4))
    qc = 3.645*np.sqrt(air_density)*np.power(diameter,0.75)\
                 *np.power(temp-air_temp,1.25)

    error = qc+qr-I_ss*I_ss*R

    if error < 0:
        error = -1*error

    if error < gap:
        gap = error
        best = temp

print best,
print ' degrees C'
t0 = best

Temps = {}
for phase in range(1,4):
    plt.subplot(3,1,phase)

    for style in styles:
        if phase == 1:
            Temps[style] = {}
    
        I_test = I[style][phase]
        T = [t0]

        for i in range(0,1440):
            qr = 17.8*diameter*emissivity*(np.power((T[i]+273)/100,4)-
                                           np.power((air_temp+273)/100,4))
            qc = 3.645*np.sqrt(air_density)*np.power(diameter,0.75)\
                 *np.power(T[i]-air_temp,1.25)
            dTdt = (R*I_test[i]*I_test[i]-qc-qr)/mCp

            T.append(t0+dTdt*60)

        Temps[style][phase] = T

        plt.plot(t,T[1:],label=style)
        plt.xlim(0,24)
        plt.xticks(xaxis2, my_xticks2)
        plt.ylim(30,65)
        plt.grid()
        plt.title('Phase '+str(phase),y=0.85)
        plt.ylabel('Temperature (C)')
        if phase == 3:
            plt.xlabel('Time')

        if phase == 1:
            plt.legend(loc=[0,1.2],ncol=5)
'''
temp = {}
# first work out the control case for no vehicles
temp['NONE'] = {}

for phase in range(1,4):
    temp['NONE'][phase] = [0.0]*1440
    sum_I2 = 0
    for i in range(0,1440):
        sum_I2 += I['NONE'][phase][i]*I['NONE'][phase][i]
        temp['NONE'][phase][i] = sum_I2*K
    
for style in styles:
    if style == 'NONE':
        continue
    temp[style] = {}

    for phase in range(1,4):
        plt.subplot(3,1,phase)
        temp[style][phase] = [0.0]*1440

        sum_I2 = 0
        for i in range(0,1440):
            sum_I2 += I[style][phase][i]*I[style][phase][i]

            temp[style][phase][i] = sum_I2*K - temp['NONE'][phase][i] 
            
        plt.plot(t,temp[style][phase],label=style)
        plt.xlim(0,24)
        plt.xticks(xaxis2,my_xticks2)

plt.legend()
'''
print '..............................'
print 'PRINTING MAX TEMPERATURES'
print '..............................'

for style in styles:
    print style,
    print ':',
    print max([max(Temps[style][1]),max(Temps[style][2]),max(Temps[style][3])]),
    print 'degrees C'

print '..............................'
print 'PRINTING AVERAGE TEMPERATURES'
print '..............................'

for style in styles:
    print style,
    print ': ',
    Tot = sum([sum(Temps[style][1]),sum(Temps[style][2]),sum(Temps[style][3])])
    print float(Tot)/(3*1441),
    print ' degrees C'

plt.show()
