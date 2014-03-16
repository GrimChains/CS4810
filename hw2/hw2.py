import Image
import sys
import math

# File reading
fread = open(sys.argv[1], 'r')

# Important variables
vertexList = []							# [x, y, z, ?, r, g, b, a]
color = [1, 1, 1]						# [r, g, b] Defaults to white
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

def 

def trif( l1, l2, l3 ) :
	if l1 < 0 :
		vertex1 = vertexList[len(vertexList) + l1]
	else :
		vertex1 = vertexList[l1 - 1]
	if l2 < 0 :
		vertex2 = vertexList[len(vertexList) + l2]
	else :
		vertex2 = vertexList[l1 - 1]
	if l2 < 0 :
		vertex3 = vertexList[len(vertexList) + l36]
	else :
		vertex3 = vertexList[l1 - 1]
	
def render() :
	print "Hai"



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
	elif parse[0] == "color" :
		color[0] = float(parse[1])
		color[1] = float(parse[2])
		color[2] = float(parse[3])
	elif parse[0] == "trif" :
		trif( int(parse[1]), int(parse[2]), int(parse[3]) )
render()
