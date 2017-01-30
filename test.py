import numpy as np
import random

oldLog = []
oldLog.append([324,17])
oldLog.append([2,10])
oldLog.append([154,11])

newLog = []

while len(oldLog) > 0:
    earliest = oldLog[0]
    for j in range(1,len(oldLog)):
        if oldLog[j][0] < earliest[0]:
           earliest = oldLog[j]

    newLog.append(earliest)
    oldLog.remove(earliest)

print newLog
print oldLog
