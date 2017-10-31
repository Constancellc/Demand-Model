import matplotlib.pyplot as plt

plt.figure(1)

plt.plot([0,1,1,2,2,3,4,5,5,6,6,7,8],[0,0,1,1,0,0,0,0,1,1,0,0,0],label='x')
plt.plot([0,1,2,2,3,3,4,5,6,6,7,7,8],[0,0,0,1,1,0,0,0,0,1,1,0,0],label='y')
plt.legend()
plt.show()
