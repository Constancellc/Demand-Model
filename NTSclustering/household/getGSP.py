import csv
import requests


class Querier(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def query(self):
        return requests.get(self.endpoint)

locs = []

day = '2017-01-01'

if __name__ == "__main__":
    endpoint = "https://api0.solar.sheffield.ac.uk/pvlive/v1/gsp_list"
    querier = Querier(endpoint)
    response = querier.query()
    data = response.json()['data']
    for r in data:
        locs.append(r)

with open('../../../Documents/simulation_results/NTS/clustering/power/'+\
          'locationsGSP/lat-lon.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID','Lat','Long'])
    for i in range(len(locs)):
        writer.writerow([locs[i][0],locs[i][3],locs[i][4]])
