import Image
import sys
import math

# File reading
fread = open(sys.argv[1], 'r')

# Mildly important variables
vertexList = []

def drawlineh( vertex1, vertex2, hexNum1, hexNum2):
	red1 = int(hexNum1[1] + hexNum1[2], 16)
	green1 = int(hexNum1[3] + hexNum1[4], 16)
	blue1 = int(hexNum1[5] + hexNum1[6], 16)
	red2 = int(hexNum2[1] + hexNum2[2], 16)
	green2 = int(hexNum2[3] + hexNum2[4], 16)
	blue2 = int(hexNum2[5] + hexNum2[6], 16)
	drawline( vertex1, vertex2, red1, green2, blue1, red2, green2, blue2)


def drawline( vertex1, vertex2, red1, green1, blue1, red2, green2, blue2):
	pass
	# Set up location vectors
	print vertex1
	print vertex2
	print "============="
	x1 = vertex1[0]
	y1 = vertex1[1]
	x2 = vertex2[0]
	y2 = vertex2[1]
	length = math.sqrt(pow((x1-x2), 2) + pow((y1-y2), 2))
	dx = abs(x1-x2)/length
	dy = abs(y1-y2)/length
	if x1 > x2 :
		dx *= -1
	if y1 > y2 :
		dy *= -1

	# Set up color vectors
	# TODO: Set up alpha at some point
	dr = abs(red1 - red2)/length
	if red1 > red2 :
		dr *= -1
	dg = abs(green1 - green2)/length
	if green1 > green2 :
		dg *= -1
	db = abs(blue1 - blue2)/length
	if blue1 > blue2 :
		db *= -1


	# Set up iters
	xiter = x1 + dx
	yiter = y1 + dy
	riter = red1
	giter = green1
	biter = blue1

	# Draw loop
	flag = True
	while flag :
		putpixel((math.ceil(xiter), math.ceil(yiter)), (riter, giter, biter, 255))
		xiter += dx
		yiter += dy
		riter += dr
		giter += dg
		biter += db
		flag = not((x1 > x2 and x2 > xiter) or (x1 < x2 and x2 < xiter) or (y1 > y2 and y2 > yiter) or (y1 < y2 and y2 < yiter)) # Basically checking to see if we've over-stepped the endpoints of the line.


def linec( parse ) :
	if int(parse[1]) < 0 :
		list1 = vertexList[len(vertexList) + int(parse[1])]
	else :
		list1 = vertexList[int(parse[1]) - 1]
	if int(parse[2]) < 0 :
		list2 = vertexList[len(vertexList) + int(parse[2])]
	else :
		list2 = vertexList[int(parse[2]) - 1]
	drawlineh( list1, list2, parse[3], parse[3])

def lineg( parse ) :
	if int(parse[1]) < 0 :
		list1 = vertexList[len(vertexList) + int(parse[1])]
	else :
		list1 = vertexList[int(parse[1]) - 1]
	if int(parse[2]) < 0 :
		list2 = vertexList[len(vertexList) + int(parse[2])]
	else :
		list2 = vertexList[int(parse[2]) - 1]
	drawline( list1, list2, list1[2], list1[3], list1[4], list2[2], list2[3], list2[4] )

def cubicc ( parse ) :
	hexNum = parse[5]
	red = int(hexNum[1] + hexNum[2], 16)
	green = int(hexNum[3] + hexNum[4], 16)
	blue = int(hexNum[5] + hexNum[6], 16)
	points = []
	for x in range(1, 5) :
		if int(parse[x]) < 0 :
			points.append(vertexList[len(vertexList) + int(parse[x])])
		else :
			points.append(vertexList[int(parse[1]) - 1])
	bezier( points, red, 0, green, 0, blue, 0)

def beznc ( parse ) :
	hexNum = parse[len(parse) - 1]
	red = int(hexNum[1] + hexNum[2], 16)
	green = int(hexNum[3] + hexNum[4], 16)
	blue = int(hexNum[5] + hexNum[6], 16)
	points = []
	for x in range(2, len(parse) - 1)
		if int(parse[x]) < 0 :
			points.append(vertexList[len(vertexList) + int(parse[x])])
		else :
			points.append(vertexList[int(parse[1]) - 1])
	bezier( points, red, 0, green, 0, blue, 0)


def bezier ( points, red, dr, green, dg, blue, db ) :


#Set up png file
line = fread.readline()
info = line.split()
fileType = info[0]
fileName = info[3]
img = Image.new("RGBA", (int(info[1]), int(info[2])), (0,0,0,0))
putpixel = img.im.putpixel
# Read the file
while (line != "") :
	parse = line.split()
	if parse == [] :
		parse # Should probably try finding a better noop
	elif parse[0] == "xy" :
		vertexList.append([float(parse[1]), float(parse[2]), 255, 255, 255, 255])
	elif parse[0] == "xyrgb" :
		vertexList.append([float(parse[1]), float(parse[2]), int(parse[3]), int(parse[4]), int(parse[5]), 255])
	elif parse[0] == "xyc" :
		hexNum = parse[3]
		red = hexNum[1] + hexNum[2]
		green = hexNum[3] + hexNum[4]
		blue = hexNum[5] + hexNum[6]
		vertexList.append([float(parse[1]), float(parse[2]), int(red, 16), int(green, 16), int(blue, 16), 255])
	elif parse[0] == "xyrgba" :
		vertexList.append([float(parse[1]), float(parse[2]), int(parse[3]), int(parse[4]), int(parse[5]), int(parse[6])])
	elif parse[0] == "linec" :
		linec(parse)
	elif parse[0] == "lineg" :
		lineg(parse)
	elif parse[0] == "cubicc" :
		cubicc(parse)
	elif parse[0] == "beznc" :
		beznc(parse)
	line = fread.readline()
img.save(fileName)
