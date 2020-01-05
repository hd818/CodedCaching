import numpy as np
from scipy import special as sp
from scipy.linalg import block_diag
from generate_subsets import generate_subsets
def generate_cache(N, K, r, k):
    """
    Generate the coefficient matrix for each user. At user 1, the base symbols are in the following order:
        A_{2;1}
        A_{3;1}
        A_{4;1}
        B_{2;1}
        B_{3;1}
        B_{4;1}
        C_{2;1} ...
    We only generate the I copies, and for Q copies, we simply concatenate the coefficient matrix

    :param N: Number of files
    :param K: Number of users
    :param r: |R|
    :param k: The current user
    :return: Coefficient matrix of the cache at user k
                and the set R (Particularly, it is a list, since its element order matters)

    """
    # number of cached Type I and Type II symbols, for Type II symbols, remove one file, remove one index 
    num_row = int(sp.binom(K-1, r) + (N-1) * sp.binom(K-2, r-1))
    num_col = int(N * sp.binom(K-1, r))
    # Initialize cache for this user
    cache = np.zeros((num_row, num_col), dtype=bool)

    # 2. Initialize cache matrix for Type I cached symbols
    for R in range(int(sp.binom(K-1,r))):
        for f in range(N):
            cache[R, f*int(sp.binom(K-1,r)) + R] = 1
    # print(cache)


    # 3. Initialize cache matrix for Type II cache symbols
    # Generate all choices of R
    T = set(range(K))
    T = T.difference([k])

    set_R = generate_subsets(T, r)
    """
        The set_R is very import, because it determines the order of the subscript. Since a set is an unordered data structure, 
        we need to convert the set R to a list to preserve the order of the elements inside it. 
    """

    # Find all (r-1) sets, don't forget to remove one index (let's use the last index)
    set_R_minus_1 = generate_subsets(T.difference([list(T)[-1]]),r-1)
    current_row = int(sp.binom(K-1,r));

    for f in range(0, N-1): # remove the last file
        for R_minus_1 in set_R_minus_1:
            # print("hello, I'm set R_mnisu_1")
            # print(R_minus_1)
            pos_in_R = 0
            for R in set_R:
                # print("Hello, I'm set R")
                if set(R_minus_1).issubset(set(R)):
                    cache[current_row, f*int(sp.binom(K-1,r)) + pos_in_R] = 1
                pos_in_R += 1
            current_row += 1
    # print(cache)

    # Do the same thing for copy Q
    cache = block_diag(cache, cache)
    # print(cache)
    # print(cache.shape)
    return cache, set_R
