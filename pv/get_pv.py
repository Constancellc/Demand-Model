#!/usr/bin/python2.7
"""
A script to download all historic data from the Sheffield Solar PV_Live API and save in CSV format.

Jamie Taylor 2015-10-13
"""

from datetime import datetime, timedelta, date
import requests
import json
import sys

def main():
    ##### CONFIG #####
    block_size = 100 #Number of days to query at a time
    username = "pvlive"
    password = ""
    outfile = "GBPV_data.csv" #Where to save the csv file
    quiet = False #Set to True to avoid printing all the data to screen/stdout
    version = "0.1"
    ##################

    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        duration = int(round(float(sys.argv[1]))) #Numbers of days of historic data to get
    else:
        duration = 1825 #Numbers of days of historic data to get (1825 == 5 years)
    latest_timestamp = datetime.now() #Initialise to now
    earliest_timestamp = latest_timestamp - timedelta(days=duration)

    request_start = earliest_timestamp #Initialise
    printer = [] #Initialise
    if block_size > duration:
        block_size = duration

    while request_start < latest_timestamp:
        #import pdb; pdb.set_trace() #for debugging
        if latest_timestamp - request_start < timedelta(days=block_size):
            request_end = latest_timestamp
        else:
            request_end = request_start + timedelta(days=block_size)
        if not quiet:
            print ("Requesting data between %s and %s for version %s..."
                   % (request_start.strftime("%Y-%m-%dT%H:%M:%S"),
                      request_end.strftime("%Y-%m-%dT%H:%M:%S"),
                      version))
        url = ('http://www.solar.sheffield.ac.uk/ssfdb3/sql/call pv_generation(0,"%s","%s")'
               % (request_start.strftime("%Y-%m-%dT%H:%M:%S"),
                  request_end.strftime("%Y-%m-%dT%H:%M:%S")))
        resultpage = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password)).text #return the web page (JSON) as a string
        data = json.loads(resultpage) #translate the JSON string to a python dictionary

        if len(data[0]["data"]) > 0:
            columns = [x["column"] for x in data[0]["meta"]]
            #if not quiet:
                #print "    " + ",".join(columns)
            if len(printer) == 0:
                printer.append(",".join(columns))
            for row in data[0]["data"]:
                #print row
                row = [str(x) for x in row]
                #if not quiet:
                    #print "    " + ",".join(row)
                printer.append(",".join(row))
        request_start += timedelta(days=block_size)

    with open(outfile, "w") as f:
        for s in printer:
            f.write(s + "\n")

if __name__ == "__main__":
    main()
