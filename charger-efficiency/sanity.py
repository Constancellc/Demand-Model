
import matplotlib.pyplot as plt

p_ = range(60)

p = [p_[0],p_[25],p_[10],p_[40],p_[20],p_[30],p_[5],p_[35],p_[15],p_[45]]
for i in range(50):
    if i%5 != 0:
        p.append(p_[i])
'''
n = 2
while len(p) < 50:
i = 0
p = []
n_ = 2
while len(p) < 50:
    for i in range(n_):
        num = i*50/n_+0.5*50/n_
        if num not in p:
            p.append(num)
    n_ += 1
'''

t = [0]*30
for i in range(len(p_)):
    t[int(p_[i]*30/60)] += 1

plt.figure()
plt.bar(range(30),t)
plt.show()
print(p)
