import csv

fileStem1 = '../../Documents/NationalProfiles/'
fileStem2 = '../../Documents/NationalProfilesRT/'


ms = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun',
      '7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
for m in range(1,13):
    month = str(m)
    print(month)

    en = 0
    with open(fileStem1+ms[month]+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            en += float(row[3])
    print(en)
    en = 0
    with open(fileStem2+ms[month]+'RT.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            en += float(row[3])
    print(en)
