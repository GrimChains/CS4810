from math import sqrt, pow, pi
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
						return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
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
	   
def trace(ray, objects, maxRecur):
	global suns
	global bulbs
	global cameraPos
	if maxRecur < 0:
		return (0,0,0)
	intersect = testRay(ray, objects)
	if intersect.d == -1 or intersect.p.z < -100000000000:
		col = Vector(-1,-1,-1)
	else :
		col = Vector( 0, 0, 0 )
		for b in bulbs:
			lightDir = Vector(  b[0] - intersect.p.x,  b[1] - intersect.p.y,  b[2] - intersect.p.z).normal()
			ray = Ray( intersect.p, lightDir )
			inter = testRay( ray, objs, intersect.obj)
			dist = sqrt( pow( intersect.p.x - b[0], 2) + pow( intersect.p.y - b[1], 2) + pow( intersect.p.z - b[2], 2) )
			if inter.d == -1 or inter.d > dist:
				col = Vector( col.x + intersect.obj.col.x * b[3] * intersect.n.dot(lightDir), col.y + intersect.obj.col.y * b[4] * intersect.n.dot(lightDir), col.z + intersect.obj.col.z * b[5] * intersect.n.dot(lightDir))
		for s in suns:
			lightDir = Vector( s[0], s[1], s[2] )
			ray = Ray( intersect.p, lightDir )
			inter = testRay( ray, objs, intersect.obj)
			if inter.d == -1:
				col = Vector( col.x + intersect.obj.col.x * s[3] * intersect.n.dot(lightDir), col.y + intersect.obj.col.y * s[4] * intersect.n.dot(lightDir), col.z + intersect.obj.col.z * s[5] * intersect.n.dot(lightDir))
	return col


global objs
global suns
global bulbs
objs = []
suns = []
bulbs = []
cameraPos = Vector(0,0,10)


fread = open(sys.argv[1], 'r')
line = fread.readline()
info = line.split()
fileType = info[0]
fileName = info[3]
width = int(info[1])
height = int(info[2])
img = Image.new("RGBA", (width, height), (0,0,0,0))


forward = Vector( 0, 0, -1 )
up = Vector( 0, 1, 0 )
right = Vector( 1, 0, 0 )

while (line != ""):
		parse = line.split()
		if parse == []:
				parse
		elif parse[0] == "bulb" :
				#bulbs.append([5.0*float(parse[1]), 5.0*float(parse[2]), 5.0*float(parse[3]), float(parse[4])*255.0, float(parse[5])*255.0, float(parse[6])*255.0])
				#bulbs.append([5.0*float(parse[1]), 5.0*float(parse[2]), 5.0*float(parse[3]), float(parse[4]), float(parse[5]), float(parse[6])])
				bulbs.append([5.0*float(parse[1]), 5.0*float(parse[2]), 5.0*float(parse[3]), float(parse[4]), float(parse[5]), float(parse[6])])
		elif parse[0] == "sun" :
				suns.append([float(parse[1]), float(parse[2]), float(parse[3]), float(parse[4]), float(parse[5]), float(parse[6])])
				#suns.append([5.0*float(parse[1]), 5.0*float(parse[2]), 5.0*float(parse[3]), float(parse[4]), float(parse[5]), float(parse[6])])
				#suns.append([float(parse[1]), float(parse[2]), float(parse[3]), float(parse[4]), float(parse[5]), float(parse[6])])
		elif parse[0] == "plane" :
				if float(parse[1]) != 0:
						objs.append( Plane( Vector( 5.0*(-float(parse[4])/float(parse[1])), 0, 0), Vector( 5.0*float(parse[1]), 5.0*float(parse[2]), 5.0*float(parse[3])), Vector(255.0*float(parse[5]), 255.0*float(parse[6]), 255.0*float(parse[7]))) )
				elif float(parse[2]) != 0 :
						objs.append( Plane( Vector( 0, 5.0*(-float(parse[4])/float(parse[2])), 0), Vector( 5.0*float(parse[1]), 5.0*float(parse[2]), 5.0*float(parse[3])), Vector(255.0*float(parse[5]), 255.0*float(parse[6]), 255.0*float(parse[7]))) )
				elif float(parse[2]) != 0 :
						objs.append( Plane( Vector( 0, 0, 5.0*(-float(parse[4])/float(parse[3])) ), Vector( 5.0*float(parse[1]), 5.0*float(parse[2]), 5.0*float(parse[3])), Vector(255.0*float(parse[5]), 255.0*float(parse[6]), 255.0*float(parse[7]))) )
		elif parse[0] == "sphere" :
				objs.append( Sphere( Vector(5.0*float(parse[1]), 5.0*float(parse[2]), 5.0*float(parse[3])), 10.0*float(parse[4]), Vector(float(parse[5])*255.0, float(parse[6])*255.0, float(parse[7])*255.0)) )
		elif parse[0] == "eye" :
				cameraPos = Vector( 5.0*float(parse[1]), 5.0*float(parse[2]), 5.0*float(parse[3]) )
		line = fread.readline()



for x in range(width):
		for y in range(height):
				ray = Ray( cameraPos, (Vector(x/(float(width)/10.0)-5,y/(float(height)/10.0)-5,0)-cameraPos).normal())
				col = trace(ray, objs, 10)
				if col.x != -1 and col.y != -1 and col.z != -1 :
						img.putpixel((int(x),height-1-int(y)),(int(col.x), int(col.y), int(col.z)))
img.save(fileName)



"""s = (2*x - width) / max(width, height)
t = (height - 2*y) / max(width, height)
ray = Ray( cameraPos, (Vector( forward.x + (s * right.x) + (t * up.x), forward.y + (s * right.y) + (t * up.y), forward.z + (s * right.z) + (t * up.z)) ) )"""