# Demand-Model

There are several functionalities within this folder.

******************
vehicleOriented.py
******************
This contains all the classes necessary to run the agent-based simulation. This includes the following:
- Vehicle 
- JourneyPool 
- Agent
- Fleet
- ChargingScheme
- Simulation

***************
vehicleModel.py
***************
This contains the class Drivecycle which imports the correct version of Artemis and loops it until the required distance has been obtained.

***************
powerPredict.py
***************
This runs the ‘journey oriented’ model which uses monte carlo methods to predict vehicle demand. Some large number of journeys are randomly generated, distributed through time (month, day, hour) and space (type of region).

OUTPUTS:
- a csv file for each month and region type, stored in the uk-wide folder, containing the minute by minute predicted power demand
- ‘number.csv’ a file containing the journeys per member of the relevant population which were simulated for each region, month and day. This will be used in later models to determine how many journeys a population will generate.

*************
plotDemand.py
*************
This utilises the output of the ‘powerPredict’ simulation

INPUTS:
- the region type of the area concerned
- the population of the area concerned

OUTPUTS:
- A figure containing 12 subplots, one for each month. Each plot displays the predicted power requirements throughout the day with one line per day of the week.



—————————————————————————————————————————————————————————————————————————————————————
in ‘old’ folder:                                            (ie. probably not useful)
—————————————————————————————————————————————————————————————————————————————————————

***************
testCharging.py
***************
Takes a specific day of the week, month, region type and population then randomly generates a bunch of journeys which are stored in a (large) csv file.

**************
chargePlots.py
**************
Exploits the results of testCharging and predicts the charge power. Imports all of the generated journeys and assumes charging immediately after completion.
