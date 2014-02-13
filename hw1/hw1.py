import Image
import sys
import math

# File reading
fread = open(sys.argv[1], 'r')

# Mildly important variables
vertexList = []

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
		blue = hexNum[5] + hexNum[6]
		green = hexNum[3] + hexNum[4]
		vertexList.append([float(parse[1]), float(parse[2]), int(red, 16), int(blue, 16), int(green, 16), 255])
	elif parse[0] == "xyrgba" :
		vertexList.append([float(parse[1]), float(parse[2]), int(parse[3]), int(parse[4]), int(parse[5]), int(parse[6])])
	elif parse[0] == "linec" :
		if int(parse[1]) < 0 :
			list1 = vertexList[len(vertexList) + int(parse[1])]
		else :
			list1 = vertexList[int(parse[1]) - 1]
		if int(parse[2]) < 0 :
			list2 = vertexList[len(vertexList) + int(parse[2])]
		else :
			list2 = vertexList[int(parse[2]) - 1]
		x1 = list1[0]
		y1 = list1[1]
		x2 = list2[0]
		y2 = list2[1]
		length = math.sqrt(pow((x1-x2), 2) + pow((y1-y2), 2))
		
		# This is the DDA algorithm with the forced progression. It's janky as fuck, but I'll come back to it later.
		#if abs(x1-x2) > abs(y1-y2) :
		#	dx = 1
		#	dy = abs(y1-y2)/length
		#elif abs(x1-x2) <= abs(y1-y2) :
		#	dx = abs(x1-x2)/length
		#	dy = 1

		dx = abs(x1-x2)/length
		dy = abs(y1-y2)/length
		if x1 > x2 :
			dx *= -1
		if y1 > y2 :
			dy *= -1
		flag = True
		xiter = x1 + dx
		yiter = y1 + dy
		hexNum = parse[3]
		red = hexNum[1] + hexNum[2]
		green = hexNum[3] + hexNum[4]
		blue = hexNum[5] + hexNum[6]
		while flag :
			putpixel((math.ceil(xiter), math.ceil(yiter)), (int(red, 16), int(green, 16), int(blue, 16), 255))
			yiter = yiter + dy
			xiter = xiter + dx
			flag = not((x1 > x2 and x2 > xiter) or (x1 < x2 and x2 < xiter) or (y1 > y2 and y2 > yiter) or (y1 < y2 and y2 < yiter)) # Basically checking to see if we've over-stepped the endpoints of the line.
		img.save(fileName)
	line = fread.readline()
img.save(fileName)
