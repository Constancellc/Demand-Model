import csv
import random
import numpy as np
from sklearn import svm

stem = '../../Documents/My_Electric_avenue_Technical_Data/training/'

obs = ['BL01.csv','BL02.csv','BL03.csv','BL04.csv','BL05.csv','BL06.csv',
       'BL08.csv','CC01.csv','CC02.csv','CC04.csv','CC05.csv','CC06.csv',
       'CC07.csv','CC09.csv','CC10.csv','CRG01.csv','CRG02.csv','CRG03.csv',
       'CRG04.csv','CRG06.csv','CRG07.csv','CRG08.csv','CRG09.csv','CRG10.csv',
       'CRG11.csv','GC01.csv','GC03.csv','GC04.csv','GC05.csv','GC06.csv',
       'GC07.csv','GC08.csv','GC09.csv','GC10.csv','GC11.csv','JD01.csv',
       'JD02.csv','JD03.csv','JD04.csv','JD05.csv','JD06.csv','JD07.csv',
       'JD09.csv','JD10.csv','JD11.csv','MC01.csv','MC02.csv','MC03.csv',
       'MC04.csv','MC05.csv','MC06.csv','MC07.csv','MC09.csv','MC10.csv',
       'SS01.csv','SS02.csv','SS03.csv','SS04.csv','SS05.csv','SS06.csv',
       'SS07.csv','SS08.csv','SS09.csv','SS10.csv','SS11.csv','SS201.csv',
       'SS202.csv','SS203.csv','SS204.csv','SS205.csv','SS206.csv','SS207.csv',
       'SS208.csv','SS209.csv','SS210.csv','SS211.csv','SS212.csv',
       'ST1000.csv','ST1001.csv','ST1002.csv','ST1003.csv','ST1004.csv',
       'ST1005.csv','ST1006.csv','ST1007.csv','ST1009.csv','ST1010.csv',
       'ST1011.csv','ST1012.csv','ST1013.csv','ST1014.csv','ST1015.csv',
       'ST1017.csv','ST1018.csv','ST1019.csv','ST1020.csv','ST1021.csv',
       'ST1022.csv','ST1023.csv','ST1027.csv','ST1028.csv','ST1029.csv',
       'ST1030.csv','ST1031.csv','ST1032.csv','ST1034.csv','ST1035.csv',
       'ST1036.csv','ST1037.csv','ST1038.csv','ST1039.csv','ST1041.csv',
       'ST1042.csv','ST1043.csv','ST1044.csv','ST1045.csv','ST1046.csv',
       'ST1047.csv','ST1048.csv','ST1049.csv','ST1050.csv','ST1051.csv',
       'ST1052.csv','ST1053.csv','ST1054.csv','ST1055.csv','ST1056.csv',
       'ST1057.csv','ST1058.csv','ST1059.csv','ST1060.csv','ST1061.csv',
       'ST1062.csv','ST1063.csv','ST1064.csv','ST1065.csv','ST1066.csv',
       'ST1067.csv','ST1068.csv','ST1069.csv','ST1070.csv','ST1071.csv',
       'ST1072.csv','ST1073.csv','ST1074.csv','ST1075.csv','ST1076.csv',
       'ST1077.csv','ST1078.csv','ST1079.csv','ST1080.csv','ST1081.csv',
       'ST1082.csv','ST1083.csv','ST1084.csv','ST1085.csv','ST1086.csv',
       'ST1087.csv','ST1090.csv','ST1091.csv','ST1092.csv','ST1093.csv',
       'ST1094.csv','ST1095.csv','ST1096.csv','ST1097.csv','ST1098.csv',
       'ST1099.csv','ST1100.csv','ST1101.csv','ST1102.csv','ST1103.csv',
       'ST1104.csv','ST1105.csv','ST1106.csv','ST1107.csv','ST1108.csv',
       'ST1110.csv','ST1111.csv','ST1112.csv','ST1113.csv','ST1114.csv',
       'SW01.csv','SW03.csv','SW04.csv','SW05.csv','SW06.csv','SW07.csv',
       'SW09.csv','SW10.csv','SW11.csv','SW12.csv','WC01.csv','WC02.csv',
       'WC03.csv','WC04.csv','WC05.csv','WC06.csv','WC07.csv','WC08.csv',
       'WC09.csv','WC11.csv','YH01.csv','YH02.csv','YH03.csv','YH04.csv',
       'YH05.csv','YH06.csv','YH08.csv','YH09.csv','YH10.csv','YH11.csv',
       'YH12.csv','YH13.csv','YH14.csv']

data = []
for file in obs:
    v = []
    c = []
    with open(stem+file,'rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            v.append(float(row[0]))
            c.append(float(row[1]))

    nDays = int(len(v)/48)

    for d in range(nDays-1):
        if sum(v[d*48:d*48+48]) == 0:
            continue
        data.append(v[d*48:d*48+48]+c[d*48+24:d*48+72])
        '''

    for t in range(48,len(v)):
        if sum(v[t-48:t]) == 0:
            continue
        data.append(v[t-48:t]+c[t-48:t])
        '''

random.shuffle(data)
print(len(data))
data = data[:10000] # save yo storage space

with open(stem+'X.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row[:48])
        
with open(stem+'y.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(row[48:])
