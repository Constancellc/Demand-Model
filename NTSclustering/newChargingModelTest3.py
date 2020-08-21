import csv
import matplotlib.pyplot as plt
import random
import numpy as np
import copy

stem = '../../Documents/simulation_results/NTS/clustering/labels2/'

charge_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/charges.csv'

trip_data = '../../Documents/My_Electric_Avenue_Technical_Data/constance/trips.csv'

outstem = '../../Documents/simulation_results/NTS/clustering/power/'


# ok so this is going to be my new test, I want to start by geenrating the
# charging pdf of one vehicle for one week

# I am going to investigate at a resolution of 30 mins

        
# First get the pdfs for charging
pdfs = {'0':{},'1':{}} # after journey
pdfs_ = {'0':{},'1':{}} # random
for d in ['0','1']:
    for i in range(3):
        pdfs[d][i] = {}
        for s in range(6):
            pdfs[d][i][s] = [0]*48
    for s in range(6):
        pdfs_[d][s] = [0]*48

stm = {'0':'jointPdfW','1':'jointPdfWE'}
for d in ['0','1']:
    for i in range(3):       
        with open(stem+stm[d]+str(i+1)+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            s = 0
            for row in reader:
                for t in range(48):
                    pdfs[d][i][s][t] = float(row[t])
                s += 1
                
    with open(stem+stm[d]+'_.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        s = 0
        for row in reader:
            for t in range(48):
                pdfs_[d][s][t] = float(row[t])
            s += 1

def chargeAfterJourney(d,k,s,t):
    if random.random() < pdfs[d][k][s][t]:
        return True
    else:
        return False
    
def chargeAfterJourneyS(d,k,s,t):
    return pdfs[d][k][s][t]
        
def randomCharge(d,s,t):
    if random.random() < pdfs_[d][s][t]:
        return True
    else:
        return False
        
def randomChargeS(d,s,t):
    return pdfs_[d][s][t]

def normalise(x):
    s = sum(x)
    for i in range(len(x)):
        x[i] = x[i]/s
    return x
    
# Then get the NTS vehicle labels, and the household to vehicle list
MEA = {}
with open(stem+'MEAlabels.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA[row[0]] = int(row[1])
with open(stem+'MEAlabelsWE.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        MEA[row[0]] = int(row[1])

def step(t,d):
    t += 1
    if t >= 48:
        t = 0
        d += 1
    return [t,d]

true_charges = [0.0]*48*14
p_charge_new = [0.0]*48*14
p_charge_aj = [0.0]*48*14

t_veh = 'GC08'
startDay = 125# Monday
wkends = []
for d in [5,6,12,13]:
    wkends.append(str(startDay+d))

data = []
with open('mea_training_data - '+t_veh+'.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        # start, SOC, type, end
        offset = (int(row[0])-startDay)*48
        if row[3] == 'c':
            data.append([offset+int(int(row[1])/30),int(float(row[2])*6),
                         row[3],offset+int(float(row[1])/30)])
        else:
            data.append([offset+int(int(row[1])/30),int(float(row[2])*6),
                         row[3],offset+int(float(row[4])/30)])
        
t = 0
data_i = 0
s = 5
while t < 48*14:
    if t == data[data_i][3]:
        if data[data_i][2] == 'c':
            true_charges[data[data_i][0]] = 1
            data_i += 1
            if data_i == len(data):
                data_i = 0
        else:
            # journey ends here
            if data[data_i][3] > data[data_i][0]:
                for _t in range(data[data_i][0],data[data_i][3]):
                    p_charge_new[t] = 0.0
            d = str(125+int(t/48))
            hh = t%48
            s = data[data_i][1]
            try:
                k = MEA[t_veh+d]
            except:
                print(t_veh+d)
                k = 2
            if d in wkends:
                dt = '1'
            else:
                dt = '0'
            p_charge_new[t] = chargeAfterJourneyS(dt,k,s,hh)
            data_i += 1
            if data_i == len(data):
                data_i = 0
    elif p_charge_new[t] == 0:
        # random charge
        d = str(int(t/48))
        hh = t%48
        if d in wkends:
            dt = '1'
        else:
            dt = '0'
        p_charge_new[t] = randomChargeS(dt,s,hh)
        t += 1

    else:
        t += 1

def brier(p,true):
    s = 0
    for t in range(len(true)):
        s += np.power(p[t]-true[t],2)
    return s/len(true)

jLog = {}
for i in range(len(data)-1):
    if data[i][2] == 'c':
        continue
    d = int(data[i][0]/48)
    if d not in jLog:
        jLog[d] = []
    jLog[d].append(data[i][3])

for d in jLog:
    x = sorted(jLog[d])
    p_charge_aj[x[-1]] = 1


print(brier(p_charge_new[48*7:],true_charges[48*7:]))
#print(brier(p_charge_new,true_charges))
sf = 1#14/sum(p_charge_new)
#print(sf)
for t in range(14*48):
    p_charge_new[t] = p_charge_new[t]*sf

#print(brier(p_charge_new,true_charges))
    
#print(brier(p_charge_aj,true_charges))

print(brier(p_charge_new[48*7:],true_charges[48*7:]))
    
print(brier(p_charge_aj[48*7:],true_charges[48*7:]))

#print(brier(p_charge_new[:48*7],true_charges[:48*7]))
    
#print(brier(p_charge_aj[:48*7],true_charges[:48*7]))

# MEA
p_charge_mea = []
with open('mea_av.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        p_charge_mea.append(float(row[0]))
print(brier(p_charge_mea,true_charges[48*7:]))

x_ticks = ['Mon\n0:00','Mon\n12:00','Tue\n0:00','Tue\n12:00','Wed\n0:00',
           'Wed\n12:00','Thu\n0:00','Thu\n12:00','Fri\n0:00','Fri\n12:00',
           'Sat\n0:00','Sat\n12:00','Sun\n0:00','Sun\n12:00','Sun\n23:59']
plt.figure(figsize=(7,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
plt.subplot(3,1,1)
plt.title('Proposed Method')
plt.plot(p_charge_new[48*7:])
#plt.plot(p_charge_new[:48*7])
for t in range(48*7):
    if true_charges[48*7+t] == 1:
    #if true_charges[t] == 1:
        plt.plot([t,t],[0,0.21],c='r',ls=':',lw=2)
plt.ylim(0,1.1*max(p_charge_new))
plt.xlim(0,48*7-1)
plt.ylim(0,0.2)
plt.grid(ls=':')
plt.ylabel('Probability')
plt.xticks(np.linspace(0,48*7-1,num=len(x_ticks)),x_ticks)

plt.subplot(3,1,3)
plt.plot(p_charge_aj[48*7:])
for t in range(48*7):
    if true_charges[48*7+t] == 1:
    #if true_charges[t] == 1:
        plt.plot([t,t],[0,0.21],c='r',ls=':',lw=2)
plt.ylim(0,1.01*max(p_charge_aj))
plt.xlim(0,48*7-1)
plt.ylim(0,0.2)
plt.grid(ls=':')
plt.ylabel('Probability')
plt.title('After final journey')
plt.xticks(np.linspace(0,48*7-1,num=len(x_ticks)),x_ticks)

plt.subplot(3,1,2)
plt.title('Average charging from trial')
plt.plot(p_charge_mea,label='Predicted')
for t in range(48*7):
    if true_charges[48*7+t] == 1:
    #if true_charges[t] == 1:
        if t > 48*6:
            plt.plot([t,t],[0,0.21],c='r',ls=':',lw=2,label='True')
        else:
            plt.plot([t,t],[0,0.21],c='r',ls=':',lw=2)
plt.ylim(0,1.1*max(p_charge_mea))
plt.xlim(0,48*7-1)
plt.ylim(0,0.2)
plt.legend(ncol=2)
plt.grid(ls=':')
plt.xticks(np.linspace(0,48*7-1,num=len(x_ticks)),x_ticks)
#plt.plot(true_charges[48*7:])
plt.ylabel('Probability')
plt.tight_layout()
plt.savefig('../../Dropbox/papers/uncontrolled/img/single_vehicle.eps',
            format='eps', dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()
        
    


