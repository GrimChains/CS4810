import Image
import sys

# File reading
fread = open(sys.argv[1], 'r')

# Set up png file
line = fread.readline()
info = line.split()
fileType = info[0]
fileName = info[3]
img = Image.new("RGBA", (int(info[1]), int(info[2])), (0, 0, 0, 0))
putpixel = img.im.putpixel
line = fread.readline()
while (line != "") :
	parse = line.split()
	if parse[0]=="xy" :
		putpixel((int(parse[1]), int(parse[2])), (255, 255, 255, 255))
	elif parse[0]=="xyrgb" :
		putpixel((int(parse[1]), int(parse[2])), (int(parse[3]), int(parse[4]), int(parse[5]), 255))
	elif parse[0]=="xyc" :
		hexNum = parse[3]
		red = hexNum[1] + hexNum[2]
		blue = hexNum[5] + hexNum[6]
		green = hexNum[3] + hexNum[4]
		putpixel((int(parse[1]), int(parse[2])), (int(red, 16), int(green, 16), int(blue, 16), 255))
	line = fread.readline()
img.save(fileName)
