import Image
import sys
import math

def matrixmult(a, b) :
	print len(a[0])
	print len(a)
	print len(b[0])
	print len(b)
	if len(a[0]) != len(b) :
		raise ArithmeticError('Matrix dimensions do not match')
	result = []
	for x in range(0, len(a)) :
		for y in range(0, len(b[0])) :
			for z in range(0, len(b)) :

	for x in range(0, len(a)-1) :
		print "x"
		print x
		result.append([])
		result[x].append(0)
		for y in range(0, len(b[0])-1) :
			print "y"
			print y
			print "z"
			for z in range(0, len(b)) :
				print z
				tmp = a[x][y]
				tmp2 = b[y][x]
				result[x][y] += (a[z][y] * b[x][z])
	return result


# File reading
fread = open(sys.argv[1], 'r')

a = []
a.append([])
a.append([])
a.append([])
a[0].append(1)
a[0].append(2)
a[1].append(3)
a[1].append(4)
a[2].append(1)
a[2].append(2)

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