from cvxopt import matrix, spdiag, solvers, sparse

t = 3
n = 2

A_sv = matrix(0,(t,t*n)) # sv: stack vehicles - calculates total v(t)
for i in range(0,t):
    for j in range(0,n):
        A_sv[t*t*j+i+i*t] = 1

print A_sv
