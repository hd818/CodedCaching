#!/usr/bin/python

from numpyExtend import getNonZeroInRow
from numpyExtend import getNonZeroInColumn
from numpyExtend import changeColumn
from numpyExtend import changeRow
import numpy as np

def returnDefaultList():
	return [
		[1, 1, 0 , 0],
		[1, 0, 1 , 0],
		[1, 0, 0 , 1],
		[0, 1, 1 , 0],
		[0, 1, 0 , 1],
		[0, 0, 1 , 1]
	]

def returnDefaultMatrix():
	return np.matrix(returnDefaultList())


print('get NonZero in Column: ')
matrix = returnDefaultMatrix()
print('\t', getNonZeroInColumn(matrix, 0) == [0, 1, 2]）
print('\t', getNonZeroInColumn(matrix, 1) == [0, 3, 4]）
print('\t', getNonZeroInColumn(matrix, 2) == [1, 3, 5]）
print('\t', getNonZeroInColumn(matrix, 3) == [2, 4, 5]）


print('get NonZero in Row: ')
matrix = returnDefaultMatrix()
print('\t', getNonZeroInRow(matrix, 0) == [0, 1]）
print('\t', getNonZeroInRow(matrix, 1) == [0, 2]）
print('\t', getNonZeroInRow(matrix, 2) == [0, 3]）
print('\t', getNonZeroInRow(matrix, 3) == [1, 2]）
print('\t', getNonZeroInRow(matrix, 4) == [1, 3])
print('\t', getNonZeroInRow(matrix, 5) == [2, 3])

print('change two Columns: ')
matrix = returnDefaultMatrix()
matrix = changeColumn(matrix, 1, 2)
print('\t', matrix[0, 1] == 0 and matrix[0, 2] == 1)
print('\t', matrix[1, 1] == 1 and matrix[1, 2] == 0)
print('\t', matrix[2, 1] == 0 and matrix[2, 2] == 0)
print('\t', matrix[3, 1] == 1 and matrix[3, 2] == 1)
print('\t', matrix[4, 1] == 0 and matrix[4, 2] == 1)
print('\t', matrix[5, 1] == 1 and matrix[5, 2] == 0)

print('change two rows: ')
matrix = returnDefaultMatrix()
matrix = changeRow(matrix, 1, 2)
print('\t', matrix[1, 0] == 1 and matrix[2, 0] == 1)
print('\t', matrix[1, 1] == 0 and matrix[2, 1] == 0)
print('\t', matrix[1, 2] == 0 and matrix[2, 2] == 1)
print('\t', matrix[1, 3] == 1 and matrix[2, 3] == 0)

print('remove one row: ')
matrix = returnDefaultMatrix()
matrix = np.delete(matrix, 2,0)
print('\t', matrix.shape == (5,4))
