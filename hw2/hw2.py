import Image
import sys
import math

# File reading
fread = open(sys.argv[1], 'r')

# Important variables
vertexList = []							# [x, y, z, ?, r, g, b, a]
color = [1, 1, 1]						# Defaults to white
eye = [0.0, 0.0, 0.0]					# Defaults to the origin
bounds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]	# [lx, rx, dy, uy, bz, fz]

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


line = fread.readline()
info = line.split()
fileType = info[0]
fileName = info[3]
img = Image.new("RGBA", (int(info[1]), int(info[2])), (0,0,0,0))
putpixel = img.im.putpixel

while (line != "") :
	parse = line.split()
	if parse == [] :
		continue
	elif parse[0] == "xyz" :
		vertexList.append([float(parse[1]), float(parse[2]), float(parse[3]), 1, 255, 255, 255, 255])
