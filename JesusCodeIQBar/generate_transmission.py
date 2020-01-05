from generate_subsets import generate_subsets
from find_subsetPos import find_subsetPos
from scipy import special as sp
import numpy as np
from find_f_for_user_k import find_f_for_user_k

def generate_transmission(N, K, r, d, k, set_R, assignment):
    """
    :param K: Number of users
    :param k: Current user
    :param r: |R|
    :return: Transmission coefficients

    Find the R+ set and each transmission:
        Input: K, k, assignment
        Output: transmission coefficients
    """
    # Find all R+ sets
    T = set(range(K))
    set_R_plus_1 = generate_subsets(T.difference({k}), r+1)

    # number of cached Type I and Type II symbols, for Type II symbols, remove one file, remove one index
    num_trans = int(sp.binom(K-1, r+1) * 2) # x2 because there are two copies
    num_col = int(N * sp.binom(K-1, r) * 2) # x2 because there are two copies

    # Initialize cache for this user
    transmissions = np.zeros((num_trans, num_col), dtype=bool)
    current_row = 0

    # print("set_R_plus_1 is: ", set_R_plus_1)
    for R_plus_1 in set_R_plus_1:
        # print("R_plus_1 is ",R_plus_1)
        for R in generate_subsets(R_plus_1, r):
            # print("R is ",R)
            u = list(set(R_plus_1).difference(set(R)))[0]
            f = find_f_for_user_k(K, u, d)
            # print("set_R is", set_R)
            # print(R)
            index = int(f * sp.binom(K-1, r)) + find_subsetPos(R, set_R)

            # Find the transmission for copy I:
            if (assignment[u] == 'I'):
                # print(current_row)
                # type(current_row)
                # print(index)
                # type(index)
                transmissions[current_row, index] = 1 # for copy I

                transmissions[current_row + 1, index] = 1
                transmissions[current_row + 1, index + N * int(sp.binom(K-1, r))] = 1
            if (assignment[u] == 'Q'):
                transmissions[current_row, index + N * int(sp.binom(K-1, r))] = 1

                transmissions[current_row + 1, index] = 1  # for copy I
            if (assignment[u] == '-'):
                transmissions[current_row, index] = 1
                transmissions[current_row, index + N * int(sp.binom(K-1, r))] = 1

                transmissions[current_row + 1, index + N * int(sp.binom(K - 1, r))] = 1
        current_row += 2

    return transmissions