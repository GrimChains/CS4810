import math
import sys
import copy
import threading
import time
import pygame
import hashlib
from numbers import Number


class Pixel(threading.Thread):

	def run(self):
		y = self.y
		x = self.x
		x_bound = self.x_bound
		y_bound = self.y_bound
		global width,height, screen, errorLock, running, cameraPos, forward, right, up, numThreadsCompleted, totalThreadTime
		t = float(height - 2 * y) / max(width, height)
		while running:
			startTime = time.clock();
			hash = oldHash;
			for i in range(x, min(x_bound, width)):
				for j in range(y, min(y_bound, height)):
					t = float(height - 2 * j) / max(width, height)
					s = float(2 * i - width) / max(width, height)
					ray = Ray(cameraPos, forward + (right * s) + (up * t))
					col = trace(ray, objs, hash)
					screen.fill((max(min(int(col.x),255),0), max(min(int(col.y),255),0), max(min(int(col.z),255),0)), pygame.Rect(i,j,1,1))

			endTime = time.clock();
			numThreadsCompleted += 1;
			totalThreadTime += endTime - startTime;


class ObjFile(threading.Thread):

	def run( self ):
		global fileLock
		global bulbs
		global suns
		global objs
		global width
		global height
		global running
		global verts
		global cache
		global oldHash
		global lastCacheReset

		fileLock.acquire()
		self.fread = open(self.fileName, 'r')
		fread = self.fread
		line = fread.readline()
		info = line.split()
		width = int(info[1])
		height = int(info[2])
		fileLock.release()
		while running:
			try:
				old_bulbs = []
				old_suns = []
				old_objs = []
				old_verts = []

				fileList = []
				fileString = "";
				line = fread.readline()
				while line != "":
					fileList.append(line);
					fileString += line;
					line = fread.readline()
				fread.seek(0)

				m = hashlib.md5();
				m.update(fileString);
				hash = m.digest();

				if (hash != oldHash):
					for line in fileList:
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
						elif parse[0] == "vertex":
							x = float(parse[1])
							y = float(parse[2])
							z = float(parse[3])

							old_verts.append( Vector(x, y ,z))
						elif parse[0] == "rect":
							red = 255*float(parse[1])
							green = 255*float(parse[2])
							blue = 255*float(parse[3])

							v1 = old_verts[int(parse[4])]
							v2 = old_verts[int(parse[5])]
							v3 = old_verts[int(parse[6])]
							v4 = old_verts[int(parse[7])]

							old_objs.append( Rectangle(Vector(red, green, blue), v1, v2, v3, v4))
						elif parse[0] == "box" :
							red = 255*float(parse[1])
							green = 255*float(parse[2])
							blue = 255*float(parse[3])

							v1 = old_verts[int(parse[4])]
							v2 = old_verts[int(parse[5])]
							v3 = old_verts[int(parse[6])]
							v4 = old_verts[int(parse[7])]
							v5 = old_verts[int(parse[8])]
							v6 = old_verts[int(parse[9])]
							v7 = old_verts[int(parse[10])]
							v8 = old_verts[int(parse[11])]

							bVerts = [ v1, v2, v3, v4, v5, v6, v7, v8 ]

							bVerts= sorted(bVerts, key=lambda vert: vert.x)
							old_objs.append( Rectangle(Vector(red, green, blue), bVerts[0], bVerts[1], bVerts[2], bVerts[3]))
							old_objs.append( Rectangle(Vector(red, green, blue), bVerts[4], bVerts[5], bVerts[6], bVerts[7]))

							bVerts= sorted(bVerts, key=lambda vert: vert.y)
							old_objs.append( Rectangle(Vector(red, green, blue), bVerts[0], bVerts[1], bVerts[2], bVerts[3]))
							old_objs.append( Rectangle(Vector(red, green, blue), bVerts[4], bVerts[5], bVerts[6], bVerts[7]))

							bVerts= sorted(bVerts, key=lambda vert: vert.z)
							old_objs.append( Rectangle(Vector(red, green, blue), bVerts[0], bVerts[1], bVerts[2], bVerts[3]))
							old_objs.append( Rectangle(Vector(red, green, blue), bVerts[4], bVerts[5], bVerts[6], bVerts[7]))
						elif parse[0] == "triangle":
							v0 = old_verts[int(parse[1])]
							v1 = old_verts[int(parse[2])]
							v2 = old_verts[int(parse[3])]
							tri_color = Vector(255*float(parse[4]), 255*float(parse[5]), 255*float(parse[6]))
							old_objs.append(Triangle(v0, v1, v2, tri_color))
						elif parse[0] == "tetrahedron":
							v0 = old_verts[int(parse[1])]
							v1 = old_verts[int(parse[2])]
							v2 = old_verts[int(parse[3])]
							v3 = old_verts[int(parse[4])]

							tetra_color = Vector(255*float(parse[5]), 255*float(parse[6]), 255*float(parse[7]))
							t1 = Triangle(v0, v1, v2, tetra_color)
							t2 = Triangle(v0, v1, v3, tetra_color)
							t3 = Triangle(v0, v2, v3, tetra_color)
							t4 = Triangle(v1, v2, v3, tetra_color)
							old_objs.append(t1)
							old_objs.append(t2)
							old_objs.append(t3)
							old_objs.append(t4)
							Tetrahedron((v0, v1, v2, v3), (t1, t2, t3, t4))

					print("FILE IS DIFFERENT! CLEARING CACHE");
					cache.clear();
					oldHash = hash;
					lastCacheReset = time.time()

					if old_bulbs != bulbs:
						bulbs = copy.deepcopy(old_bulbs)
					if old_suns != suns:
						suns = copy.deepcopy(old_suns)
					if old_objs != objs:
						objs = copy.deepcopy(old_objs)
					if old_verts != verts:
						verts = copy.deepcopy(old_verts)
			except Exception:
				print "There was an error in the object file."
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
		if isinstance(b, Vector):
			return Vector(self.x + b.x, self.y+b.y, self.z+b.z)
		elif isinstance(b, Number):
			return Vector(self.x + b, self.y + b, self.z + b)

	def __sub__(self, b):
		return Vector(self.x-b.x, self.y-b.y, self.z-b.z)

	def __mul__(self, b):
		assert type(b) == float or type(b) == int
		return Vector(self.x*b, self.y*b, self.z*b)

class Rectangle(object):
	def __init__(self, color, v1, v2, v3, v4):
		self.col = color

		rVerts = [ v1, v2, v3, v4 ]

		line1 = None
		line2 = None

		rVerts = sorted(rVerts, key=lambda vert: vert.x)
		self.minX = round(rVerts[0].x, 5)
		self.maxX = round(rVerts[3].x, 5)

		if (self.minX != self.maxX):
			line1 = Vector(rVerts[1].x - rVerts[0].x, rVerts[1].y - rVerts[0].y, rVerts[1].z - rVerts[0].z)

		rVerts = sorted(rVerts, key=lambda vert: vert.y)
		self.minY = round(rVerts[0].y, 5)
		self.maxY = round(rVerts[3].y, 5)

		if (self.minY != self.maxY):
			if (line1):
				line2 = Vector(rVerts[1].x - rVerts[0].x, rVerts[1].y - rVerts[0].y, rVerts[1].z - rVerts[0].z)
			else:
				line1 = Vector(rVerts[1].x - rVerts[0].x, rVerts[1].y - rVerts[0].y, rVerts[1].z - rVerts[0].z)

		rVerts = sorted(rVerts, key=lambda vert: vert.z)
		self.minZ = round(rVerts[0].z, 5)
		self.maxZ = round(rVerts[3].z, 5)

		if (self.minZ != self.maxZ):
			if (line1 == None):
				line1 = Vector(rVerts[1].x - rVerts[0].x, rVerts[1].y - rVerts[0].y, rVerts[1].z - rVerts[0].z)
			elif(line2 == None):
				line2 = Vector(rVerts[1].x - rVerts[0].x, rVerts[1].y - rVerts[0].y, rVerts[1].z - rVerts[0].z)

		normalTmp = line2.cross(line1)
		self.n = Vector(normalTmp[0], normalTmp[1], normalTmp[2]).normal()
		self.p = rVerts[0]


	def intersection(self, l):
		d = l.d.dot(self.n)
		if d == 0:
			return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
		else:
			d = (self.p - l.o).dot(self.n) / d
			point = l.o+l.d*d
			global enableOutput

			if (round(point.x, 5) >= self.minX and round(point.x, 5) <= self.maxX and round(point.y, 5) >= self.minY and round(point.y, 5) <= self.maxY and round(point.z, 5) >= self.minZ and round(point.z, 5) <= self.maxZ) :
				if (enableOutput):
					print("INTERSECTION AT: "  + str(point.x) + ", " + str(point.y) + ", " + str(point.z))
				return Intersection(l.o+l.d*d, d, self.n, self)
			else :
				if (enableOutput):
					if (point.x < self.minX or point.x > self.maxX):
						print("MISS DUE TO X: "  + str(point.x) + ", " + str(point.y) + ", " + str(point.z) + "   minX: " + str(self.minX) + "   maxX: " + str(self.maxX))
					elif (point.y < self.minY or point.y > self.maxY):
						print("MISS DUE TO Y: "  + str(point.x) + ", " + str(point.y) + ", " + str(point.z) + "   minY: " + str(self.minY) + "   maxY: " + str(self.maxY))
					elif (point.z < self.minZ or point.z > self.maxZ):
						print("MISS DUE TO Z: "  + str(point.x) + ", " + str(point.y) + ", " + str(point.z) + "   minZ: " + str(self.minZ) + "   maxZ: " + str(self.maxZ))

				return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)

class Sphere(object):

	def __init__(self, center, radius, color):
		self.c = center
		self.r = radius
		self.col = color

	def intersection(self, l):
		p0c = l.o - self.c

		a = l.d.dot(l.d)
		b = (l.d * 2).dot(l.o - self.c)
		c = p0c.dot(p0c) - self.r**2

		try:
			t1 = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
		except ValueError:
			t1 = None
		try:
			t2 = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
		except ValueError:
			t2 = None
		if t1 is None and t2 is None:
			return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
		elif t1 is not None and t2 is not None:
			if (t1 <= 0):
				return Intersection( Vector(0,0,0), -1, Vector(0,0,0), self)
			elif (t2 <= 0):
				t = t1;
			else:
				t = t2;
		return Intersection( (l.o + l.d * t), math.sqrt( (l.d.x * t)**2 + (l.d.y * t)**2 + (l.d.z * t)**2), self.normal(l.o + l.d*t), self )


	def normal(self, b):
		return (b - self.c).normal()


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

class Triangle(object):
	def __init__(self, v0, v1, v2, color):
		self.v0 = v0
		self.v1 = v1
		self.v2 = v2
		self.col = color

	def normal(self):
		v0v1 = self.v1 - self.v0
		v0v2 = self.v2 - self.v0
		cross = v0v1.cross(v0v2)
		return Vector(cross[0], cross[1], cross[2]).normal()

	def intersection(self, l):
		""" http://www.scratchapixel.com/lessons/3d-basic-lessons/lesson-9-ray-triangle-intersection/
		ray-triangle-intersection-geometric-solution/ """
		origin = l.o
		v = l.d
		d = self.normal().dot(self.v0)
		if -0.00001 < self.normal().dot(v) < 0.00001:
			return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
			# return None

		t = -(self.normal().dot(origin) + d) / self.normal().dot(v)
		# if t < 0:
		#     return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
		p = origin + (v * t)

		edge0 = self.v1 - self.v0
		vp0 = p - self.v0
		c = edge0.cross(vp0)
		c = Vector(c[0], c[1], c[2])
		if self.normal().dot(c) < 0.00001:
			return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
			# return None

		edge1 = self.v2 - self.v1
		vp1 = p - self.v1
		c = edge1.cross(vp1)
		c = Vector(c[0], c[1], c[2])
		if self.normal().dot(c) < 0.00001:
			return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
			# return None

		edge2 = self.v0 - self.v2
		vp2 = p - self.v2
		c = edge2.cross(vp2)
		c = Vector(c[0], c[1], c[2])
		if self.normal().dot(c) < 0.00001:
			return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
			# return None

		# Intersection(point, distance, normal, obj)
		return Intersection(p, p.magnitude(), self.normal(), self)


class Tetrahedron(object):
	def __init__(self, vertices, triangles):
		self.vertices = vertices
		self.triangles = triangles


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

class CacheObject(object):
	def __init__(self, hash, color):
		self.hash = hash
		self.color = color

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


def trace(ray, objects, hash):
	global suns
	global bulbs
	global cameraPos
	global cacheHits
	global cacheMisses
	global cache
	global oldHash
	global lastCacheReset
	global cacheMissesDueToHash
	global totalThreadTime
	global numThreadsCompleted

	tempo = time.time()
	intersect = testRay(ray, objects)

	if intersect.d == -1 or intersect.p.z < -100:
		return Vector(-1,-1,-1)
	else:
		eyeDir = Vector( cameraPos.x - intersect.p.x, cameraPos.y - intersect.p.y, cameraPos.z - intersect.p.z)

		if (numThreadsCompleted > 0):
			averageThreadTime = totalThreadTime / numThreadsCompleted;
		else:
			averageThreadTime = 1;

		rounding = 0

		if (averageThreadTime > 8):
			rounding = 0
		elif (averageThreadTime > 5):
			rounding = 1
		elif (averageThreadTime > 3):
			rounding = 2
		elif (averageThreadTime > 1):
			rounding = 3
		else :
			rounding = 5

		if intersect.n.dot(eyeDir) < 0 :
			intersect.n = intersect.n * -1

		cacheString = str(round(intersect.p.x, rounding)) + ", " + str(round(intersect.p.y, rounding)) + ", " + str(round(intersect.p.z, rounding)) + ", " + str(round(intersect.n.x, rounding)) + ", " + str(round(intersect.n.y, rounding)) + ", " + str(round(intersect.n.z, rounding))
		col = Vector( 0, 0, 0 )

		try:
			cacheObj = cache[cacheString];

			if (cacheObj.hash == oldHash and oldHash == hash):
				col = cacheObj.color;
				cacheHits += 1;
			else:
				col = recalculateColor(intersect);
				cacheMissesDueToHash += 1;
		except: # not in cache
			col = recalculateColor(intersect)

			if (time.time() - lastCacheReset > 2):
				cache[cacheString] = CacheObject(oldHash, col);

			cacheMisses += 1;

	if time.time() - tempo > 0.013:
		pass#print "a"
	return col

def recalculateColor(intersect):
	global enableOutput

	col = Vector( 0, 0, 0 )
	for b in bulbs:
		lightDir = Vector( b[0] - intersect.p.x, b[1] - intersect.p.y, b[2] - intersect.p.z).normal()
		ray = Ray( intersect.p, lightDir )
		inter = testRay( ray, objs, intersect.obj)
		dist = math.sqrt( (intersect.p.x - b[0])**2 + (intersect.p.y - b[1])**2 + (intersect.p.z - b[2])**2 )
		if inter.d == -1 or inter.d > dist:
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
global width
global height
global fileLock
global screen
global errorLock
global running
global verts
global cache
global cacheHits
global cacheMisses
global totalThreadTime
global numThreadsCompleted
global oldHash
global lastCacheReset
global cacheMissesDueToHash
global enableOutput

running = True

pygame.init()
pygame.display.set_caption("Real-time Ray Tracer")
fileLock = threading.Lock()
errorLock = threading.Lock()
sensitivity = 0.05
width = 1
height = 1
imgLock = threading.Lock()
pixBuff = []
objs = []
suns = []
bulbs = []
verts = []
cache = dict();
cacheMisses = 0;
cacheHits = 0;
cacheMissesDueToHash = 0
totalThreadTime = 0;
numThreadsCompleted = 0;
oldHash = "";
lastCacheReset = 0;
enableOutput = False
cameraPos = Vector(0,0,0)

print "Now reading ", sys.argv[1], "..."
objFile = ObjFile()
objFile.fileName = sys.argv[1]
objFile.start()
print "Done reading file."

# Basically waiting on objFile to do its thing.
fileLock.acquire()
fileLock.release()

screen = pygame.display.set_mode((width, height))

forward = Vector( 0.0, 0.0, -1.0 )
up = Vector( 0.0, 1.0, 0.0 )
right = Vector( 1.0, 0.0, 0.0 )

print "Now starting threads... (This may take awhile)"
# Thread factory
running = True
running = True

numThreads = 81;
numThreadsXorY = int(math.floor(math.sqrt(numThreads)))
for x in range(numThreadsXorY):
	for y in range(numThreadsXorY):
		px = Pixel()
		px.x = int(float(x)*float(width)/numThreadsXorY)
		px.x_bound = px.x + width/numThreadsXorY + 1
		px.y = int(float(y)*float(height)/numThreadsXorY)
		px.y_bound = px.y + height/numThreadsXorY + 1
		#print x, y, "\t|\t", px.x, px.y, "\t\t|\t", px.x_bound, px.y_bound
		px.start()
	print float(x*numThreadsXorY + y + 1)/((numThreads)/100.0), "% done"
"""
for x in range(40):
	for y in range(20):
		px = Pixel()
		px.x = int(float(x)*float(width)/40.0)
		px.x_bound = px.x + width/40 + 1
		px.y = int(float(y)*float(height)/20.0)
		px.y_bound = px.y + height/20 + 1
		#print x, y, "\t|\t", px.x, px.y, "\t\t|\t", px.x_bound, px.y_bound
		px.start()
	print float(x*20 + y + 1)/((40.0*20.0)/100.0), "% done"
	"""

print "Done starting threads."

while True:
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running = False
			while threading.activeCount() > 1:
				pass
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			#print("CACHE HITS: " + str(cacheHits)  + "    CACHE MISSES: " + str(cacheMisses) + "   CACHE MISSED DUE TO HASH: " + str(cacheMissesDueToHash))
			#print("CACHE SIZE: " + str(len(cache)))
			#print("AVG THREAD TIME: " + str(totalThreadTime / numThreadsCompleted))

			print("CAMERA POS: " + str(cameraPos.x) + ", " + str(cameraPos.y) + ", " + str(cameraPos.z))
			print("FORWARD: " + str(forward.x) + ", " + str(forward.y) + ", " + str(forward.z) + "\n")
			if event.key == pygame.K_w:
				dX = forward.x * sensitivity;
				dY = forward.y * sensitivity;
				dZ = forward.z * sensitivity;
				cameraPos = Vector(cameraPos.x + dX, cameraPos.y + dY, cameraPos.z + dZ)
			elif event.key == pygame.K_s:
				dX = forward.x * -sensitivity;
				dY = forward.y * -sensitivity;
				dZ = forward.z * -sensitivity;
				cameraPos = Vector(cameraPos.x + dX, cameraPos.y + dY, cameraPos.z + dZ)
			elif event.key == pygame.K_a:
				dX = right.x * -sensitivity;
				dY = right.y * -sensitivity;
				dZ = right.z * -sensitivity;
				cameraPos = Vector(cameraPos.x + dX, cameraPos.y + dY, cameraPos.z + dZ)
			elif event.key == pygame.K_d:
				dX = right.x * sensitivity;
				dY = right.y * sensitivity;
				dZ = right.z * sensitivity;
				cameraPos = Vector(cameraPos.x + dX, cameraPos.y + dY, cameraPos.z + dZ)
			elif event.key == pygame.K_LCTRL:
				dX = up.x * -sensitivity;
				dY = up.y * -sensitivity;
				dZ = up.z * -sensitivity;

				cameraPos = Vector(cameraPos.x + dX, cameraPos.y + dY, cameraPos.z + dZ)
			elif event.key == pygame.K_SPACE:
				dX = up.x * sensitivity;
				dY = up.y * sensitivity;
				dZ = up.z * sensitivity;

				cameraPos = Vector(cameraPos.x + dX, cameraPos.y + dY, cameraPos.z + dZ)
			elif event.key == pygame.K_UP:
				dY = sensitivity;
				dZ = sensitivity;

				if (forward.z >= 0):
					dY = -dY;
				
				if (forward.y <= 0):
					dZ = - dZ;
				
				forward = Vector(forward.x, dY + forward.y, dZ + forward.z);
				cross = forward.cross(up)
				right = Vector(cross[0], cross[1], cross[2]).normal();
				cross = right.cross(forward);
				up = Vector(cross[0], cross[1], cross[2]).normal();
			elif event.key == pygame.K_DOWN:
				dY = sensitivity;
				dZ = sensitivity;

				if (forward.z <= 0):
					dY = -dY;
				
				if (forward.y >= 0):
					dZ = - dZ;
				
				forward = Vector(forward.x, dY + forward.y, dZ + forward.z);
				cross = forward.cross(up)
				right = Vector(cross[0], cross[1], cross[2]).normal();
				cross = right.cross(forward);
				up = Vector(cross[0], cross[1], cross[2]).normal();
			elif event.key == pygame.K_RIGHT:
				dX = sensitivity;
				dZ = sensitivity;

				if (forward.z >= 0):
					dX = -dX;
				
				if (forward.x <= 0):
					dZ = - dZ;
				
				forward = Vector(dX + forward.x, forward.y, dZ + forward.z);
				cross = forward.cross(up)
				right = Vector(cross[0], cross[1], cross[2]).normal();
				cross = right.cross(forward);
				up = Vector(cross[0], cross[1], cross[2]).normal();
			elif event.key == pygame.K_LEFT:
				dX = sensitivity;
				dZ = sensitivity;

				if (forward.z <= 0):
					dX = -dX;
				
				if (forward.x >= 0):
					dZ = - dZ;
				
				forward = Vector(dX + forward.x, forward.y, dZ + forward.z);
				cross = forward.cross(up)
				right = Vector(cross[0], cross[1], cross[2]).normal();
				cross = right.cross(forward);
				up = Vector(cross[0], cross[1], cross[2]).normal();
			elif event.key == pygame.K_r:
				forward = Vector( 0.0, 0.0, -1.0 )
				up = Vector( 0.0, 1.0, 0.0 )
				right = Vector( 1.0, 0.0, 0.0 )

				cameraPos = Vector(0, 0 , 0)
			elif event.key == pygame.K_e:
				forward = Vector( 0.0, 0.0, -1.0 )
				up = Vector( 0.0, 1.0, 0.0 )
				right = Vector( 1.0, 0.0, 0.0 )
			elif event.key == pygame.K_p:
				enableOutput = not enableOutput
				print("ENABLE OUTPUT = " + str(enableOutput))
			elif event.key == pygame.K_ESCAPE:
				running = False
				while threading.activeCount() > 1:
					pass
				pygame.quit()
				sys.exit()
			#clock.tick(5) # lock framerate to 10 fps.
