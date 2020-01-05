# Program for computing the outerbound of caching system, based on the report of S.Shuo
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

# choose delta < 0 or delta >= 0:
delta_option = input("Choose delta < 0 (Press: 0) OR delta >= 0 (Press: 1)?")
delta_option = int(delta_option)


def zero_out(vec, p0, p1, p2, p3, p4, delta):
    vec *= 0
    p0 *= 0
    p1 *= 0
    p2 *= 0
    p3 *= 0
    p4 *= 0
    delta *= 0
    return vec, p0, p1, p2, p3, p4, delta

def create_vec(p0, p1, p2, p3, p4, delta):
    vec = np.hstack([p0.flatten(), p1.flatten(), p2.flatten(), p3, p4, delta])
    return vec

# 1. Init
N = 2
K = 4

A = np.zeros((1, 3*(K-1)**2 + 2*(K-1) + 1))
b = 0

A_eq = np.zeros((1, 3*(K-1)**2 + 2*(K-1) + 1))
b_eq = 0

vec = np.zeros((1, 3*(K-1)**2 + 2*(K-1) + 1))
p0 = np.zeros((K - 1, K - 1))
p1 = np.zeros((K - 1, K - 1))
p2 = np.zeros((K - 1, K - 1))
p3 = np.zeros(K - 1)
p4 = np.zeros(K - 1)
delta = 0

# constraint (1)
(vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
for t in range(1, K):
    p1[t-1, 0] = 1
p3[0] = 1
p2[0, 1] = 1
p0[0, 0] = -1
vec = create_vec(p0, p1, p2, p3, p4, delta)
A = np.vstack([A, vec])
b = np.append(b, 0)


# constraint (2)
for j in range(2, K):
    (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
    for t in range(1, K):
        p1[t-1, j-1] = 1
    p3[j-1] = 1
    p0[0, j-1] = -1
    vec = create_vec(p0, p1, p2, p3, p4, delta)
    A = np.vstack([A, vec])
    b = np.append(b, 0)

# constraint (3)
for i in range(2, K):
    (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
    for t in range(i, K):
        p1[t-1, 0] = 1
    p2[i-1, 1] = 1
    p0[i-1, 0] = -1
    vec = create_vec(p0, p1, p2, p3, p4, delta)
    A = np.vstack([A, vec])
    b = np.append(b, 0)

# constraint (4)
for i in range(2, K):
    for j in range(1, K-i+1):
        (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
        for t in range(i, K):
            p1[t-1, j-1] = 1
        p0[i-1, j-1] = -1
        vec = create_vec(p0, p1, p2, p3, p4, delta)
        A = np.vstack([A, vec])
        b = np.append(b, 0)

# constraint (5)
for i in range(1, K):
    for j in range(2, K-i):
        (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
        p2[i-1, j] = 1
        p2[i-1, j-1] = -1
        vec = create_vec(p0, p1, p2, p3, p4, delta)
        A = np.vstack([A, vec])
        b = np.append(b, 0)

# constraint (6)
(vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
for j in range(1, K):
    p4[j-1] = 1
for j in range(1,K):
    for i in range(1, K-j+1):
        p1[i-1, j-1] = -1
vec = create_vec(p0, p1, p2, p3, p4, delta)
A = np.vstack([A, vec])
b = np.append(b, 0)

# constraint (7)
for i in range(1, K):
    for j in range(2, K-i+1):
        (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
        p2[i-1, j-1] = 1
        p1[i-1, j-1] = -1
        vec = create_vec(p0, p1, p2, p3, p4, delta)
        A = np.vstack([A, vec])
        b = np.append(b, 0)


# constraint (8)
for i in range(1, K):
    (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
    p1[i - 1, 0] = 1
    vec = create_vec(p0, p1, p2, p3, p4, delta)
    A_eq = np.vstack([A_eq, vec])
    b_eq = np.append(b_eq, 0)


# constraint (9): greater than 0, flip the sign
for j in range(2,K):
    (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
    for m in range(j-1, K):
        p3[m-1] = -1
    for m in range(j, K):
        p4[m-1] = -1
    for i in range(1, K-j+1):
        p2[i-1, j-1] = 1
        vec = create_vec(p0, p1, p2, p3, p4, delta)
    A = np.vstack([A, vec])
    b = np.append(b, 0)


# constraint (10): equality constraint
(vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
for m in range(0,K):
    p3[m-1] = 1
for m in range(1,K):
    p4[m-1] = 1
for i in range(1,K):
    for j in range(1,K-i+1):
        p1[i-1, j-1] = i
for j in range(2, K):
    for m in range(j-1, K):
        p3[m-1] = p3[m-1] + 1
    for m in range(j, K):
        p4[m-1] = p4[m-1] + 1
    for i in range(1,K-j+1):
        p2[i-1, j-1] = p2[i-1, j-1] - 1
delta = 1
vec = create_vec(p0, p1, p2, p3, p4, delta)
A_eq = np.vstack([A_eq, vec])
b_eq = np.append(b_eq, 1)


# constraint (11): delta >= 0 or delta < 0
(vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
if delta_option == 1:
    delta = -1
elif delta_option == 0:
    delta = 1
vec = create_vec(p0, p1, p2, p3, p4, delta)
A = np.vstack([A, vec])
b = np.append(b, 0)


# constraints for p0, p1, p2:
# lower right triangle should be zero, others should be [0, 1]
for i in range(1, K):
    for j in range(1, K):
        if (i + j > K):
            (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
            p0[i-1, j-1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta)
            A_eq = np.vstack([A_eq, vec])
            b_eq = np.append(b_eq, 0)


            (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
            p1[i - 1, j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta)
            A_eq = np.vstack([A_eq, vec])
            b_eq = np.append(b_eq, 0)

            (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
            p2[i - 1, j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta)
            A_eq = np.vstack([A_eq, vec])
            b_eq = np.append(b_eq, 0)
        else:
            (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
            p0[i-1, j-1] = -1
            vec = create_vec(p0, p1, p2, p3, p4, delta)
            A = np.vstack([A, vec])
            b = np.append(b, 0)

            (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
            p0[i - 1, j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta)
            A = np.vstack([A, vec])
            b = np.append(b, 1)

            (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
            p1[i-1, j-1] = -1
            vec = create_vec(p0, p1, p2, p3, p4, delta)
            A = np.vstack([A, vec])
            b = np.append(b, 0)

            (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
            p1[i - 1, j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta)
            A = np.vstack([A, vec])
            b = np.append(b, 1)

            (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
            p2[i-1, j-1] = -1
            vec = create_vec(p0, p1, p2, p3, p4, delta)
            A = np.vstack([A, vec])
            b = np.append(b, 0)

            (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
            p2[i - 1, j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta)
            A = np.vstack([A, vec])
            b = np.append(b, 1)

# constraints for p3 and p4:
for i in range(1, K):
    (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
    p3[i - 1] = -1
    vec = create_vec(p0, p1, p2, p3, p4, delta)
    A = np.vstack([A, vec])
    b = np.append(b, 0)

    (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
    p3[i - 1] = 1
    vec = create_vec(p0, p1, p2, p3, p4, delta)
    A = np.vstack([A, vec])
    b = np.append(b, 1)

    (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
    p4[i - 1] = -1
    vec = create_vec(p0, p1, p2, p3, p4, delta)
    A = np.vstack([A, vec])
    b = np.append(b, 0)

    (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
    p4[i - 1] = 1
    vec = create_vec(p0, p1, p2, p3, p4, delta)
    A = np.vstack([A, vec])
    b = np.append(b, 1)


# add constraint on page 3:
(vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
for i in range(1, K):
    for j in range(1, K-i+1):
        p0[i-1, j-1] = i
vec = create_vec(p0, p1, p2, p3, p4, delta)
A = np.vstack([A, vec])
b = np.append(b, 1)


## delete first row of A, b, A_eq, b_eq
A = np.delete(A, 0, 0)
#print(A.shape)
b = np.delete(b, 0, 0)
#print(b.shape)
A_eq = np.delete(A_eq, 0, 0)
#print(A_eq.shape)
b_eq = np.delete(b_eq, 0, 0)
#print(b_eq.shape)


X = []
Y = []

for M in np.linspace(0, 2, 11):
# M = 1/4.0

    # set linear programming
    (vec, p0, p1, p2, p3, p4, delta) = zero_out(vec, p0, p1, p2, p3, p4, delta)
    for j in range(1,K):
        p3[j-1] = 1
    for j in range(1,K):
        p4[j-1] = 1
    for i in range(1,K):
        for j in range(1,K-i+1):
            p1[i-1, j-1] = i-1
    if delta_option == 1:
        delta = (M-1.0)/2.0
    elif delta_option == 0:
        delta = M
    c = -create_vec(p0, p1, p2, p3, p4, delta)


    res = linprog(c, A, b, A_eq, b_eq, bounds=None, options={"disp": True})
    print("result is:", res.x)
    R = np.sum(res.x[3*(K-1)**2 : 3*(K-1)**2+(K-1)*2]) \
        + np.sum([(i-1)*res.x[(K-1)**2 + (i-1)*(K-1) + (j-1)] for i in range(1, K) for j in range(1, K-i+1)]) \
        + 1 - M + delta * res.x[-1]
    X.append(M)
    Y.append(R)
# print("Optimization result: ", res.x)

print("M is: ", X)
print("R is: ", Y)

# plot the data
fig, ax = plt.subplots()
# (2,3)
"""
M_Tian = [0, 1/3.0, 4/3.0, 2]
R_Tian = [2, 4/3.0, 1/3.0, 0]
ax.annotate('(1/3, 4/3)', xy=(1/3.0, 4/3.0), xytext=(0.5, 1.5),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
ax.annotate('(4/3, 1/3)', xy=(4/3.0, 1/3.0), xytext=(1.5, 0.5),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
#  (2,4)
"""
M_Tian = [0, 1/4.0, 6/13.0, 2/3.0, 1, 3/2.0, 2]
R_Tian = [2, 3/2.0, 16/13.0, 1, 2/3.0, 1/4.0, 0]
ax.annotate('(1/4, 3/2)', xy=(1/4.0, 3/2.0), xytext=(1/4.0+0.1, 3/2.0+0.1),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
ax.annotate('(6/13.0, 16/13.0)', xy=(6/13.0, 16/13.0), xytext=(6/13.0+0.1, 16/13.0+0.1),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
ax.annotate('(2/3.0, 1)', xy=(2/3.0, 1), xytext=(2/3.0 + 0.1, 1+0.1),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
ax.annotate('(1, 2/3.0)', xy=(1, 2/3.0), xytext=(1 + 0.1, 2/3.0 + 0.1),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
ax.annotate('(3/2.0, 1/4.0)', xy=(3/2.0, 1/4.0), xytext=(3/2.0 + 0.1, 1/4.0 + 0.1),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )

ax.grid(True)
ax.set_xlabel('M',fontsize=14)
ax.set_ylabel('R',fontsize=14)
ax.set_xlim([-0.02, N+0.02])
ax.set_ylim([-0.02, N+0.02])
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
ax.plot(M_Tian, R_Tian, color='k', label='Tian Computed Outerbound')
ax.plot(X, Y, color='r', label='Shao Computed Outerbound')
ax.legend()

plt.show()

print("A is: ", A)
print("b is: ", b)
print("A_eq is: ", A_eq)
print("b_eq is: ", b_eq)

# set the limits


