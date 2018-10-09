import csv
import matplotlib.pyplot as plt

data = '../../../Documents/elec_demand/MSOA_domestic_electricity_2016.csv'

vehicles = '../../../Documents/simulation_results/NTS/clustering/power/locationsLA/'

p1_winter = []
p1_spring = []
p1_summer = []
p1_autumn = []

p2_winter = []
p2_spring = []
p2_summer = []
p2_autumn = []
with open('../../../Documents/elec_demand/ProfileClass1.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p1_winter.append(float(row[-3]))
        p1_spring.append(float(row[-6]))
        p1_summer.append(float(row[-9]))
        p1_autumn.append(float(row[1]))
        
with open('../../../Documents/elec_demand/ProfileClass2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        p2_winter.append(float(row[-3]))
        p2_spring.append(float(row[-6]))
        p2_summer.append(float(row[-9]))
        p2_autumn.append(float(row[1]))

p1 = p1_winter
p2 = p2_winter

s1 = sum(p1)
s2 = sum(p2)

r1 = sum(p1_winter)/(sum(p1_winter)+sum(p1_spring)+sum(p1_summer)+\
                     sum(p1_autumn))
r2 = sum(p2_winter)/(sum(p2_winter)+sum(p2_spring)+sum(p2_summer)+\
                     sum(p2_autumn))

print(r1)
print(r2)
for t in range(48):
    p1[t] = p1[t]/s1
    p2[t] = p2[t]/s2

E7 = {}
Std = {}
n = {}
with open(data,'r+',encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        LA = row[1]
        if LA == '':
            continue
        if LA not in E7:
            E7[LA] = 0
            Std[LA] = 0
            n[LA] = 0

        E7[LA] += float(row[4])# total kWh E7
        Std[LA] += float(row[5])# total kWh standard
        n[LA] += int(row[9])# total number of customers

results = {}       
for la in n:
    e = E7[la]*2*r2/(365*0.25)
    s = Std[la]*2*r1/(365*0.25)
    p = []
    for t in range(48):
        new = (p1[t]*e+p2[t]*s)/n[la]
        for tt in range(30):
            p.append(new)

    old_peak = max(p)

    t = 0
    try:
        with open(vehicles+la+'.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if t < 1440:
                    p[t] += float(row[1])/50
                    t += 1

        new_peak = max(p)
    except:
        continue

    results[la] = [old_peak,new_peak]

with open(vehicles+'peaks.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LA Code','Old Peak','New Peak'])
    for la in results:
        writer.writerow([la]+results[la])

