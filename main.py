from PIL import Image

def crop_image(image, x_offset, y_offset, width, height):
	crop_box = (x_offset, y_offset, width + x_offset, height + y_offset)
	
	result = image.crop(crop_box)

	result.show()

	return

if __name__ == "__main__":
	im = Image.open(r"test.jpg")

	crop_image(im, 123, 165, 1230, 1860)
