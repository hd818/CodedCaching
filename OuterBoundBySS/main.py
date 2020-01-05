# Program for computing the outerbound of caching system, based on the report of S.Shuo
import numpy as np
from scipy.optimize import linprog
from findIndex import findIndex
# 1. just append vectors
N = 3
K = 4
alpha = -1

x = np.zeros(3*(K-1)**2 + 2*K +2)
A_ub = np.zeros_like(x)

# Coefficient (6)
A_eq = np.zeros_like(x)
vec =  np.zeros_like(x)
for j in range(2, K):
    vec += findIndex(K, "p3", j-1, K-1) + findIndex(K, "p4", j, K-1) - findIndex(K, "p2", 1, K-j, j)
for i in range(1, K):
    vec += i * findIndex(K, "p1", 1, K-i,i)
A_eq = vec + findIndex(K, "p3", 0, K-1) + findIndex(K,"p4", 1, K-1) + findIndex(K, "delta", 0, 1)
b_eq = 1

# Constraint (2)
tmp = np.zeros_like(x)
for i in range(1, K):
    tmp += (i-1)*findIndex(K, "p1", 1, K-i, i)
A_ub = findIndex(K, "p3", 1, K-1) + findIndex(K, "p4", 1, K-1) + findIndex(K, "p3", 1, K-1) + tmp + (-1) * findIndex(K, "y", 0, 1) - 1/2 * findIndex(K, "delta", 0, 1)
b_ub = -1

# Constraint (3)
vec = findIndex(K, "y", 0, 1) - alpha * findIndex(K, "M", 0, 1) - findIndex(K, "R", 0, 1)
A_ub = np.r_[A_ub, vec]
b_ub = np.r_[b_ub, 0]

# Constraint (4)
vec = -1 * findIndex(K, "delta", 0, 1)
A_ub = np.r_[A_ub, vec]
b_ub = np.r_[b_ub, 2-2*alpha]

# Constraint (5)
vec = -1 * findIndex(K, "delta", 0, 1)
A_ub = np.r_[A_ub, vec]
b_ub = np.r_[b_ub, 0]

# Constraint (7)
for j in range(2, K):
    vec = -( findIndex(K, "p3", j-1, K-1) + findIndex(K,"p4", j, K-1) - findIndex(K, "p2", 1, K-j, j) )
    A_ub = np.r_[A_ub, vec]
    b_ub = np.r_[b_ub, 0]

# Constraint (8)
vec = findIndex(K, "p1", 1, K-1, 1) + findIndex(K, "p3", 1, 1) + findIndex(K, "p2", 1, 1, 2) - findIndex(K, "p0",0, 1, 1)
A_ub = np.r_[A_ub, vec]
b_ub = np.r_[b_ub, 0]

# Constraint (9)
for j in range(1, K):
    vec = findIndex(K, "p1", 1, K-1, j) + findIndex(K, "p3", j, j) - findIndex(K, "p0", j, j, 1)
    A_ub = np.r_[A_ub, vec]
    b_ub = np.r_[b_ub, 0]

# Constraint (10)
tmp = np.zeros_like(x)
for i in range(1, K):
    tmp += findIndex(K, "p1", i, K-1, 1) + findIndex(K, "p2", i, i, 2) - findIndex(K, "p0", i, i, 1)
    A_ub = np.r_[A_ub, vec]
    b_ub = np.r_[b_ub, 0]

# Constraint (11)
# res = linprog(c, A_ub=A, b_ub=b, bounds=(x0_bounds, x1_bounds),
#                options={"disp": True})