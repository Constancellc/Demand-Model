import matplotlib.pyplot as plt
import numpy as np

sc = {0.1:[10,12],0.1:[10,16],0.4:[14,30],0.3:[20,38],0.1:[31,42]}

p = [0.0]*48
for s in sc:
    for t in range(48):
        if t>sc[s][1] or t < sc[s][0]:
            p[t] += s

plt.figure()
plt.plot(p)
plt.show()
