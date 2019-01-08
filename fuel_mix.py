# import the standard stuff
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

# installed capacity
steam = 16334
combined = 32887
nuclear = 9361
gas = 1680
hydro_flow = 1623
hydro_pump = 2744
wind = 8529
solar = 2172
renew_oth = 5964

f = steam+combined+nuclear+gas+hydro_pump+renew_oth
print(steam+combined+nuclear+gas+hydro_flow+hydro_pump+wind+solar+renew_oth)
flat = [f]*1440

plt.figure()
plt.plot(flat)
plt.show()
