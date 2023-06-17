from PIL import Image

def crop_image(image, x_offset, y_offset, width, height):
	crop_box = (x_offset, y_offset, width + x_offset, height + y_offset)
	
	result = image.crop(crop_box)

	return result

if __name__ == "__main__":
	image = Image.open(r"test.jpg")

	cropped_image = crop_image(image, 123, 165, 1230, 1860)

	cropped_image.show()
