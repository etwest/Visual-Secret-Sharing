from PIL import Image
import argparse


parser = argparse.ArgumentParser(description = 'Converts white pixels in black')
parser.add_argument('images', help = 'input images', nargs = '+')
args = parser.parse_args()

for bw_image in args.images:
	img = Image.open(bw_image)
	img = img.convert("RGBA")
	data_arr  = img.getdata()

	ndata_arr = []
	for pixel in data_arr:
		if pixel[0] > 0 and pixel[1] > 0 and pixel[2] > 0:
			ndata_arr.append((255,255,255,0))
		else:
			ndata_arr.append((0,0,0,255))

	img.putdata(ndata_arr)
	img.save("clear_" + bw_image, "PNG")