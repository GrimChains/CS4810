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
	   
def trace(ray, objects):
	global suns
	global bulbs
	global cameraPos
	intersect = testRay(ray, objects)
	if intersect.d == -1 or intersect.p.z < -10000000:
		return Vector(-1,-1,-1)
	else :
		eyeDir = Vector( cameraPos.x - intersect.p.x, cameraPos.y - intersect.p.y, cameraPos.z - intersect.p.z)
		if intersect.n.dot(eyeDir) < 0 :
			intersect.n = intersect.n * -1
		col = Vector( 0, 0, 0 )
		for b in bulbs:
			lightDir = Vector(  b[0] - intersect.p.x,  b[1] - intersect.p.y,  b[2] - intersect.p.z).normal()
			ray = Ray( intersect.p, lightDir )
			inter = testRay( ray, objects, intersect.obj)
			dist = sqrt( pow( intersect.p.x - b[0], 2) + pow( intersect.p.y - b[1], 2) + pow( intersect.p.z - b[2], 2) )
			if inter.d == -1 or inter.d > dist:
				"""print x
				print y
				print inter.d
				print "bam"""
				col = Vector( col.x + intersect.obj.col.x * b[3] * max(intersect.n.dot(lightDir), 0), col.y + intersect.obj.col.y * b[4] * max(intersect.n.dot(lightDir), 0), col.z + intersect.obj.col.z * b[5] * max(intersect.n.dot(lightDir), 0))
		for s in suns:
			lightDir = Vector( s[0], s[1], s[2] )
			ray = Ray( intersect.p, lightDir )
			inter = testRay( ray, objs, intersect.obj)
			if inter.d == -1:
				col = Vector( col.x + intersect.obj.col.x * s[3] * max(intersect.n.dot(lightDir), 0), col.y + intersect.obj.col.y * s[4] * max(intersect.n.dot(lightDir), 0), col.z + intersect.obj.col.z * s[5] * max(intersect.n.dot(lightDir), 0))
	return col


global objs
global suns
global bulbs
objs = []
suns = []
bulbs = []
cameraPos = Vector(0,0,0)

fread = open(sys.argv[1], 'r')
line = fread.readline()
info = line.split()
fileType = info[0]
fileName = info[3]
width = int(info[1])
height = int(info[2])

img = Image.new("RGBA", (width, height), (0,0,0,0))

forward = Vector( 0.0, 0.0, -1.0 )
up = Vector( 0.0, 1.0, 0.0 )
right = Vector( 1.0, 0.0, 0.0 )

while (line != ""):
	parse = line.split()
	if parse == []:
		parse
	elif parse[0] == "bulb" :
		x = float(parse[1])
		y = float(parse[2])
		z = float(parse[3])
		bulbs.append([x, y, z, float(parse[4]), float(parse[5]), float(parse[6])])
	elif parse[0] == "sun" :
		suns.append([float(parse[1]), float(parse[2]), float(parse[3]), float(parse[4]), float(parse[5]), float(parse[6])])
	elif parse[0] == "aplane" :
		x = float(parse[1])
		y = float(parse[2])
		z = float(parse[3])
		d = float(parse[4])
		if x != 0:
			objs.append( Plane( Vector( (-d/x), 0, 0), Vector( x, y, z), Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7]))) )
		elif y != 0 :
			objs.append( Plane( Vector( 0, (-d/y), 0), Vector( x, y, z), Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7]))) )
		elif z != 0 :
			objs.append( Plane( Vector( 0, 0, (-d/z) ), Vector( x, y, z), Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7]))) )
	elif parse[0] == "sphere" :
		x = float(parse[1])
		y = float(parse[2])
		z = float(parse[3])
		r = float(parse[4])
		objs.append( Sphere( Vector( x, y, z), r, Vector(float(parse[5])*255.0, float(parse[6])*255.0, float(parse[7])*255.0)))
	elif parse[0] == "eye" :
		x = float(parse[1])
		y = float(parse[2])
		z = float(parse[3])
		cameraPos = Vector( x, y, z )
	elif parse[0] == "forward" :
		forward = Vector( float(parse[1]), float(parse[2]), float(parse[3]))
		tmp = forward.cross(up)
		right = Vector( tmp[0], tmp[1], tmp[2]).normal()
		tmp = right.cross(forward)
		up = Vector( tmp[0], tmp[1], tmp[2] ).normal()
	elif parse[0] == "up" :
		temp = Vector( float(parse[1]), float(parse[2]), float(parse[3]))
		tmp = forward.cross(temp)
		right = Vector( tmp[0], tmp[1], tmp[2]).normal()
		tmp = right.cross(forward)
		up = Vector( tmp[0], tmp[1], tmp[2]).normal()
	line = fread.readline()


for x in range(width):
	#print x
	for y in range(height):
		s = float(2 * x - width) / max(width, height)
		t = float(height - 2 * y) / max(width, height)
		ray = Ray( cameraPos, forward + (right * s) + (up * t))
		col = trace(ray, objs)
		if col.x != -1 and col.y != -1 and col.z != -1 :
			img.putpixel((int(x),int(y)),(int(col.x), int(col.y), int(col.z)))
img.save(fileName)