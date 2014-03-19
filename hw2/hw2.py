from math import sqrt, pow, pi, cos, sin
import Image
import sys
 
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
				col = Vector(AMBIENT,AMBIENT,AMBIENT)
		elif intersect.n.dot(light - intersect.p) < 0:
				col = intersect.obj.col * AMBIENT
		else:
				lightRay = Ray(intersect.p, (light-intersect.p).normal())
				if testRay(lightRay, objects, intersect.obj).d == -1:
						lightIntensity = 1000.0/(4*pi*(light-intersect.p).magnitude()**2)
						col = intersect.obj.col * max(intersect.n.normal().dot((light - intersect.p).normal()*lightIntensity), AMBIENT)
				else:
						col = intersect.obj.col * AMBIENT
		return col
	   
def gammaCorrection(color,factor):
		return (int(pow(color.x/255.0,factor)*255),
						int(pow(color.y/255.0,factor)*255),
						int(pow(color.z/255.0,factor)*255))
					   
 
AMBIENT = 1
GAMMA_CORRECTION = 1/2.2

def trif( parse ):
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
			objs.append(Triangle(Vector(vertex1[0], vertex1[1], vertex1[2]), Vector(vertex2[0], vertex2[1], vertex2[2]), Vector(vertex3[0], vertex3[1], vertex3[2]), Vector(color[0], color[1], color[2])))
	else:
		objs.append(Triangle(Vector(vertex1[0], vertex1[1], vertex1[2]), Vector(vertex2[0], vertex2[1], vertex2[2]), Vector(vertex3[0], vertex3[1], vertex3[2]), Vector(color[0], color[1], color[2])))

def translate( x, y, z, w ):
	for v in range(0, len(vertexList)):
		(vertexList[v])[0] = (vertexList[v])[0] + x
		(vertexList[v])[1] = (vertexList[v])[1] + y
		(vertexList[v])[2] = (vertexList[v])[2] + z
		(vertexList[v])[3] = (vertexList[v])[3]

def scale( x, y, z, w ):
	for v in range(0, len(vertexList)):
		# Translate back into relative form
		(vertexList[v])[0] = ((vertexList[v])[0] - width/2)/(width/2)
		(vertexList[v])[1] = ((vertexList[v])[1] - height/2)/(height/2)

		# Scale
		(vertexList[v])[0] = (vertexList[v])[0] * x
		(vertexList[v])[1] = (vertexList[v])[1] * y
		(vertexList[v])[2] = (vertexList[v])[2] * z

		# Translate back into xyz
		(vertexList[v])[0] = ((vertexList[v])[0] * width/2)+(width/2)
		(vertexList[v])[1] = ((vertexList[v])[1] * height/2)+(height/2)

def lookat( parse ):
	print parse
	if int(parse[1]) < 0 :
		eye = vertexList[len(vertexList) + int(parse[1])]
	else :
		eye = vertexList[int(parse[1]) - 1]
	if int(parse[2]) < 0 :
		center = vertexList[len(vertexList) + int(parse[2])]
	else :
		center = vertexList[int(parse[2]) - 1]
	print eye
	eye = Vector(float(eye[0]), float(eye[0]), float(eye[0]))
	center = Vector(float(center[0]), float(center[0]), float(center[0]))
	up = Vector(float(parse[3]), float(parse[4]), float(parse[4]))
	
	zaxis = Vector(center.x - eye.x, center.y - eye.y, center.z - eye.z)
	zaxis.normal()
	tmp = up.cross(zaxis)
	xaxis = Vector(tmp[0], tmp[1], tmp[2])
	xaxis.normal()
	tmp = zaxis.cross(xaxis)
	yaxis = Vector(tmp[0], tmp[1], tmp[2])
	print tmp
	print xaxis.x
	print xaxis.y
	print xaxis.z
	print yaxis.x
	print yaxis.y
	print yaxis.z
	print zaxis.x
	print zaxis.y
	print zaxis.z
	print "========"

def rotatex( parse ):
	degree = -cos(float(parse[1]) * (pi/180))
	for v in vertexList:
		v[1] = cos(degree)*v[1] + sin(degree)*v[2]
		v[2] = -sin(degree)*v[1] + cos(degree)*v[2]

def rotatey( parse ):
	degree = -cos(float(parse[1]) * (pi/180))
	for v in vertexList:
		v[0] = cos(degree)*v[0] - sin(degree)*v[2]
		v[2] = sin(degree)*v[0] + cos(degree)*v[2]

def rotatez( parse ):
	degree = -cos(float(parse[1]) * (pi/180))
	for v in vertexList:
		v[0] = cos(degree)*v[0] + sin(degree)*v[1]
		v[1] = -sin(degree)*v[0] + cos(degree)*v[1]

def loadmv( pase ):
	for v in vertexList:
		#v[0] = (v[0] - width/2)/(width/2)
		#v[1] = (v[1] - height/2)/(height/2)
		#v[2] = -v[2]

		v[0] = v[0]*float(parse[1]) + v[1]*float(parse[5]) + v[2]*float(parse[9]) + float(parse[13])
		v[1] = v[0]*float(parse[2]) + v[1]*float(parse[6]) + v[2]*float(parse[10]) + float(parse[14])
		v[2] = v[0]*float(parse[3]) + v[1]*float(parse[7]) + v[2]*float(parse[11]) + float(parse[15])
		
		#v[0] = (v[0] * width/2)+(width/2)
		#v[1] = (v[1] * height/2)+(height/2)
		#v[2] = -v[2]

objs = []
vertexList = []
color = (255, 255, 255)
cull = False
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
		vertexList.append([(float(parse[1]) * width/2) + width/2, -(float(parse[2]) * height/2) + height/2, -float(parse[3]), 1])
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
		translate( (float(parse[1]) * width/2), -(float(parse[2]) * height/2), -float(parse[3]), 1 ) 
	elif parse[0] == "scale":
		#scale( (float(parse[1]) * width/2), -(float(parse[2]) * height/2), -float(parse[3]), 1 )
		scale( float(parse[1]), float(parse[2]), float(parse[3]), 1)
	elif parse[0] == "lookat":
		# lookat( parse )
		print "need to do lookat"
	elif parse[0] == "rotatex":
		rotatex( parse )
	elif parse[0] == "rotatey":
		rotatey( parse )
	elif parse[0] == "rotatez":
		rotatez( parse )
	elif parse[0] == "loadmv":
		loadmv( parse )
	line = fread.readline()

lightSource = Vector(0,0,0)
cameraPos = Vector(0,0,10)
for x in range(width):
		#print x
		for y in range(height):
				#ray = Ray( cameraPos, (Vector(x/12.0-5,y/12.0-5,0)-cameraPos).normal())
				ray = Ray( cameraPos, (Vector(x,y,0)-cameraPos).normal())
				col = trace(ray, objs, lightSource, 10)
				img.putpixel((x,(width-1)-y),gammaCorrection(col,GAMMA_CORRECTION))
img.save(fileName)	



#objs = []
#objs.append(Plane( Vector(0,0,-14), Vector(0,0,1), Vector(255,255,255)))
#objs.append(Triangle(Vector(10, -10, 1.5), Vector(10, 10, -0.5), Vector(-10, -10, -1.5), Vector(255, 0, 0)))
#lightSource = Vector(0,0,10)
#img = Image.new("RGB",(120,120))
#cameraPos = Vector(0,0,100)
#for x in range(120):
#		print x
#		for y in range(120):
#				ray = Ray( cameraPos, (Vector(x/12.0-5,y/12.0-5,0)-cameraPos).normal())
#				col = trace(ray, objs, lightSource, 10)
#				img.putpixel((x,119-y),gammaCorrection(col,GAMMA_CORRECTION))
#img.save("trace.bmp","BMP")