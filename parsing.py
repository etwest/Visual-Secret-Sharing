"""
Made by Eugene Chou and Timothy Lo
Supervised and finished by Evan West

Part of the CS Makerspace VSS Project.
"""

import sys
import argparse
import numpy as np
import os
import io
from imageio import imwrite
from array import array
from PIL import Image
import kofk

def image_to_bits(image):
	print 	"Image info:"
	print 	"""Number of bits: %d,  Image Size: %s,  Image format: %s""" %(image.bits, image.size, image.format)
	# image.show()
	image = image.convert("L")
	toBW(image)
	return np.array(image.convert("1").getdata())

#converts grayscale pixels to pure black and white
#This is unfortunately necessary (it seems) because image.convert("1") is bugged
def toBW(image):
	depth, width = image.size
	pixels = image.load()
	for row in range(depth):
		for pixel in range(width):
			if pixels[row, pixel] >= 127:
				pixels[row, pixel] = 255
			else:
				pixels[row, pixel] = 0

def print_image(image):
	image.show()


def print_bit_array(image, data):
	count = 0
	for bit in data:
		count += 1

		if count % image.size[1] == 0:
			print bit/255

		else:
			print bit/255,


def flip_bits(bits):
# Flips bits for KofK peoples (1 is black and 0 is white)
	for x in range(len(bits)):
		if bits[x] == 255:
			bits[x] = 0
		else:
			bits[x] = 255


def paste_images(background, foreground):
	# Pastes foreground image on background
	return Image.alpha_composite(background, foreground).save("stacked-img.png")

def from_2D_to_img(Matrix):
	for row in range(len(Matrix)):
		for pixel in range(len(Matrix[row])):
			if Matrix[row][pixel] == 1: #used to be that 0 was black and 1 was white
				Matrix[row][pixel] = 255
			# elif Matrix[row][pixel] == 1:
			# 	Matrix[row][pixel] = 0

def make_2D_array(data,ratio):
	print ratio[0],ratio[1]
	Matrix = np.zeros((ratio[1], ratio[0]), dtype=np.uint8)
	x,y = 0,0
	for datum in data:
		Matrix[y][x] = datum + 1 #This is so 0 maps to 0 and 255 maps to 1
		x = (x+1) % ratio[0]
		if x == 0:
			y = (y+1) % ratio[1]
	return Matrix

if __name__ == '__main__':
	# import pdb; pdb.set_trace()
	parser = argparse.ArgumentParser(description = 'Runs VSS-encryption')
	parser.add_argument('-s', help = 'split', action = 'store_true', default = False)
	parser.add_argument('-r', help = 'reconstruct', action = 'store_true', default = False)
	parser.add_argument('image', help = 'input files', nargs = '+')
	parser.add_argument('-o', dest='outImage', help = 'output files (if not specified, stdout)', nargs = '+')
	# parser.add_argument('-p', help = 'Print out the bit array', action = 'store_true', default = False)
	args = parser.parse_args()
	k = 3
	inp = Image.open(args.image[0])										# Open image
	out = image_to_bits(inp)										# Convert to bits
	flip_bits(out)
	Matrix = make_2D_array(out,inp.size)
	shares = kofk.koutofk_to3D_Matrix(k,Matrix)
	for i in range(k):
		from_2D_to_img(shares[i])
		imwrite("share"+str(i)+".png", shares[i])
	outMatrix = kofk.toImage_fr3D(k, shares)
	from_2D_to_img(outMatrix)
	imwrite('result.png', outMatrix)
	from_2D_to_img(Matrix)
	imwrite('beforeShare.png', Matrix)

	# Stacked2 = [shares[0], shares[1]]
	outMatrix = kofk.stack_images(shares)
	from_2D_to_img(outMatrix)
	imwrite('stacked.png', outMatrix)

	# outMatrix = kofk.stack_images(Stacked2)
	# from_2D_to_img(outMatrix)
	# imwrite('stacked2.png', outMatrix)

	# if args.s:
	# 	inp = Image.open(args.i[0])										# Open image
	# 	out = image_to_bits(inp)										# Convert to bits
	# 	flip_bits(out)
	# 	Matrix = make_2D_array(out,inp.size)


	# 	#kofk stuff goes here
	# if args.r:
	# 	for
	# 	flip_bits(out)
	# 	Matrix = make_2D_array(out,inp.size)
	# 	from_2D_to_img(Matrix)
	# 	imwrite('lawrence1.png', Matrix)
		# if args.p:														# Print the bit array
		# 	print_bit_array(inp, out)
		# data = numpy.array(out).reshape(inp.size[0], inp.size[1])		# Convert bits to image
		# if args.o:
		# 	imwrite(args.o[0], data)							# Save the file
		# else:
		# 	imwrite("output.jpg", data)						# Print file to stdout
		# 	inp = Image.open("output.jpg")
		# 	print_image(inp)


	# if args.i and args.o:
	# 	inp = Image.open(args.i[0])
	# 	out = Image.open(args.o[0])

	# 	stackImages(inp, out)




