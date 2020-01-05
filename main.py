# Program for computing the outerbound of caching system, based on the report of S.Shuo
import numpy as np
from scipy.optimize import linprog

def zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M):
    vec = []
    p0 = np.zeros((K - 1, K - 1))
    p1 = np.zeros((K - 1, K - 1))
    p2 = np.zeros((K - 1, K - 1))
    p3 = np.zeros((K - 1, 1))
    p4 = np.zeros((K - 1, 1))
    delta = 0
    y = 0
    R = 0
    M = 0
    return vec, p0, p1, p2, p3, p4, delta, y, R, M

def create_vec(p0, p1, p2, p3, p4, delta, y, R, M):
    vec = np.append(p0.flatten(), p1.flatten())
    vec = np.append(vec, p2.flatten())
    vec = np.append(vec, p3)
    vec = np.append(vec, p4)
    vec = np.append(vec, delta)
    vec = np.append(vec, y)
    vec = np.append(vec, R)
    vec = np.append(vec, M)
    return vec

# 1. Init
N = 2
K = 4

alpha = 1

A = np.zeros((1, 3*(K-1)**2 + 2*(K-1) + 4))
b = 0

A_eq = np.zeros((1, 3*(K-1)**2 + 2*(K-1) + 4))
b_eq = 0

vec = []
p0 = np.zeros((K - 1, K - 1))
p1 = np.zeros((K - 1, K - 1))
p2 = np.zeros((K - 1, K - 1))
p3 = np.zeros((K - 1, 1))
p4 = np.zeros((K - 1, 1))
delta = 0
y = 0
R = 0
M = 0

# constraint (1)
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
for t in range(1, K):
    p1[t-1][0] = 1
p3[0] = 1
p2[0][1] = 1
p0[0][0] = -1
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, 0)



# constraint (2)
for j in range(2, K):
    (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
    for t in range(1, K):
        p1[t-1][j-1] = 1
    p3[j-1] = 1
    p0[0][j-1] = -1
    vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
    A = np.vstack([A, vec])
    b = np.append(b, 0)

# constraint (3)
for i in range(2, K):
    (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
    for t in range(i, K):
        p1[t-1][0] = 1
    p2[i-1][1] = 1
    p0[i-1][0] = -1
    vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
    A = np.vstack([A, vec])
    b = np.append(b, 0)

# constraint (4)
for i in range(2, K):
    for j in range(1, K-i+1):
        (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
        for t in range(i, K):
            p1[t-1][j-1] = 1
        p0[i-1][j-1] = -1
        vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
        A = np.vstack([A, vec])
        b = np.append(b, 0)

# constraint (5)
for i in range(1, K):
    for j in range(2, K-i):
        (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
        p2[i-1][j] = 1
        p2[i-1][j-1] = -1
        vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
        A = np.vstack([A, vec])
        b = np.append(b, 0)

# constraint (6)
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
for j in range(1, K):
    p4[j-1] = 1
for j in range(1,K):
    for i in range(1, K-j+1):
        p1[i-1][j-1] = -1
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, 0)

# constraint (7)
for i in range(1, K):
    for j in range(2, K-i+1):
        (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
        p2[i-1][j-1] = 1
        p1[i-1][j-1] = -1
        vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
        A = np.vstack([A, vec])
        b = np.append(b, 0)


# constraint (8)
for i in range(1, K):
    (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
    p1[i - 1][0] = 1
    vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
    A_eq = np.vstack([A_eq, vec])
    b_eq = np.append(b_eq, 0)


# constraint (9): greater than 0, flip the sign
for j in range(2,K):
    (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
    for m in range(j-1, K):
        p3[m-1] = -1
    for m in range(j, K):
        p4[m-1] = -1
    for i in range(1, K-j+1):
        p2[i-1][j-1] = 1
        vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
    A = np.vstack([A, vec])
    b = np.append(b, 0)



# constraint (10): equality constraint
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
for m in range(0,K):
    p3[m-1] = 1
for m in range(1,K):
    p4[m-1] = 1
for i in range(1,K):
    for j in range(1,K-i+1):
        p1[i-1][j-1] = i
for j in range(2, K):
    for m in range(j-1, K):
        p3[m-1] = p3[m-1] + 1
    for m in range(j, K):
        p4[m-1] = p4[m-1] + 1
    for i in range(1,K-j+1):
        p2[i-1][j-1] = p2[i-1][j-1] - 1
delta = 1
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A_eq = np.vstack([A_eq, vec])
b_eq = np.append(b_eq, 1)


# constraint (11): greater than, flip sign
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
delta = -1
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, 0)



# constraint (12)
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
for j in range(1,K):
    p3[j-1] = 1
for j in range(1,K):
    p4[j-1] = 1
for i in range(1,K):
    for j in range(1,K-i+1):
        p1[i-1][j-1] = i-1
delta = -1.0/2.0
y = -1
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, -1)


# constraint (13)(1)
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
delta = -1.0/2.0
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, -(1-alpha))

# constraint (13)(2)
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
y = 1
R = -1
M = -1*alpha
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, 0)

# constraints: lower right triangle should be zero, others should be [0, 1]
for i in range(1, K):
    for j in range(1, K):
        if (i + j > K):
            (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
            p0[i-1][j-1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
            A_eq = np.vstack([A_eq, vec])
            b_eq = np.append(b_eq, 0)


            (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
            p1[i - 1][j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
            A_eq = np.vstack([A_eq, vec])
            b_eq = np.append(b_eq, 0)

            (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
            p2[i - 1][j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
            A_eq = np.vstack([A_eq, vec])
            b_eq = np.append(b_eq, 0)
        else:
            (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
            p0[i-1][j-1] = -1
            vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
            A = np.vstack([A, vec])
            b = np.append(b, 0)

            (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
            p0[i - 1][j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
            A = np.vstack([A, vec])
            b = np.append(b, 1)

            (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
            p1[i-1][j-1] = -1
            vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
            A = np.vstack([A, vec])
            b = np.append(b, 0)

            (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
            p1[i - 1][j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
            A = np.vstack([A, vec])
            b = np.append(b, 1)

            (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
            p2[i-1][j-1] = -1
            vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
            A = np.vstack([A, vec])
            b = np.append(b, 0)

            (vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
            p2[i - 1][j - 1] = 1
            vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
            A = np.vstack([A, vec])
            b = np.append(b, 1)

# constraint for R:  0 <= R <= N
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
R = -1
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, 0)

(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
R = 1
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, N)

# constraint for M:  0 <= M <= N
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
M = -1
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, 0)

(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
M = 1
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, N)


# add constraint on page 3:
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
for i in range(1, K):
    for j in range(1, K-i+1):
        p0[i-1][j-1] = i
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, 1)

(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
for i in range(1, K):
    for j in range(1, K-i+1):
        p1[i-1][j-1] = i
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, 1)

(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
for i in range(1, K):
    for j in range(1, K-i+1):
        p2[i-1][j-1] = i
vec = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)
A = np.vstack([A, vec])
b = np.append(b, 1)



## delete first row of A, b, A_eq, b_eq
A = np.delete(A, 0, 0)
# print(A.shape)
b = np.delete(b, 0, 0)
# print(b.shape)
A_eq = np.delete(A_eq, 0, 0)
# print(A_eq.shape)
b_eq = np.delete(b_eq, 0, 0)
# print(b_eq.shape)

# set linear programming
(vec, p0, p1, p2, p3, p4, delta, y, R, M) = zero_out(vec, p0, p1, p2, p3, p4, delta, y, R, M)
R = 1
M = alpha
c = create_vec(p0, p1, p2, p3, p4, delta, y, R, M)


res = linprog(c, A, b, A_eq, b_eq, bounds=None, options={"disp": True})
print(res)