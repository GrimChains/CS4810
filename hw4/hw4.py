import math
import sys
import copy
import threading
import time
import pygame


class Pixel(threading.Thread):

	def run(self):
		y = self.y
		global width
		global height
		global imgLock
		flipflop = self.flipflop
		t = float(height - 2 * y) / max(width, height)
		while True:
			flipflop = not flipflop
			for x in range(width):
				if (x % 2 == 0) == flipflop:
					continue
				s = float(2 * x - width) / max(width, height)
				ray = Ray(cameraPos, forward + (right * s) + (up * t))
				col = trace(ray, objs)
				if col.x != -1 and col.y != -1 and col.z != -1:
					try:
						square.fill((min(int(col.x),255), min(int(col.y),255), min(int(col.z),255)))
					except Exception:
						imgLock.acquire()
						print min(int(col.x),255)
						print min(int(col.y),255)
						print min(int(col.z),255)
						print "=========="
						imgLock.release()
				else:
					square.fill((0, 0, 0))
				draw_me = pygame.Rect((x, y, 1, 1))
				screen.blit(square, draw_me)


class ObjFile(threading.Thread):

	def run( self ):
		global fileLock
		global bulbs
		global suns
		global objs
		global width
		global height
		fileLock.acquire()
		self.fread = open(self.fileName, 'r')
		fread = self.fread
		line = fread.readline()
		info = line.split()
		width = int(info[1])
		height = int(info[2])
		fileLock.release()
		while True:
			old_bulbs = []
			old_suns = []
			old_objs = []
			line = fread.readline()
			while line != "":
				parse = line.split()
				if parse == []:
					pass
				elif parse[0] == "bulb" :
					x = float(parse[1])
					y = float(parse[2])
					z = float(parse[3])
					old_bulbs.append([x, y, z, float(parse[4]), float(parse[5]), float(parse[6])])
				elif parse[0] == "sun" :
					old_suns.append([float(parse[1]), float(parse[2]), float(parse[3]), float(parse[4]), float(parse[5]), float(parse[6])])
				elif parse[0] == "plane" :
					x = float(parse[1])
					y = float(parse[2])
					z = float(parse[3])
					d = float(parse[4])
					if x != 0:
						old_objs.append( Plane( Vector( (-d/x), 0, 0), Vector( x, y, z), Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7]))) )
					elif y != 0 :
						old_objs.append( Plane( Vector( 0, (-d/y), 0), Vector( x, y, z), Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7]))) )
					elif z != 0 :
						old_objs.append( Plane( Vector( 0, 0, (-d/z) ), Vector( x, y, z), Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7]))) )
				elif parse[0] == "sphere" :
					x = float(parse[1])
					y = float(parse[2])
					z = float(parse[3])
					r = float(parse[4])
					old_objs.append( Sphere( Vector( x, y, z), r, Vector(float(parse[5])*255.0, float(parse[6])*255.0, float(parse[7])*255.0)))
				elif parse[0] == "rect" :
					x = float(parse[1])
					y = float(parse[2])
					z = float(parse[3])
					d = float(parse[4])

					minX = float(parse[8]);
					maxX = float(parse[9]);
					minY = float(parse[10]);
					maxY = float(parse[11]);
					minZ = float(parse[12]);
					maxZ = float(parse[13]);

					if x != 0:
						old_objs.append( Rectangle( Vector( (-d/x), 0, 0), Vector( x, y, z), Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7])), minX, maxX, minY, maxY, minZ, maxZ) )
					elif y != 0 :
						old_objs.append( Rectangle( Vector( 0, (-d/y), 0), Vector( x, y, z), Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7])), minX, maxX, minY, maxY, minZ, maxZ) )
					elif z != 0 :
						old_objs.append( Rectangle( Vector( 0, 0, (-d/z) ), Vector( x, y, z), Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7])), minX, maxX, minY, maxY, minZ, maxZ) )
				#elif parse[0] == "eye" :
				#    x = float(parse[1])
				#    y = float(parse[2])
				#    z = float(parse[3])
				#    cameraPos = Vector( x, y, z )
				#elif parse[0] == "forward" :
				#    forward = Vector( float(parse[1]), float(parse[2]), float(parse[3]))
				#    tmp = forward.cross(up)
				#    right = Vector( tmp[0], tmp[1], tmp[2]).normal()
				#    tmp = right.cross(forward)
				#    up = Vector( tmp[0], tmp[1], tmp[2] ).normal()
				#elif parse[0] == "up" :
				#    temp = Vector( float(parse[1]), float(parse[2]), float(parse[3]))
				#    tmp = forward.cross(temp)
				#    right = Vector( tmp[0], tmp[1], tmp[2]).normal()
				#    tmp = right.cross(forward)
				#    up = Vector( tmp[0], tmp[1], tmp[2]).normal()
				line = fread.readline()
			fread.seek(0)
			if old_bulbs != bulbs:
				bulbs = copy.deepcopy(old_bulbs)
			if old_suns != suns:
				suns = copy.deepcopy(old_suns)
			if old_objs != objs:
				objs = copy.deepcopy(old_objs)
			time.sleep(1)


class Vector(object):

		def __init__(self, x, y, z):
				self.x = x
				self.y = y
				self.z = z

		def dot(self, b):
				return self.x*b.x + self.y*b.y + self.z*b.z

		def cross(self, b):
				return self.y*b.z-self.z*b.y, self.z*b.x-self.x*b.z, self.x*b.y-self.y*b.x

		def magnitude(self):
				return math.sqrt(self.x**2+self.y**2+self.z**2)

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


def ray_sphere(p0, d, sph):

	pc = sph.c
	r = sph.r

	p0c = p0 - pc

	a = d.dot(d)
	b = (d * 2).dot(p0 - pc)
	c = p0c.dot(p0c) - r**2

	try:
		t1 = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
	except ValueError:
		t1 = None
	try:
		t2 = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
	except ValueError:
		t2 = None

	return t1, t2


class Rectangle(object):
	def __init__(self, point, normal, color, minX, maxX, minY, maxY, minZ, maxZ):
		self.point = point
		self.normal = normal
		self.color = color
		self.minX = minX;
		self.maxX = maxX;
		self.minY = minY;
		self.maxY = maxY;
		self.minZ = minZ;
		self.maxZ = maxZ;


	def intersection(self, l):
				d = l.d.dot(self.n)
				if d == 0:
						return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
				else:
						d = (self.p - l.o).dot(self.n) / d
						point = l.o+l.d*d;

						if (point.x >= self.minX and point.x <= self.maxX and point.y >= self.minY and point.y <= self.maxY and point.z >= self.minZ and point.z <= self.maxZ) :
							return Intersection(l.o+l.d*d, d, self.n, self)
						else :
							return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
	
class Sphere(object):

		def __init__(self, center, radius, color):
				self.c = center
				self.r = radius
				self.col = color

		def intersection(self, l):
				points = ray_sphere(l.o, l.d, self)
				if points == (None, None):
					return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
				elif points[0] != None and points[1] != None:
					t = min(points)
				else:
					t = max(points)
				return Intersection( (l.o + l.d * t), math.sqrt( (l.d.x * t)**2 + (l.d.y * t)**2 + (l.d.z * t)**2), self.normal(l.o + l.d*t), self )


		def normal(self, b):
				return (b - self.c).normal()


class Box(object):
		def __init__(self, verts, color):
				self.verts = verts;
				self.color = color;

class Plane(object):

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



class Ray(object):

		def __init__(self, origin, direction):
				self.o = origin
				self.d = direction


class Intersection(object):

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
			lightDir = Vector( b[0] - intersect.p.x, b[1] - intersect.p.y, b[2] - intersect.p.z).normal()
			ray = Ray( intersect.p, lightDir )
			inter = testRay( ray, objects, intersect.obj)
			dist = math.sqrt( pow( intersect.p.x - b[0], 2) + pow( intersect.p.y - b[1], 2) + pow( intersect.p.z - b[2], 2) )
			if inter.d == -1 or inter.d > dist:
				col = Vector( col.x + intersect.obj.col.x * b[3] * max(intersect.n.dot(lightDir), 0), col.y + intersect.obj.col.y * b[4] * max(intersect.n.dot(lightDir), 0), col.z + intersect.obj.col.z * b[5] * max(intersect.n.dot(lightDir), 0))
		for s in suns:
			lightDir = Vector( s[0], s[1], s[2] )
			ray = Ray( intersect.p, lightDir )
			inter = testRay( ray, objs, intersect.obj)
			if inter.d == -1:
				col = Vector( col.x + intersect.obj.col.x * s[3] * max(intersect.n.dot(lightDir), 0), col.y + intersect.obj.col.y * s[4] * max(intersect.n.dot(lightDir), 0), col.z + intersect.obj.col.z * s[5] * max(intersect.n.dot(lightDir), 0))
	return col

t0 = time.time()
global objs
global suns
global bulbs
global width
global height
global pixBuff
global fileLock
global square
global screen

pygame.init()
fileLock = threading.Lock()
sensitivity = 0.05
width = 1
height = 1
square = pygame.Surface((1,1))
imgLock = threading.Lock()
pixBuff = []
objs = []
suns = []
bulbs = []
cameraPos = Vector(0,0,0)

objFile = ObjFile()
objFile.fileName = sys.argv[1]
objFile.start()

# Basically waiting on objFile to do its thing.
fileLock.acquire()
fileLock.release()

screen = pygame.display.set_mode((width, height))

forward = Vector( 0.0, 0.0, -1.0 )
up = Vector( 0.0, 1.0, 0.0 )
right = Vector( 1.0, 0.0, 0.0 )


# Thread factory
flip = True
for y in range(height):
	px = Pixel()
	px.flipflop = flip
	flip = not flip
	px.y = y
	px.start()


# Used for frame limiting
clock = pygame.time.Clock()
while True:
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			print event.key
			if event.key == pygame.K_w:
				cameraPos = Vector(cameraPos.x, cameraPos.y, -sensitivity+cameraPos.z)
			elif event.key == pygame.K_s:
				cameraPos = Vector(cameraPos.x, cameraPos.y, sensitivity+cameraPos.z)
			elif event.key == pygame.K_a:
				cameraPos = Vector(-sensitivity+cameraPos.x, cameraPos.y, cameraPos.z)
			elif event.key == pygame.K_d:
				cameraPos = Vector(sensitivity+cameraPos.x, cameraPos.y, cameraPos.z)
			elif event.key == pygame.K_LCTRL:
				cameraPos = Vector(cameraPos.x, -sensitivity+cameraPos.y, cameraPos.z)
			elif event.key == pygame.K_SPACE:
				cameraPos = Vector(cameraPos.x, sensitivity+cameraPos.y, cameraPos.z)
			elif event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
	#clock.tick(10) # lock framerate to 10 fps.
