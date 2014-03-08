import Image
import sys
import math

def matrixmult(a, b) :
	if len(a[0]) != len(b) :
		raise ArithmeticError('Matrix dimensions do not match')
	result = []
	for x in range(0, len(a[0])) :
		result.append([])
		for y in range(0, len(b)) :
			result[x].append(0)
			print result
			print "++++++++++++"
			for z in range(0, len(b[0])) :
				result[x][y] += a[z][y] * b[x][z]
			print result
			print "============"
	return result


# File reading
# fread = open(sys.argv[1], 'r')

a = []
a.append([])
a.append([])
a.append([])
a[0].append(1)
a[0].append(2)
a[1].append(3)
a[1].append(4)
a[2].append(5)
a[2].append(6)

b = []
b.append([])
b.append([])
b[0].append(9)
b[0].append(8)
b[0].append(7)
b[1].append(6)
b[1].append(5)
b[1].append(4)

print a
print b
tmp = matrixmult(a, b)

print a
print b
print tmp