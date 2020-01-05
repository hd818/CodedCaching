"""
Purpose: This program is to test if usgin I/Q/Bar copies for the Jesus Gomez scheme, what is the number of redundancies we still have in the transmissions 

Author: Kai Zhang

Data: 11/6/2018

Email: kaizhang@tamu.edu
"""
import numpy as np
from scipy import special as sp
import matplotlib.pyplot as plt


""" 
1. System parameters
"""

from find_leaders import find_leaders
from generate_cache import generate_cache
from generate_demands import generate_demands
from find_IQBarAssignment import find_IQBarAssignment
from generate_transmission import generate_transmission
from GF import GF

gf = GF(2)

N = 5
K = 7

demands = generate_demands(N, K)
R = np.zeros(K)
M = np.zeros(K)

M[0] = 0
R[0] = N

for r in range(1, K):
    R_r = 0
    print("Current r is:", r)
    for d in demands:
        # print("Current demand is:", d)
        leaders = find_leaders(d)
        R_d = 0
        for i in range(len(leaders)):
            # print(" \t Current user is:", leaders[i])

            cache, set_R = generate_cache(N, K, r, leaders[i])
            # print(cache)
            # print(set_R)

            assignment = find_IQBarAssignment(K, d, i)
            transmissions = generate_transmission(N, K, r, d, leaders[i], set_R, assignment)
            # print("Cache size is:", cache.shape[0])
            # print("transmissions:", transmissions)


            # calculate the R of this leader, then multiply by the number of users requesting this file
            R_l = gf.matrix_rank(np.matrix(transmissions))
            # print("Transmissions is {} ".format(R_l))
            R_d += R_l * d[i]
        # print("No. of transmissions for all users of this file is {} ".format(R_l))
        R_r = max(R_r, R_d)

    # print("The number of cache is:", cache.shape[0])
    # print("The number of transmissions is:", R_r)
    M[r] = (cache.shape[0] + (K - 1)* int(sp.binom(K - 2, r - 1)) * N * 2) / (int(sp.binom(K-1, r)) * K * 2)
    R[r] = R_r / (int(sp.binom(K-1, r)) * K * 2)
    # print("===================")
print(M)
print(R)


# Plot Tian transmission
M_Tian = np.zeros(K+1)
R_Tian = np.zeros(K+1)
for t in range(K+1):
    M_Tian[t] = t * ((N-1)*t+K-N)/K/(K-1)
    R_Tian[t] = N*(K-t)/K

# Yu transmission
Ned = min(K, N)
M_Yu = np.zeros(K + 1)
R_Yu = np.zeros(K + 1)
for t in range(0, K):
    M_Yu[t] = N / K * t
    if K - Ned >= t + 1:
        R_Yu[t] = (sp.binom(K, t + 1) - sp.binom(K - Ned, t + 1)) / sp.binom(K, t)
    else:
        R_Yu[t] = sp.binom(K, t + 1) / sp.binom(K, t)

M_Yu[-1:] = N
R_Yu[-1:] = 0

fig = plt.figure()
plt.plot(M, R, 'b-o', M_Tian, R_Tian, 'r-*', M_Yu, R_Yu, 'g-d')
fig.suptitle("N={}, K={}".format(N ,K))
plt.show()

plt.close



