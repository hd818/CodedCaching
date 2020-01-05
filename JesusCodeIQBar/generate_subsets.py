import itertools
def generate_subsets(S, m):
    """
    :param S: Set of numbers
    :param m: Size of subset
    :return: A list of all subsets of S that of size m, each is a tuple
    """
    a = list()
    for i in itertools.combinations(S, m):
        # print(i)
        a.append(list(i))
    return a
    # return list(itertools.combinations(S, m))
