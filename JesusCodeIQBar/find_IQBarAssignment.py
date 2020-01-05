from find_leaders import find_leaders
def find_IQBarAssignment(K, d, i):
    """
    Find I/Q/Bar Assignment for leader l,
    :param K: The number of users
    :param d: Demand
    :param leaders: Leaders of all users
    :param i: File i
    :return: The I/Q/Bar assignment for the leader requesting file i
    """
    """ 

        Input: d, l, leaders
        Output: assignment: a list of length K, with each element being I/Q/Bar, NaN for current user
    """
    leaders = find_leaders(d)

    assignment = [None] * K
    # For the current user, the assignment should be NaN
    assignment[leaders[i]] = 'NaN'
    # print("This is the original assignment:")
    # print(assignment)
    # for f in range(len(d)):
    """ For all other users requests the same file, based on the number of users, the user assignment should be:
    0: don't worry about it
    1: I
    2: - -
    3: - - I 
    4: - - - - 
    5: - - - - I
    6: - - - - - -
    ...
    """
    if(d[i] - 1 != 0):
        assignment[leaders[i]+1:leaders[i]+d[i]] = ['-'] * (d[i]-1)
        if (d[i] -1) % 2 == 1:
            assignment[leaders[i]+d[i]-1] = 'I'
    # print("This is the assignment after of the current file")
    # print(assignment)
    """ For the other users, based on the number of users, the user assignment should be:
    1: -
    2: I, Q
    3: - - - 
    4: - - I Q
    5: - - - - -
    6: - - - - I Q
    ...
    """
    for j in [x for x in range(len(leaders)) if x != i]:
        # print(j)
        # print("From %i to %i", leaders[j], leaders[j]+d[j])
        assignment[leaders[j]:leaders[j]+d[j]] = ['-'] * d[j]
        if(d[j] % 2 == 0):
            assignment[leaders[j]+d[j]-2] = 'I'
            assignment[leaders[j]+d[j]-1] = 'Q'
    return assignment
