import numpy as np
import matplotlib.pyplot as plt
import random
import csv

from cvxopt import matrix, spdiag, solvers, sparse

n = 2
t = 4

I = spdiag([1]*t)
M = sparse([[I]*n]*n)
print M
