import numpy as np
import csv
import random

class Drivecycle:
    def __init__(self, distance, version):
        
        # First, import artemis
        v0 = []

        if version == 'urban':
            with open('drivecycles/artemis_urban.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    v0.append(float(row[0])*0.277778)

        elif version == 'rural':
            with open('drivecycles/artemis_rural.csv','rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    v0.append(float(row[0])*0.277778)

        else:
            raise InputError('please enter a valid version of artemis')

        # Then, calculate distance covered by one cycle
        s0 = 0
        for value in v0:
            s0 += value

        v = []
        if s0 >= distance:
            # If the distance covered by one cycle is greater than the trip
            s = 0
            i = 0
            while s <= distance:
                v.append(v0[i])
                s += v0[i]
                i += 1

        else:
            for i in range(0,int(distance/s0)):
                for value in v0:
                    v.append(value)
            s = int(distance/s0)*s0
            
            while s <= distance:
                v.append(v0[i])
                s += v0[i]
                i += 1

        self.velocity = v

        a = [0]

        for i in range(0,len(v)-1):
            a.append(v[i+1]-v[i])

        self.acceleration = a



