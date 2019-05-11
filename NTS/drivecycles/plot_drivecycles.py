import csv
import matplotlib.pyplot as plt

u = []
r = []
h = []

with open('artemis_urban.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        u.append(float(row[0]))

with open('artemis_rural.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        r.append(float(row[0]))

with open('artemis_mway130.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        h.append(float(row[0]))

plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 12
plt.plot(u)
plt.ylabel('Speed (kmph)')
plt.xlabel('Time (s)')
plt.xlim(0,len(u))
plt.tight_layout()
plt.ylim(0,60)
plt.grid(ls=':')
plt.savefig('artemis_urban.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)

plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 12
plt.plot(r)
plt.ylabel('Speed (kmph)')
plt.xlabel('Time (s)')
plt.xlim(0,len(r))
plt.tight_layout()
plt.ylim(0,115)
plt.grid(ls=':')
plt.savefig('artemis_rural.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0)

plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 12
plt.plot(h)
plt.ylabel('Speed (kmph)')
plt.xlabel('Time (s)')
plt.xlim(0,len(h))
plt.tight_layout()
plt.ylim(0,140)
plt.grid(ls=':')
plt.savefig('artemis_mtrway.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0.)
plt.show()
