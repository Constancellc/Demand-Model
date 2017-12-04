import csv
from SMenergyPrediction import HouseholdElectricityDemand


for i in range(1,60):
    test = HouseholdElectricityDemand(ACORNType=str(float(i)))

    profiles = test.getProfile(3,1,nProfiles=1000)

    J = len(profiles)
    if J == 0:
        continue
    print(J)

    if J > 1000:
        J = 1000

    with open('../../Documents/HH_demand_by_acorn_type/'+str(i)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for j in range(J):
            writer.writerow(profiles[j])
