from accel_asc import accel_asc
def generate_demands(N, K):
    """
    :param N: Number of files
    :param K: Number of users
    :return: Demand vector, e.g. (N,K)=(3,5), [1,2,2] means (A,B,B,C,C)
    """
    # Generate demand types where all files are requested
    demands = list()
    for x in accel_asc(K):
        # print(x)
        if len(x) == N:
            demands.append(x)
    return demands
