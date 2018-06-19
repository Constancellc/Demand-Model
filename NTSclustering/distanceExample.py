import matplotlib.pyplot as plt
import scipy.ndimage
plt.figure(1)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'

a = [0.0]*48
b = [0.0]*48
c = [0.0]*48

a[12] = 1
b[13] = 1
c[20] = 1
c[22] = 1
a[35] = 1
b[36] = 1

titles = {1:'a',2:'b',3:'c'}
lines = {1:a,2:b,3:c}

for n in lines:
    plt.subplot(3,1,n)
    plt.plot(lines[n])
    plt.title('('+titles[n]+')',y=0.6)
    plt.grid()
    plt.xlim(0,47)
    plt.ylim(0,1)

plt.tight_layout()

plt.figure(2)
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '8'

a1 = scipy.ndimage.filters.gaussian_filter1d(a,0.5)
b1 = scipy.ndimage.filters.gaussian_filter1d(b,0.5)
c1 = scipy.ndimage.filters.gaussian_filter1d(c,0.5)

a3 = scipy.ndimage.filters.gaussian_filter1d(a,2)
b3 = scipy.ndimage.filters.gaussian_filter1d(b,2)
c3 = scipy.ndimage.filters.gaussian_filter1d(c,2)

a2 = scipy.ndimage.filters.gaussian_filter1d(a,1)
b2 = scipy.ndimage.filters.gaussian_filter1d(b,1)
c2 = scipy.ndimage.filters.gaussian_filter1d(c,1)

lines1 = {1:a1,2:b1,3:c1}
lines2 = {1:a3,2:b3,3:c3}
lines = {1:a2,2:b2,3:c2}

for n in lines:
    plt.subplot(3,1,n)
    plt.plot(lines1[n],label='0.5 std')
    plt.plot(lines[n],label='1.0 std')
    plt.plot(lines2[n],label='2.0 std')
    plt.title('('+titles[n]+')',y=0.6)
    plt.grid()
    plt.xlim(0,47)
    plt.ylim(0,0.8)
plt.legend()
plt.tight_layout()
plt.show()
