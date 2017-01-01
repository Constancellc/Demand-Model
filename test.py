import datetime


times = []

for hour in range(0,24):
    for minute in range(0,60):
        times.append(datetime.time(hour,minute))

print times
