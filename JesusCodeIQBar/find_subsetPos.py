def find_subsetPos(R, R_plus_1_set):
    """
    From the list of all subsets of a set, find the position of a particular subset
    :param R (list): The subset being looking for
    :param R_plus_1_set (list): A list of all subsets of a set
    :return: Position of the subset in the list
    """
    for i in range(len(R_plus_1_set)):
        if (R == R_plus_1_set[i]):
            return i

