import matplotlib.pyplot as plt
import numpy as np
import csv
#from sklearn.cluster import KMeans
import datetime

def generate(t_r,t_t,solar=12000,skip=None):
    scen = []
    dates = []
    rain = []
    temp = []
    p = []
    with open('../../Documents/solar_data_scenarios/net_profile_cleaned_'+\
              str(solar)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            dates.append(row[0])
            dt = datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                                   int(row[0][8:10]))
            if dt == skip:
                continue
            wd = dt.isoweekday()
            if wd > 5:
                continue
            rain.append(float(row[1]))
            temp.append(float(row[2]))
            _p = []
            for i in range(3,len(row)):
                _p.append(float(row[i]))

            p.append(_p)

    # now normalise rain and temp
    mr = sum(rain)/len(rain)
    vr = 0
    mt = sum(temp)/len(temp)
    vt = 0
    for i in range(len(rain)):
        vr += np.power(rain[i]-mr,2)/len(rain)
        vt += np.power(temp[i]-mt,2)/len(rain)

    for i in range(len(rain)):
        rain[i] = (rain[i]-mr)/np.sqrt(vr)
        temp[i] = (temp[i]-mt)/np.sqrt(vt)

    max_d = 1.5

    t_r = (t_r-mr)/np.sqrt(vr)
    t_t = (t_t-mt)/np.sqrt(vt)
    test = [t_r,t_t]

    p_t = 0
    for i in range(len(rain)):
        d = np.sqrt(np.power(test[0]-rain[i],2)+np.power(test[1]-temp[i],2))
        if d < max_d:
            p_t += max_d-d#1/d
            scen.append([max_d-d]+p[i])#[1/d]+p[i])
    
    for i in range(len(scen)):
        scen[i][0] = scen[i][0]/p_t

    return scen

def generate_control(solar=12000,skip=None):
    p = []
    with open('../../Documents/solar_data_scenarios/net_profile_cleaned_'+\
              str(solar)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(p) > 0:
                continue
            dt = datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                                   int(row[0][8:10]))
            if dt == skip:
                continue
            wd = dt.isoweekday()
            if wd > 5:
                continue
            _p = []
            for i in range(3,len(row)):
                _p.append(float(row[i]))

            p.append(_p)
    scen = []
    for i in range(len(p)):
        scen.append([1.0/len(p)]+p[i])

    return scen

def get_single(chosen,solar=12000):
    with open('../../Documents/solar_data_scenarios/net_profile_cleaned_'+\
              str(solar)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            dt = datetime.datetime(int(row[0][:4]),int(row[0][5:7]),
                                   int(row[0][8:10]))
            if dt != chosen:
                continue
            rain = float(row[1])
            temp = float(row[2])
            _p = []
            for i in range(3,len(row)):
                _p.append(float(row[i]))

        return rain,temp,_p
