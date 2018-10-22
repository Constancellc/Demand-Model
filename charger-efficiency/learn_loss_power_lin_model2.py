import matplotlib.pyplot as plt
import numpy as np

p = np.arange(0.01,1.1,0.01)

x = []
y = []

pts = [[0.0,0.0],
       [0.0026087358020132623, 0.005042016806722893],
       [0.047326622956875175, 0.07731092436974807],
       [0.08943577430972405, 0.14453781512605057],
       [0.11510758149413625, 0.2100840336134454],
       [0.1353772278142027, 0.27226890756302535],
       [0.15830178225136216, 0.3378151260504202],
       [0.18118016437344164, 0.4050420168067228],
       [0.20140363837842856, 0.4689075630252101],
       [0.235271031489519, 0.5361344537815126],
       [0.2819512420352759, 0.6369747899159662],
       [0.3780820020315818, 0.73781512605042],
       [0.48141564318034913, 0.7764705882352939],
       [0.5768307322929169, 0.8033613445378149],
       [0.6423492473912644, 0.818487394957983],
       [0.7106611875519444, 0.8319327731092434],
       [0.7789269553975438, 0.8470588235294115],
       [0.8833225597931478, 0.8470588235294115],
       [0.9704497183488783, 0.8756302521008401]]

train = {}
for pp in pts:
    x.append(pp[0])
    y.append(pp[1])
    train[round(pp[0],2)] = pp[1]
    
def f(a,b,c,d):

    # x is the crossover point
    xx = (c-a)/(b-d)
    eff = []
    for i in range(len(p)):
        if p[i] < xx:
            eff.append(a + b*p[i])
        else:
            eff.append(c + d*p[i])
            
    error = 0
    for i in range(len(p)):
        if p[i] in train and p[i] > 0.2:
            error += abs(eff[i]-train[p[i]])
    return [eff,error]

best = None
lowest = 10000000
for aa in [0]:
    for bb in np.arange(1,2,0.01):
        for cc in np.arange(0.6,0.8,0.01):
            for dd in np.arange(0,0.2,0.01):
                [eff,error] = f(aa,bb,cc,dd)
                if error < lowest:
                    best = [aa,bb,cc,dd]
                    lowest = error
                    eff_ = eff

print(best)

plt.figure()
plt.plot(p,eff_)
plt.scatter(x,y)
plt.ylim(0,1)
plt.show()