"""
Input: a .txt file containing the:
1st line: random raviables
    Can be the following symbols: alphanumeric (a-z, A-Z, 0-9) or one of these symbols: ! " # $ % & / . ; ? @ _ ` ' { } ~.
2nd line to end: constraints

Output:
    CPLEX LP file format file
"""


def split(line):
    """
    :param line: "H(X1, X2|X3) - I(X1; W1 | X2) >= 0"
    :return: coef: [1, -1]
             entity: ['H(X1, X2|X3)', I(X1; W1 | W2)]
             sign: 'geq'
             constant: 0
    """
    i = 0
    coef = []
    entity = []
    if (line[0] == 'H' or line[0] == 'I'):
        line = '1' + line
    sign_set = ['<', '>']

    # seperate the inequality to single entities
    while (line[i] not in sign_set):
        j = i+1
        while (line[j] != 'H' and line[j] != 'I'):
            j += 1

        # find one (coefficient * entity) pair
        coef_tmp = float(line[i:j].strip().replace(" ", '')) if line[i:j].strip() != '-' and line[i:j].strip() != '+' else float(line[i:j].strip() + '1')
        i = j
        while (line[j] != ')'):
            j += 1
        entity_tmp = line[i:j+1].strip()

        # change it to canonical form:
        toCanonical(coef_tmp, entity_tmp, coef, entity)

        i = j + 1
        while (line[i] == ' '): i += 1

    # reaches to the end
    if line[i+1] == '=':
        sign = line[i: i+2]
        i = i + 2
    else:
        sign = line[i: i+1]
        i = i + 1

    constant = line[i:].strip()
    return coef, entity, sign, constant


def splitObj(line):
    """
    :param line: "H(X1, X2|X3) - I(X1; W1 | X2) >= 0"
    :return: coef: [1, -1]
             entity: ['H(X1, X2|X3)', I(X1; W1 | W2)]
             sign: 'geq'
             constant: 0
    """
    line += '<0'
    return split(line)


def toCanonical(coef, entity, coef_vec, entity_vec):
    """
    :param line: an information quantity, say: -2, I(X1; X2)
                since its canonical form is: I(X1; X2) = H(X1) + H(X2) - H(X1, X2)
    :return: coef_vec: [-2, -2, 2]
             entity_vec: ['H(X1), H(X2), H(X1, X2)']
    """
    if entity[0] == 'H':
        is_conditional = entity.find('|')
        if is_conditional == -1:
            coef_vec.append(coef)
            entity_vec.append(entity)

        else:
            coef_vec += [coef, -coef]
            entity_vec.append(entity.replace('|', ','))
            entity_vec.append("H(" + entity[is_conditional + 1:])

    elif entity[0] == 'I':
        is_conditional = entity.find('|')
        if is_conditional == -1:
            coef_vec += [coef, coef, -coef]
            pos_semi_colon = entity.find(';')
            entity_vec.append('H' + entity[1 : pos_semi_colon] + ')')
            entity_vec.append('H('+ entity[pos_semi_colon + 1 :])
            entity_vec.append('H' + entity[1:].replace(';', ','))

        else:
            coef_vec += [coef, coef, -coef, -coef]
            pos_semi_colon = entity.find(';')
            entity_vec.append('H' + entity[1 : pos_semi_colon] + ',' + entity[is_conditional + 1: ])
            entity_vec.append('H('+ entity[pos_semi_colon + 1 :is_conditional].strip() + ',' + entity[is_conditional + 1: ])
            entity_vec.append('H('+ entity[is_conditional + 1:])
            entity_vec.append('H' + entity[1:].replace(';', ',').replace('|', ','))

from bitstring import BitArray
def jointEtrptoPos(jointEtrp, varList):
    """
    :param jointEtrp: a string like "H(X,Y,Z)"
    :param varList: a list of variables [X, Y, Z]
    :return: 7, since 111->7
    """
    res = [0] * len(varList)
    for i, v in enumerate(varList):
        if v in jointEtrp:
            res[i] = 1
    return BitArray(res).uint

import fileinput

filename = "input.txt"
fileoutput = open('output.txt', 'w')

# for each information inequality, compute the vector of coefficients A, b (or A_eq, b_eq)
for line in fileinput.input(filename):
    if line == '\n':
        continue

    line = line.strip()

    if line.startswith("Variables"):
        lineState = 'V'
        continue
    elif line.startswith("Maximize"):
        lineState = 'O'
        continue
    elif line.startswith("Subject To"):
        lineState = 'S'
        continue


    if lineState == 'V':
        varList = [item.strip() for item in line.rstrip('\n').split(',')]
        print("Variables: ", varList)
        num_of_var = len(varList)
        print("Number of variables: ", num_of_var)
        print("Number of LP variables: ", 2 ** num_of_var - 1)  # 2^n-1 LP variables

    elif lineState == 'O':
        print("Objective function is :", line)
        coef, entity, _, _ = splitObj(line)
        c = [0] * (2 ** num_of_var - 1) # 2^n-1 LP variables
        for i in range(len(coef)):
            lp_var = entity[i]
            pos = jointEtrptoPos(lp_var, varList)
            c[pos - 1] += coef[i]
        print("Coefficient vector: ", c)

        fileoutput.write("Maximize\n")
        fileoutput.write(" obj: ")
        isFirst = True
        for i in range(2 ** num_of_var - 1):
            if c[i] > 0 and isFirst:
                fileoutput.write(str(c[i]) + " x" + str(i))
                isFirst = False
            elif c[i] > 0 and not isFirst:
                fileoutput.write(" + " + str(c[i]) + " x" + str(i))
                isFirst = False
            elif c[i] < 0:
                fileoutput.write(" - " + str(abs(c[i])) + " x" + str(i))
                isFirst = False
        fileoutput.write('\n')
        fileoutput.write("Subject To\n")

    elif lineState == 'S':
        print("Information inequality: ", line)
        coef, entity, sign, constant = split(line)
        if sign == '=':
            A_eq = [0] * (2 ** num_of_var - 1) # 2^n-1 LP variables
            for i in range(len(coef)):
                lp_var = entity[i]
                pos = jointEtrptoPos(lp_var, varList)
                A[pos-1] += coef[i]
            b_eq = constant
            isFirst = True
            for i in range(2 ** num_of_var - 1):
                if A_eq[i] > 0 and isFirst:
                    fileoutput.write(str(A_eq[i]) + " x" + str(i))
                    isFirst = False
                elif A_eq[i] > 0 and not isFirst:
                    fileoutput.write(" + " + str(A_eq[i]) + " x" + str(i))
                    isFirst = False
                elif A_eq[i] < 0:
                    fileoutput.write(" - " + str(abs(A_eq[i])) + " x" + str(i))
                    isFirst = False
            fileoutput.write(" " + sign + b_eq + "\n")
        else:
            A = [0] * (2 ** num_of_var - 1) # 2^n-1 LP variables
            for i in range(len(coef)):
                lp_var = entity[i]
                pos = jointEtrptoPos(lp_var, varList)
                A[pos-1] += coef[i]
            b = constant
            isFirst = True
            for i in range(2 ** num_of_var - 1):
                if A[i] > 0 and isFirst:
                    fileoutput.write(str(A[i]) + " x" + str(i))
                    isFirst = False
                elif A[i] > 0 and not isFirst:
                    fileoutput.write(" + " + str(A[i]) + " x" + str(i))
                    isFirst = False
                elif A[i] < 0:
                    fileoutput.write(" - " + str(abs(A[i])) + " x" + str(i))
                    isFirst = False
            fileoutput.write(" " + sign + b + "\n")
        print("Coefficient vector: ", A, sign, b)

fileoutput.write("End")
fileoutput.close()







