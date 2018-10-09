
#!/usr/bin/python3

"""

Minimal Python to query the PV_Live API (V1)

@author: Sheffield Solar

@date 23 Apr 2018

"""

import requests
import csv

class Querier(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def query(self):
        return requests.get(self.endpoint)

gen = {}
for day in range(2,32):
    if day < 10:
        d = '0'+str(day)
    else:
        d = str(day)
        
    day = '2017-01-'+d

    if __name__ == "__main__":
        for rn in range(1,328):
            endpoint = "https://api0.solar.sheffield.ac.uk/pvlive/v1?region_id="+\
                       str(rn)+"&start="+day+"T00:00:00&end="+day+"T23:30:00"
            querier = Querier(endpoint)
            response = querier.query()
            data = response.json()['data']
            gen[rn] = []
            for t in data:
                gen[rn].append(t[2])

    with open('../../../Documents/simulation_results/NTS/clustering/power/'+\
              'locationsGSP/'+day+'.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Region']+list(range(1,49)))
        for rn in gen:
            writer.writerow([rn]+gen[rn])
