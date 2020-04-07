import csv

res = []
with open('res2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        res.append(row)

s = '12000'
i = 1

res2 = [res[0]]
for i in range(1,len(res)):
    new = res[i][:3]
    if res[i][2] == res[i-1][2]:
        new += [float(res[i][3])-float(res[i-1][3])]
        new += [float(res[i][4])-float(res[i-1][4])]
    else:
        new += [res[i][3],res[i][4]]
    res2.append(new)

with open('res3.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for row in res2:
        writer.writerow(row)
