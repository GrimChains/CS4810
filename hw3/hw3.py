from math import sqrt, pow, pi, cos, sin
import Image
import sys
import copy
 
class Sphere( object ):
       
        def __init__(self, center, radius, color):
                self.c = center
                self.r = radius
                self.col = color
               
        def intersection(self, l):
                q = l.d.dot(l.o - self.c)**2 - (l.o - self.c).dot(l.o - self.c) + self.r**2
                if q < 0:
                        return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
                else:
                        d = -l.d.dot(l.o - self.c)
                        d1 = d - sqrt(q)
                        d2 = d + sqrt(q)
                        if 0 < d1 and ( d1 < d2 or d2 < 0):
                                return Intersection(l.o+l.d*d1, d1, self.normal(l.o+l.d*d1), self)
                        elif 0 < d2 and ( d2 < d1 or d1 < 0):
                                return Intersection(l.o+l.d*d2, d2, self.normal(l.o+l.d*d2), self)
                        else:
                                return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)   
                       
        def normal(self, b):
                return (b - self.c).normal()

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

def mult4x4(a, b):
	tmp = copy.deepcopy(a)
	a[0][0] = tmp[0][0] * b[0][0] + tmp[1][0] * b[0][1] + tmp[2][0] * b[0][2] + tmp[3][0] * b[0][3]
	a[1][0] = tmp[0][0] * b[1][0] + tmp[1][0] * b[1][1] + tmp[2][0] * b[1][2] + tmp[3][0] * b[1][3]
	a[2][0] = tmp[0][0] * b[2][0] + tmp[1][0] * b[2][1] + tmp[2][0] * b[2][2] + tmp[3][0] * b[2][3]
	a[3][0] = tmp[0][0] * b[3][0] + tmp[1][0] * b[3][1] + tmp[2][0] * b[3][2] + tmp[3][0] * b[3][3]
	a[0][1] = tmp[0][1] * b[0][0] + tmp[1][1] * b[0][1] + tmp[2][1] * b[0][2] + tmp[3][1] * b[0][3]
	a[1][1] = tmp[0][1] * b[1][0] + tmp[1][1] * b[1][1] + tmp[2][1] * b[1][2] + tmp[3][1] * b[1][3]
	a[2][1] = tmp[0][1] * b[2][0] + tmp[1][1] * b[2][1] + tmp[2][1] * b[2][2] + tmp[3][1] * b[2][3]
	a[3][1] = tmp[0][1] * b[3][0] + tmp[1][1] * b[3][1] + tmp[2][1] * b[3][2] + tmp[3][1] * b[3][3]
	a[0][2] = tmp[0][2] * b[0][0] + tmp[1][2] * b[0][1] + tmp[2][2] * b[0][2] + tmp[3][2] * b[0][3]
	a[1][2] = tmp[0][2] * b[1][0] + tmp[1][2] * b[1][1] + tmp[2][2] * b[1][2] + tmp[3][2] * b[1][3]
	a[2][2] = tmp[0][2] * b[2][0] + tmp[1][2] * b[2][1] + tmp[2][2] * b[2][2] + tmp[3][2] * b[2][3]
	a[3][2] = tmp[0][2] * b[3][0] + tmp[1][2] * b[3][1] + tmp[2][2] * b[3][2] + tmp[3][2] * b[3][3]
	a[0][3] = tmp[0][3] * b[0][0] + tmp[1][3] * b[0][1] + tmp[2][3] * b[0][2] + tmp[3][3] * b[0][3]
	a[1][3] = tmp[0][3] * b[1][0] + tmp[1][3] * b[1][1] + tmp[2][3] * b[1][2] + tmp[3][3] * b[1][3]
	a[2][3] = tmp[0][3] * b[2][0] + tmp[1][3] * b[2][1] + tmp[2][3] * b[2][2] + tmp[3][3] * b[2][3]
	a[3][3] = tmp[0][3] * b[3][0] + tmp[1][3] * b[3][1] + tmp[2][3] * b[3][2] + tmp[3][3] * b[3][3]
	return a

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
						if t1 >= 0 and t2 >= 0 and t3 >= 0 and temp.p.z < 0 and temp.p.z > -1: # Point q is within our triangle
							return temp
						else:
							return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
			   
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
		if clip and tx * clipplane[0] + ty * clipplane[1] + intersect.p.z * clipplane[2] + clipplane[3] <= 0:
			col = Vector(-1, -1, -1)
		return col

def lookat( parse ):
	global vertexList
	global viewmodel

	viewmodel = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

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

	tmp = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]


	tmp[0][0] = X.x
	tmp[1][0] = X.y
	tmp[2][0] = X.z
	tmp[3][0] = -eye.dot(X)
	tmp[0][1] = Y.x
	tmp[1][1] = Y.y
	tmp[2][1] = Y.z
	tmp[3][1] = -eye.dot(Y)
	tmp[0][2] = Z.x
	tmp[1][2] = Z.y
	tmp[2][2] = Z.z
	tmp[3][2] = -eye.dot(Z)
	tmp[0][3] = 0
	tmp[1][3] = 0
	tmp[2][3] = 0
	tmp[3][3] = 1

	viewmodel = mult4x4(viewmodel, tmp)

def frustum( parse ):
	global vertexList
	global viewmodel
	left = float(parse[1])
	right = float(parse[2])
	bottom = float(parse[3])
	top = float(parse[4])
	near = float(parse[5])
	far = -float(parse[6])

	t1 = (2*near)/(right - left)
	t2 = (2*near)/(top-bottom)
	a = (right + left)/(right-left)
	b = (top + bottom)/(top-bottom)
	c = -(far + near)/(far - near)
	d = -(2*far*near)/(far - near)

	tmp = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	tmp[0][0] = t1
	tmp[2][0] = a
	tmp[1][1] = t2
	tmp[2][1] = b
	tmp[2][2] = c
	tmp[3][2] = d
	tmp[3][3] = -1
	viewmodel = mult4x4(viewmodel, tmp)

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
		vertexList = copy.deepcopy(virgin)
	elif parse[0] == "color":
		red = 255*float(parse[1])
		green = 255*float(parse[2])
		blue = 255*float(parse[3])
		color = (red, green, blue)
	elif parse[0] == "translate":
		translate( float(parse[1]), float(parse[2]), float(parse[3]) )
	elif parse[0] == "scale":
		scale( float(parse[1]), float(parse[2]), float(parse[3]) )
	elif parse[0] == "lookat":
		lookat( parse )
	elif parse[0] == "rotatex":
		rotatex( parse )
	elif parse[0] == "rotatey":
		rotatey( parse )
	elif parse[0] == "rotatez":
		rotatez( parse )
	elif parse[0] == "rotate":
		rotate( parse )
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
	elif parse[0] == "rotatec":
		rotatec( parse )
	elif parse[0] == "clipplane":
		clip = True
		clipplane = [float(parse[1]), float(parse[2]), float(parse[3]), float(parse[4])]
	line = fread.readline()
lightSource = Vector(0,0,10)
cameraPos = Vector(0,0,10)
for x in range(width):
		for y in range(height):
				ray = Ray( cameraPos, (Vector(x-2.5,y-2.5,0)-cameraPos).normal())
				col = trace(ray, objs, lightSource, 10)
				if col.x != -1 and col.y != -1 and col.z != -1:
					img.putpixel((int(x),int(y)),(int(col.x), int(col.y), int(col.z)))
img.save(fileName)