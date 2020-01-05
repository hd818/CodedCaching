#####################################
# Based on ShuoSHAO's report: find the coefficient coefftor for the linear program
# Perform index finding, that is, e.g. p_{3,i,j}, we'll assign the associated place in the coefficient coefftor to 1
# Input:
#   coeff, K: number of users
#   variable: "p0", "p1", "p2", "p3", "p4", "y", "R", "M"
#   l_1, u_1: \sum_{l_1}^{u_1} ... only for p0, p1, p2, p3, p4, for the others, use l_1 = 0, u_1 = 1
#   sign: +/-1
#   i: only specify it if variable is p0, p1 or p2. (i is the index of the column, j is the index of the row), and we count the items in the matrix vertically, like in MATLAB.
import numpy as np
def assign(coeff, K, variable, i, j=None):
    # Total number of variables
    # coeff = np.zeros(3*K*(K-1)/2 + 2*K + 2)
    # mat = np.zeros(K-1, K-1)

    if variable == "p0":
        base = (i-1)*(2*K-i)//2
        coeff[base + (j - 1)] = 1
        return coeff
    elif variable == "p1":
        base = K*(K - 1)//2 + (i-1)*(2*K-i)//2
        coeff[base + (j - 1)] = 1
        return coeff
    elif variable == "p2":
        base = 2*K*(K - 1) // 2 + (i-1)*(2*K-i)//2
        coeff[base + (j - 1)] = 1
        return coeff
    elif variable == "p3":
        base = 3 * K*(K - 1) // 2
        coeff[base + (i - 1)] = 1
        return coeff
    elif variable == "p4":
        base = 3 * K*(K - 1) // 2 + (K - 1)
        coeff[base + (i - 1)] = 1
        return coeff
    elif variable == "y":
        base = 3 * K*(K - 1) // 2 + 2*(K - 1)
        coeff[base] = 1
        return coeff
    elif variable == "delta":
        base = 3 * K*(K - 1) // 2 + 2*(K - 1) + 1
        coeff[base] = 1
        return coeff
    elif variable == "R":
        base = 3 * K*(K - 1) // 2 + 2*(K - 1) + 2
        coeff[base] = 1
        return coeff
    elif variable == "M":
        base = 3 * K*(K - 1) // 2 + 2*(K - 1) + 3
        coeff[base] = 1
        return coeff