from math import sqrt, pow, pi, cos, sin
import Image
import sys
import copy
 
class Vector( object ):
	   
		def __init__(self,x,y,z):
				self.x = x
				self.y = y
				self.z = z
	   
		def dot(self, b):
				return self.x*b.x + self.y*b.y + self.z*b.z
			   
		def cross(self, b):
				return (self.y*b.z-self.z*b.y, self.z*b.x-self.x*b.z, self.x*b.y-self.y*b.x)
		   
		def magnitude(self):
				return sqrt(self.x**2+self.y**2+self.z**2)
			   
		def normal(self):
				mag = self.magnitude()
				return Vector(self.x/mag,self.y/mag,self.z/mag)
			   
		def __add__(self, b):
				return Vector(self.x + b.x, self.y+b.y, self.z+b.z)
	   
		def __sub__(self, b):
				return Vector(self.x-b.x, self.y-b.y, self.z-b.z)
			   
		def __mul__(self, b):
				assert type(b) == float or type(b) == int
				return Vector(self.x*b, self.y*b, self.z*b)            

def triangleNormal(x1, x2, x3, y1, y2, y3, z1, z2, z3) :
		U = Vector(x2-x1, y2-y1, z2-z1)
		V = Vector(x3-x1, y3-y1, z3-z1)

		norm = Vector((U.y * V.z) - (U.z * V.y), (U.z * V.x) - (U.x * V.z), (U.x * V.y) - (U.y * V.x))
		return norm

class Triangle( object ):

		def __init__(self, point1, point2, point3, color) :
				self.n = triangleNormal( point1.x, point2.x, point3.x, point1.y, point2.y, point3.y, point1.z, point2.z, point3.z )
				self.p = point1
				self.col = color
				self.p1 = point1
				self.p2 = point2
				self.p3 = point3

		def intersection(self, l):
				d = l.d.dot(self.n)
				if d == 0:
						return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
				else:
						# We intersect plane. Check to see if we're contained within the triangle
						d = (self.p - l.o).dot(self.n) / d
						# a = 1, b = 2, c = 3
						temp = Intersection(l.o+l.d*d, d, self.n, self)
						q = Vector(temp.p.x, temp.p.y, temp.p.z)
						ba = Vector(self.p2.x - self.p1.x, self.p2.y - self.p1.y, self.p2.z - self.p1.z)
						qa = Vector(q.x - self.p1.x, q.y - self.p1.y, q.z - self.p1.z)
						t1 = ba.cross(qa)
						t1 = Vector(t1[0], t1[1], t1[2]).dot(self.n)
						cb = Vector(self.p3.x - self.p2.x, self.p3.y - self.p2.y, self.p3.z - self.p2.z)
						qb = Vector(q.x - self.p2.x, q.y - self.p2.y, q.z - self.p2.z)
						t2 = cb.cross(qb)
						t2 = Vector(t2[0], t2[1], t2[2]).dot(self.n)
						ac = Vector(self.p1.x - self.p3.x, self.p1.y - self.p3.y, self.p1.z - self.p3.z)
						qc = Vector(q.x - self.p3.x, q.y - self.p3.y, q.z - self.p3.z)
						t3 = ac.cross(qc)
						t3 = Vector(t3[0], t3[1], t3[2]).dot(self.n)
						if t1 >= 0 and t2 >= 0 and t3 >= 0 and temp.p.z <= 0 and temp.p.z >= -1: # Point q is within our triangle
							return temp
						else:
							return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
			   
class Plane( object ):
	   
		def __init__(self, point, normal, color):
				self.n = normal
				self.p = point
				self.col = color
			   
		def intersection(self, l):
				d = l.d.dot(self.n)
				if d == 0:
						return Intersection( vector(0,0,0), -1, vector(0,0,0), self)
				else:
						d = (self.p - l.o).dot(self.n) / d
						return Intersection(l.o+l.d*d, d, self.n, self)
			   
class Ray( object ):
	   
		def __init__(self, origin, direction):
				self.o = origin
				self.d = direction
			   
class Intersection( object ):
	   
		def __init__(self, point, distance, normal, obj):
				self.p = point
				self.d = distance
				self.n = normal
				self.obj = obj
			   
def testRay(ray, objects, ignore=None):
		intersect = Intersection( Vector(0,0,0), -1, Vector(0,0,0), None)
	   
		for obj in objects:
				if obj is not ignore:
						currentIntersect = obj.intersection(ray)
						if currentIntersect.d > 0 and intersect.d < 0:
								intersect = currentIntersect
						elif 0 < currentIntersect.d < intersect.d:
								intersect = currentIntersect
		return intersect
	   
def trace(ray, objects, light, maxRecur):
		if maxRecur < 0:
				return (0,0,0)
		intersect = testRay(ray, objects) 
		if intersect.d == -1:
				#col = Vector(AMBIENT,AMBIENT,AMBIENT)
				col = Vector(-1, -1, -1)
		elif intersect.n.dot(light - intersect.p) < 0:
				col = intersect.obj.col * AMBIENT
		else:
				lightRay = Ray(intersect.p, (light-intersect.p).normal())
				if testRay(lightRay, objects, intersect.obj).d == -1:
						lightIntensity = 1000.0/(4*pi*(light-intersect.p).magnitude()**2)
						col = intersect.obj.col * max(intersect.n.normal().dot((light - intersect.p).normal()*lightIntensity), AMBIENT)
				else:
						col = intersect.obj.col * AMBIENT
		tx = (intersect.p.x - width/2)/(width/2)
		ty = (intersect.p.y - height/2)/(height/2)
		#if intersect.p.x != 0 and intersect.p.y != 0 and intersect.p.z != 0:
		#if intersect.d != -1:
		#	print clipplane
		#	print intersect.p.x
		#	print intersect.p.y
		#	print intersect.p.z
		#print intersect.p.x * clipplane[0] + intersect.p.y * clipplane[1] + intersect.p.z * clipplane[2] + clipplane[3]
		if clip and tx * clipplane[0] + ty * clipplane[1] + intersect.p.z * clipplane[2] + clipplane[3] <= 0:
			col = Vector(-1, -1, -1)
		return col
	   
def gammaCorrection(color,factor):
		return (int(pow(color.x/255.0,factor)*255),
						int(pow(color.y/255.0,factor)*255),
						int(pow(color.z/255.0,factor)*255))

def trif( parse ):
	global vertexList

	applyviewmodel()
	if int(parse[1]) < 0 :
		vertex1 = vertexList[len(vertexList) + int(parse[1])]
	else :
		vertex1 = vertexList[int(parse[1]) - 1]
	if int(parse[2]) < 0 :
		vertex2 = vertexList[len(vertexList) + int(parse[2])]
	else :
		vertex2 = vertexList[int(parse[2]) - 1]
	if int(parse[3]) < 0 :
		vertex3 = vertexList[len(vertexList) + int(parse[3])]
	else :
		vertex3 = vertexList[int(parse[3]) - 1]
	if cull:
		a = Vector(vertex1[0], vertex1[1], vertex1[2])
		b = Vector(vertex2[0], vertex2[1], vertex2[2])
		c = Vector(vertex3[0], vertex3[1], vertex3[2])
		if a.cross(b)[2] > 0:
			objs.append(Triangle(Vector(vertex1[0]/vertex1[3], vertex1[1]/vertex1[3], vertex1[2]/vertex1[3]), Vector(vertex2[0]/vertex2[3], vertex2[1]/vertex2[3], vertex2[2]/vertex2[3]), Vector(vertex3[0]/vertex3[3], vertex3[1]/vertex3[3], vertex3[2]/vertex3[3]), Vector(color[0], color[1], color[2])))
	else:
		objs.append(Triangle(Vector(vertex1[0]/vertex1[3], vertex1[1]/vertex1[3], vertex1[2]/vertex1[3]), Vector(vertex2[0]/vertex2[3], vertex2[1]/vertex2[3], vertex2[2]/vertex2[3]), Vector(vertex3[0]/vertex3[3], vertex3[1]/vertex3[3], vertex3[2]/vertex3[3]), Vector(color[0], color[1], color[2])))

def translate( x, y, z, w ):
	global vertexList
	for v in range(0, len(vertexList)):
		(vertexList[v])[0] = (vertexList[v])[0] + x
		(vertexList[v])[1] = (vertexList[v])[1] + y
		(vertexList[v])[2] = (vertexList[v])[2] + z

def scale( x, y, z, w ):
	global vertexList
	global viewmodel
	x = float(parse[1])
	y = float(parse[2])
	z = float(parse[3])
	# Scaling

	tmp = copy.deepcopy(viewmodel)
	viewmodel[0][0] = tmp[0][0]*x
	viewmodel[1][0] = tmp[1][0]*x
	viewmodel[2][0] = tmp[2][0]*x
	viewmodel[3][0] = tmp[3][0]*x
	viewmodel[0][1] = tmp[0][1]*y
	viewmodel[1][1] = tmp[1][1]*y
	viewmodel[2][1] = tmp[2][1]*y
	viewmodel[3][1] = tmp[3][1]*y
	viewmodel[0][2] = tmp[0][2]*z
	viewmodel[1][2] = tmp[1][2]*z
	viewmodel[2][2] = tmp[2][2]*z
	viewmodel[3][2] = tmp[3][2]*z

def lookat( parse ):
	global vertexList
	vertexList = copy.deepcopy(virgin)
	if int(parse[1]) < 0 :
		eye = vertexList[len(vertexList) + int(parse[1])]
	else :
		eye = vertexList[int(parse[1]) - 1]
	if int(parse[2]) < 0 :
		center = vertexList[len(vertexList) + int(parse[2])]
	else :
		center = vertexList[int(parse[2]) - 1]
	eye = Vector(float(eye[0]), float(eye[1]), float(eye[2]))
	center = Vector(float(center[0]), float(center[1]), float(center[2]))
	up = Vector(float(parse[3]), float(parse[4]), float(parse[5]))
	up = up.normal()

	eye.x = (eye.x - width/2)/(width/2)
	eye.y = (eye.y - height/2)/(height/2)
	eye.z = -eye.z
	center.x = (center.x - width/2)/(width/2)
	center.y = (center.y - height/2)/(height/2)
	center.z = -center.z

	Z = Vector(eye.x - center.x, eye.y - center.y, eye.z - center.z)
	Z = Z.normal()

	X = up.cross(Z)
	X = Vector(X[0], X[1], X[2])
	X = X.normal()

	Y = Z.cross(X)
	Y = Vector(Y[0], Y[1], Y[2])

	for v in vertexList:
		v[0] = (v[0] - width/2)/(width/2)
		v[1] = (v[1] - height/2)/(height/2)
		v[2] = -v[2]

		tmp = copy.deepcopy(v)
		v[0] = X.x*tmp[0] + X.y*tmp[1] + X.z*tmp[2] + tmp[3]*-eye.dot(X)
		v[1] = Y.x*tmp[0] + Y.y*tmp[1] + Y.z*tmp[2] + tmp[3]*-eye.dot(Y)
		v[2] = Z.x*tmp[0] + Z.y*tmp[1] + Z.z*tmp[2] + tmp[3]*-eye.dot(Z)

		v[0] = (v[0] * (width/2)) + (width/2)
		v[1] = (v[1] * (height/2)) + (height/2)
		v[2] = -v[2]

def rotatex( parse ):
	global vertexList
	degree = cos(float(parse[1]) * (pi/180))
	for v in vertexList:
		v[0] = (v[0] - width/2)/(width/2)
		v[1] = (v[1] - height/2)/(height/2)
		v[2] = -v[2]

		tmp = copy.deepcopy(v)
		v[1] = cos(degree)*tmp[1] - sin(degree)*tmp[2]
		v[2] = sin(degree)*tmp[1] + cos(degree)*tmp[2]

		v[0] = (v[0] * (width/2)) + (width/2)
		v[1] = (v[1] * (height/2)) + (height/2)
		v[2] = -v[2]

def rotatey( parse ):
	global vertexList
	degree = cos(float(parse[1]) * (pi/180))
	for v in vertexList:
		v[0] = (v[0] - width/2)/(width/2)
		v[1] = (v[1] - height/2)/(height/2)
		v[2] = -v[2]

		tmp = copy.deepcopy(v)
		v[0] = cos(degree)*tmp[0] + sin(degree)*tmp[2]
		v[2] = -sin(degree)*tmp[0] + cos(degree)*tmp[2]

		v[0] = (v[0] * (width/2)) + (width/2)
		v[1] = (v[1] * (height/2)) + (height/2)
		v[2] = -v[2]

def rotatez( parse ):
	global vertexList
	degree = cos(float(parse[1]) * (pi/180))
	for v in vertexList:
		v[0] = (v[0] - width/2)/(width/2)
		v[1] = (v[1] - height/2)/(height/2)
		v[2] = -v[2]

		tmp = copy.deepcopy(v)
		v[0] = cos(degree)*tmp[0] - sin(degree)*tmp[1]
		v[1] = sin(degree)*tmp[0] + cos(degree)*tmp[1]

		v[0] = (v[0] * (width/2)) + (width/2)
		v[1] = (v[1] * (height/2)) + (height/2)
		v[2] = -v[2]

def loadmv( parse ):

	global vertexList
	vertexList = copy.deepcopy(virgin)

	for v in vertexList:
		v[0] = (v[0] - width/2)/(width/2)
		v[1] = (v[1] - height/2)/(height/2)
		v[2] = -v[2]

		tmp = copy.deepcopy(v)

		v[0] = tmp[0]*float(parse[1]) + tmp[1]*float(parse[2]) + tmp[2]*float(parse[3]) + tmp[3]*float(parse[4])
		v[1] = tmp[0]*float(parse[5]) + tmp[1]*float(parse[6]) + tmp[2]*float(parse[7]) + tmp[3]*float(parse[8])
		v[2] = tmp[0]*float(parse[9]) + tmp[1]*float(parse[10]) + tmp[2]*float(parse[11]) + tmp[3]*float(parse[12])
		v[3] = tmp[0]*float(parse[13]) + tmp[1]*float(parse[14]) + tmp[2]*float(parse[15]) + tmp[3]*float(parse[16])
		
		v[0] = (v[0] * (width/2)) + (width/2)
		v[1] = (v[1] * (height/2)) + (height/2)
		v[2] = -v[2]

def orth( parse ):
	global vertexList
	vertexList = copy.deepcopy(virgin)
	left = float(parse[1])
	right = float(parse[2])
	bottom = float(parse[3])
	top = float(parse[4])
	farVal = float(parse[6])
	nearVal = (2*float(parse[5])) - farVal
	#near = 2*float(parse[5]) - far # might have to change this to 2n - f

	tx = -(right + left)/(right - left)
	ty = -(top + bottom)/(top - bottom)
	tz = -(farVal + nearVal)/(farVal - nearVal)

	for v in vertexList:
		v[0] = (v[0] - width/2)/(width/2)
		v[1] = (v[1] - height/2)/(height/2)
		v[2] = -v[2]

		tmp = copy.deepcopy(v)

		#v[0] = tmp[0] * (2/(right-left)) + (right + left)/(right - left) + tmp[3]*tx
		#v[1] = tmp[1] * (2/(top-bottom)) + (top + bottom)/(top - bottom) + tmp[3]*ty
		#v[2] = tmp[2] * (-2/(farVal-nearVal)) + (farVal + nearVal)/(farVal - nearVal) + tmp[3]*tz
		
		v[0] = tmp[0] * (2/(right-left)) + tmp[3]*tx
		v[1] = tmp[1] * (2/(top-bottom)) + tmp[3]*ty
		v[2] = tmp[2] * (-2/(farVal-nearVal)) + tmp[3]*tz


		v[0] = (v[0]*width/2) + (width/2)
		v[1] = (v[1]*height/2) + (height/2)
		v[2] = -v[2]

def scalec( parse ):

	global vertexList
	global viewmodel
	if int(parse[4]) < 0 :
		opoint = copy.deepcopy(vertexList[len(vertexList) + int(parse[4])])
	else :
		opoint = copy.deepcopy(vertexList[int(parse[4]) - 1])
	x = float(parse[1])
	y = float(parse[2])
	z = float(parse[3])
	# Scaling

	tmp = copy.deepcopy(viewmodel)
	viewmodel[0][0] = tmp[0][0]*x
	viewmodel[1][0] = tmp[1][0]*x
	viewmodel[2][0] = tmp[2][0]*x
	viewmodel[3][0] = tmp[3][0]*x
	viewmodel[0][1] = tmp[0][1]*y
	viewmodel[1][1] = tmp[1][1]*y
	viewmodel[2][1] = tmp[2][1]*y
	viewmodel[3][1] = tmp[3][1]*y
	viewmodel[0][2] = tmp[0][2]*z
	viewmodel[1][2] = tmp[1][2]*z
	viewmodel[2][2] = tmp[2][2]*z
	viewmodel[3][2] = tmp[3][2]*z

	for v in vertexList:
		# Translate back into relative form
		v[0] = (v[0] - width/2)/(width/2)
		v[1] = (v[1] - height/2)/(height/2)

		# Scale
		v[0] = v[0] * x
		v[1] = v[1] * y
		v[2] = v[2] * z

		# Translate back into xyz
		v[0] = (v[0] * width/2)+(width/2)
		v[1] = (v[1] * height/2)+(height/2)

	if int(parse[4]) < 0 :
		dpoint = vertexList[len(vertexList) + int(parse[4])]
	else :
		dpoint = vertexList[int(parse[4]) - 1]
	# Shifting back into place
	x = opoint[0] - dpoint[0]
	y = opoint[1] - dpoint[1]
	z = opoint[2] - dpoint[2]
	for v in range(0, len(vertexList)):
		(vertexList[v])[0] = (vertexList[v])[0] + x
		(vertexList[v])[1] = (vertexList[v])[1] + y
		(vertexList[v])[2] = (vertexList[v])[2] + z

def multmv( parse ):

	global vertexList
	for v in vertexList:
		v[0] = (v[0] - (width/2))/(width/2)
		v[1] = (v[1] - (height/2))/(height/2)
		v[2] = -v[2]

		tmp = copy.deepcopy(v)

		v[0] = tmp[0]*float(parse[1]) + tmp[1]*float(parse[2]) + tmp[2]*float(parse[3]) + tmp[3]*float(parse[4])
		v[1] = tmp[0]*float(parse[5]) + tmp[1]*float(parse[6]) + tmp[2]*float(parse[7]) + tmp[3]*float(parse[8])
		v[2] = tmp[0]*float(parse[9]) + tmp[1]*float(parse[10]) + tmp[2]*float(parse[11]) + tmp[3]*float(parse[12])
		v[3] = tmp[0]*float(parse[13]) + tmp[1]*float(parse[14]) + tmp[2]*float(parse[15]) + tmp[3]*float(parse[16])
		
		v[0] = (v[0] * (width/2)) + (width/2)
		v[1] = (v[1] * (height/2)) + (height/2)

def frustum( parse ):
	global vertexList
	global modelview
	left = float(parse[1])
	right = float(parse[2])
	bottom = float(parse[3])
	top = float(parse[4])
	near = float(parse[5])
	far = float(parse[6])

	t1 = (2*near)/(right - left)
	t2 = (2*near)/(top-bottom)
	a = (right + left)/(right-left)
	b = (top + bottom)/(top-bottom)
	c = -(far + near)/(far - near)
	d = -(2*far*near)/(far - near)

	print t1
	print t2
	print a
	print b
	print c
	print d
	print "+++++++++++++"

	for v in vertexList:
		v[0] = (v[0] - width/2)/(width/2)
		v[1] = (v[1] - height/2)/(height/2)
		v[2] = -v[2]

		tmp = copy.deepcopy(v)

		v[0] = tmp[0]*t1 + tmp[2]*a
		v[1] = tmp[1]*t2 + tmp[2]*b
		v[2] = tmp[2]*c + tmp[3]*d
		v[3] = v[2]*-1

		asdf

		v[0] = (v[0]*width/2) + (width/2)
		v[1] = (v[1]*height/2) + (height/2)
		v[2] = -v[2]
		print v
	print "=============="

def applyviewmodel():
	global vertexList
	global viewmodel

	for v in vertexList:
		v[0] = (v[0] - width/2)/(width/2)
		v[1] = (v[1] - height/2)/(height/2)
		v[2] = -v[2]

		tmp = copy.deepcopy(v)

		v[0] = tmp[0]*viewmodel[0][0] + tmp[1]*viewmodel[1][0] + tmp[2]*viewmodel[2][0] + tmp[3]*viewmodel[3][0]
		v[1] = tmp[0]*viewmodel[0][1] + tmp[1]*viewmodel[1][1] + tmp[2]*viewmodel[2][1] + tmp[3]*viewmodel[3][1]
		v[2] = tmp[0]*viewmodel[0][2] + tmp[1]*viewmodel[1][2] + tmp[2]*viewmodel[2][2] + tmp[3]*viewmodel[3][2]
		v[3] = tmp[0]*viewmodel[0][3] + tmp[1]*viewmodel[1][3] + tmp[2]*viewmodel[2][3] + tmp[3]*viewmodel[3][3]

		v[0] = (v[0]*width/2) + (width/2)
		v[1] = (v[1]*height/2) + (height/2)
		v[2] = -v[2]



AMBIENT = 1
GAMMA_CORRECTION = 1/2.2

global viewmodel
viewmodel= [[1, 0, 0, 0,],[0, 1, 0, 0,],[0, 0, 1, 0,],[0, 0, 0, 1,]]

objs = []
global vertexList
vertexList = []
virgin = []
color = (255, 255, 255)
cull = False
clip = False
fread = open(sys.argv[1], 'r')
line = fread.readline()
info = line.split()
fileType = info[0]
fileName = info[3]
width = int(info[1])
height = int(info[2])
img = Image.new("RGBA", (width, height), (0,0,0,0))
while (line != ""):
	parse = line.split()
	if parse == []:
		parse
	elif parse[0] == "xyz":
		vertexList.append([(float(parse[1]) * width/2) + width/2, (float(parse[2]) * height/2) + height/2, -float(parse[3]), 1, color[0], color[1], color[2]])
		virgin.append([(float(parse[1]) * width/2) + width/2, (float(parse[2]) * height/2) + height/2, -float(parse[3]), 1, color[0], color[1], color[2]])
	elif parse[0] == "cull":
		cull = True
	elif parse[0] == "trif":
		trif( parse )
	elif parse[0] == "color":
		red = 255*float(parse[1])
		green = 255*float(parse[2])
		blue = 255*float(parse[3])
		color = (red, green, blue)
	elif parse[0] == "translate":
		translate( (float(parse[1]) * width/2), (float(parse[2]) * height/2), -float(parse[3]), 1 ) 
	elif parse[0] == "scale":
		#scale( (float(parse[1]) * width/2), -(float(parse[2]) * height/2), -float(parse[3]), 1 )
		scale( float(parse[1]), float(parse[2]), float(parse[3]), 1)
	elif parse[0] == "lookat":
		lookat( parse )
	elif parse[0] == "rotatex":
		rotatex( parse )
	elif parse[0] == "rotatey":
		rotatey( parse )
	elif parse[0] == "rotatez":
		rotatez( parse )
	elif parse[0] == "loadmv":
		loadmv( parse )
	elif parse[0] == "ortho":
		orth( parse )
	elif parse[0] == "scalec":
		scalec( parse )
	elif parse[0] == "multmv":
		multmv( parse )
	elif parse[0] == "frustum":
		frustum( parse )
	elif parse[0] == "clipplane":
		clip = True
		#clipplane = [(float(parse[1]) * width/2) + width/2, (float(parse[2]) * height/2) + height/2, ((float(parse[3]) * height/2) + height/2), (float(parse[4]) * height/2) + height/2]
		clipplane = [float(parse[1]), float(parse[2]), float(parse[3]), float(parse[4])]
	line = fread.readline()
for v in vertexList:
	print v
lightSource = Vector(0,0,10)
cameraPos = Vector(0,0,10)
for x in range(width):
		for y in range(height):
				ray = Ray( cameraPos, (Vector(x,y,0)-cameraPos).normal())
				col = trace(ray, objs, lightSource, 10)
				if col.x != -1 and col.y != -1 and col.z != -1:
					img.putpixel((x,y),gammaCorrection(col,GAMMA_CORRECTION))
img.save(fileName)