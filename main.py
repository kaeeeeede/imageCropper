import PySimpleGUI as sg
import os
from PIL import Image

def crop_image(image, x_offset, y_offset, width, height):
	crop_box = (x_offset, y_offset, width + x_offset, height + y_offset)
	
	result = image.crop(crop_box)

	return result

def resize_image(image, width, height):
    new_size = (width, height)

    result = image.resize(new_size)

    return result

def save_image(image, filename, save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    image.save(f"{save_path}/cropped_{filename}.png")

    return

def read_images(path):
    for file in os.listdir(path):
        yield f"{path}/{file}"

image_path = r'test.png'

layout = [[sg.Graph(
    canvas_size=(400, 400),
    graph_bottom_left=(0, 400),
    graph_top_right=(400, 0),
    key="-GRAPH-",
    enable_events=True,  # mouse click events
    drag_submits=True), ],
    [sg.Text(key='info', size=(60, 1))]]

window = sg.Window("Cropper", layout, finalize=True)
graph = window["-GRAPH-"]

def load_image_on_graph(graph, image_path):
	im = Image.open(image_path)
	w,h = im.size

	graph.change_coordinates((0, h), (w, 0))

	graph.draw_image(image_path, location=(0,0))
	graph.set_size(im.size)

def init_crop_rect(graph, width, height):
	return graph.draw_rectangle((0, 0), (width, height), line_color='red')

def is_point_in_rect(point, rect_corner_1, rect_corner_2):
	x, y = point
	rect_top_left = (min(rect_corner_1[0], rect_corner_2[0]), min(rect_corner_1[1], rect_corner_2[1]))
	rect_bottom_right = (max(rect_corner_1[0], rect_corner_2[0]), max(rect_corner_1[1], rect_corner_2[1]))

	if (rect_top_left[0] < x and x < rect_bottom_right[0]):
		if (rect_top_left[1] < y and y < rect_bottom_right[1]):
			return True
	return False

load_image_on_graph(graph, "test.png")
prior_rect = init_crop_rect(graph, 500, 500)
rect_top_left = (0, 0)
rect_bottom_right = (500, 500)

dragging = False
moving = False
resizing = False
last_coord = None
start_point = end_point = None

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break    

    if event == "-GRAPH-":
        coord = values["-GRAPH-"]

        if moving:
        	if last_coord == None:
        		continue
        	move_vector = tuple(map(lambda i, j: i - j, coord, last_coord))

        	rect_top_left = tuple(map(lambda i, j: i + j, rect_top_left, move_vector))
        	rect_bottom_right = tuple(map(lambda i, j: i + j, rect_bottom_right, move_vector))
        if resizing:
        	if last_coord == None:
        		continue
        	resize_vector = tuple(map(lambda i, j: i - j, coord, last_coord))

        	rect_centre = ((rect_top_left[0] + rect_bottom_right[0])/2, (rect_top_left[1] + rect_bottom_right[1])/2)

        	if coord[0] < rect_centre[0]: # left
        		rect_top_left = (rect_top_left[0] + resize_vector[0], rect_top_left[1])
        	else:
        		rect_bottom_right = (rect_bottom_right[0] + resize_vector[0], rect_bottom_right[1])

        	if coord[1] < rect_centre[1]: # top	
        		rect_top_left = (rect_top_left[0], rect_top_left[1] + resize_vector[1])
        	else:
        		rect_bottom_right = (rect_bottom_right[0], rect_bottom_right[1] + resize_vector[1])

        elif is_point_in_rect(coord, rect_top_left, rect_bottom_right):
        	moving = True
        else:
        	resizing = True

        last_coord = coord
        if prior_rect:
        	graph.delete_figure(prior_rect)

        prior_rect = graph.draw_rectangle(rect_top_left, rect_bottom_right, line_color='red')

    elif event == "-GRAPH-+UP":
        moving = False
        resizing = False
        