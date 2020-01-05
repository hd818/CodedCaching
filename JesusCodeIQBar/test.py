#!/usr/bin/python

import numpy as np
from GF import GF

gf = GF(2)

print('####################################')


print('start addition test:')
print('\taddition:\t\t' + str(gf.add(0,0) == 0 and gf.add(1,1) == 0 and gf.add(1,0) == 1 and gf.add(0,1) == 1))
print('\tvector addition:\t' + str(gf.add([1,1,0], [1,1,0])==[0,0,0]))


print('####################################')


print('start rank test:')
arr = [
	[1, 1, 0, 0],
	[1, 0, 1, 0],
	[1, 0, 0, 1],
	[0, 1, 1, 0],
	[0, 1, 0, 1],
	[0, 0, 1, 1]
]
print('\t' + str(gf.matrix_rank(np.matrix(arr)) == 3))

arr2 = [
	[1, 1, 0, 0, 0],
	[0, 1, 1, 0, 0],
	[0, 0, 1, 1, 0],
	[0, 0, 0, 0, 1]
]
print('\t' + str(gf.matrix_rank(np.matrix(arr2)) == 4))

arr3 = [
	[1, 0, 0],
	[0, 1, 0],
	[0, 0, 0],
	[0, 0, 0]
]
print('\t' + str(gf.matrix_rank(np.matrix(arr3)) == 2))

arr4 = [
	[1, 0, 0],
	[0, 0, 0],
	[0, 0, 1],
	[0, 0, 0]
]
print('\t' + str(gf.matrix_rank(np.matrix(arr4)) == 2))

arr5 = [
	[1, 0, 0],
	[0, 0, 0],
	[0, 1, 0],
	[0, 0, 0]
]
print('\t' + str(gf.matrix_rank(np.matrix(arr5)) == 2))

arr6 = [
	[1, 0, 0],
	[0, 0, 1],
	[0, 1, 0],
	[0, 0, 0]
]
print('\t' + str(gf.matrix_rank(np.matrix(arr6)) == 3))

arr7 = [
	[False, True],
	[True, False]
]
print("This is matrix 7:")
print('\t' + str(gf.matrix_rank(np.matrix(arr7)) == 12)