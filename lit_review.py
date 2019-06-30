import matplotlib.pyplot as plt
import numpy as np

def plot_bubble(x,y,n):
    if n <=8:
        angle = 2*np.pi/n
        r = 0.2
        a = []
        b = []
        for i in range(n):
            a.append([x+r*np.cos(i*angle)])
            b.append([x+r*np.sin(i*angle)])
        plt.scatter(a,b,marker='+',s=4)
        
def plot_bubble2(x,y,n):
    plt.scatter([x],[y],s=n*20,c='#CCCCFF')
    plt.annotate(n,(x-0.08,y-0.08))
plt.figure()

plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 10

plt.xlim(0,9)
plt.xticks(range(1,9),['No Impact','National\nEnergy','National\nPower',
                       'Distribution Loading\nCase Study',
                       'Distribution Power\nQuality Case Study','Transmission',
                       'Distribution\nLoading','Distribution\nPower Quality'],
           rotation=90)
plt.ylim(0,6)
plt.yticks(range(1,6),['Uncontrolled','Tariff Based','Ancillary\nServices',
                       'Heuristic','Controlled'])
#plt.scatter([3],[1],s=)
plot_bubble2(3,1,5) # uncontrolled national power
plot_bubble2(4,1,7) # uncontrolled case study - loading
plot_bubble2(5,1,9) # uncontrolled case study - power flow
plot_bubble2(6,1,3) # uncontrolled transmission

plot_bubble2(5,2,3) # tariff case study - power flow

plot_bubble2(4,5,9) # controlled case study - power flow

plt.ylabel('Level of Control',fontweight='bold')
plt.xlabel('System Impact Fidelity',fontweight='bold')
plt.grid(ls=':')
plt.tight_layout()
#plt.savefig('../../Dropbox/thesis/chapter2/img/literature.eps', format='eps',
#            dpi=1000, bbox_inches='tight', pad_inches=0.1)
plt.show()
