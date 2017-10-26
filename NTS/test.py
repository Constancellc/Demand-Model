from NTSenergyPrediction import BaseLoad, EnergyPrediction


run = EnergyPrediction('3','3',regionType='4')

b = BaseLoad('3','3',36)
bl = b.getLoad(population=run.nPeople)

run.getClusteredOptimalChargingProfile(3,bl)
