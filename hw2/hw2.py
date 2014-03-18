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
primitives = []
buff = []



def matrixmult(a, b) :
	if len(a[0]) != len(b) :
		raise ArithmeticError('Matrix dimensions do not match')
	result = []
	for x in range(0, len(a[0])) :
		result.append([])
		for y in range(0, len(b)) :
			result[x].append(0)
			for z in range(0, len(b[0])) :
				result[x][y] += a[z][y] * b[x][z]
	return result

def trif( l1, l2, l3 ) :
	if l1 < 0 :
		vertex1 = vertexList[len(vertexList) + l1]
	else :
		vertex1 = vertexList[l1 - 1]
	if l2 < 0 :
		vertex2 = vertexList[len(vertexList) + l2]
	else :
		vertex2 = vertexList[l1 - 1]
	if l3 < 0 :
		vertex3 = vertexList[len(vertexList) + l3]
	else :
		vertex3 = vertexList[l1 - 1]
	addPrimitive(vertex1, vertex2, vertex3)
	
def addPrimitive(vertex1, vertex2, vertex3) :
	primitives.append([vertex1, vertex2, vertex3])

def render() :
	for x in range(0, int(info[1])-1) :
		buff.append([])
		for y in range(0, int(info[2])-1) :
			buff[x].append(1)
	dz = 0.001
	fovx = (math.pi)/4
	fovy = (float(info[1])/float(info[2])) * fovx
	width = float(info[1])
	height = float(info[2])
	for x in range(0, int(info[1])) :
		dx = (abs(x - (width/2))/(width/2) * fovx) * dz
		for y in range(0, int(info[2]])) :
			dy = (abs(y - (height/2))/(height/2) * fovy)*dz





	#fovx = 3.14596/4
	#fovy = (float(info[1])/float(info[2])) * fovx
	#width = float(info[1])
	#height = float(info[2])
	#dz = 0.001 # Magic number, yayyyy
	#for x in range(0, int(info[1])) :
	#	dx = (abs(x - (width/2))/(width/2) * fovx) * dz
	#	for y in range(0, int(info[2]])) :
	#		dy = (abs(y - (height/2))/(height/2) * fovy)*dz
	#		z = 1.0







line = fread.readline()
info = line.split()
fileType = info[0]
fileName = info[3]
img = Image.new("RGBA", (int(info[1]), int(info[2])), (0,0,0,0))
putpixel = img.im.putpixel

while (line != "") :
	parse = line.split()
	if parse == [] :
		parse
	elif parse[0] == "xyz" :
		vertexList.append([float(parse[1]), float(parse[2]), float(parse[3]), 1, 255, 255, 255, 255])
	elif parse[0] == "color" :
		color[0] = float(parse[1])
		color[1] = float(parse[2])
		color[2] = float(parse[3])
	elif parse[0] == "trif" :
		trif( int(parse[1]), int(parse[2]), int(parse[3]) )
	line = fread.readline()
render()
