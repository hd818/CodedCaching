def find_leaders(d):
    """
    :param d: Demand
    :return: Leaders of all users
    """
    leaders = [0];
    i = 0
    for l in range(len(d)-1):
        i += d[l]
        leaders.append(i)
    # print("The leaders are:")
    return leaders
