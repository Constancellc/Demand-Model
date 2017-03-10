import numpy as np
import matplotlib.pyplot as plt
import random
import csv


base = 'evprofiles/'
out = 'evprofiles2/'
for i in range(1,56):   
    results = []
    with open(base+str(i)+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for j in range(0,1440):
                results.append(float(row[j]))

    with open(out+str(i)+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for row in results:
            writer.writerow([row])
