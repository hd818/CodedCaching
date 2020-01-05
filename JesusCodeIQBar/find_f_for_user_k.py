def find_f_for_user_k(K, k, d):
    """
    :param K: The number of users
    :param k: Current user
    :param d: Demand
    :return: The file requested by user k
    """
    real_d = [None] * K
    n = 0
    for m in range(len(d)):
        real_d[n: n + d[m]] = [m] * d[m]
        n += d[m]
    return real_d[k]
