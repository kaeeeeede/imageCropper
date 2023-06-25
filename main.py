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

def save_image(image, file_name, read_path):
    if not os.path.exists(f"cropped_{read_path}"):
        os.mkdir(f"cropped_{read_path}")

    image.save(f"cropped_{read_path}/cropped_{file_name}.png")

    return

def read_images(read_path):
    for file in os.listdir(read_path):
        yield f"{read_path}/{file}"

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

image_path = r'test.png'

layout = [[sg.Button("Next")] 
        , [sg.Graph(canvas_size=(400, 400),
                graph_bottom_left=(0, 400),
                graph_top_right=(400, 0),
                key="-GRAPH-",
                enable_events=True,  # mouse click events
                drag_submits=True), ]]

window = sg.Window("Cropper", layout, finalize=True)
graph = window["-GRAPH-"]

target_aspect_ratio = (250,500)

load_image_on_graph(graph, "test.png")
prior_rect = init_crop_rect(graph, 250, 500)
rect_top_left = (0, 0)
rect_bottom_right = (250, 500)

dragging = False
moving = False
resizing = False
last_coord = None

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

        	rect_width = rect_bottom_right[0] - rect_top_left[0]
        	rect_height = rect_bottom_right[1] - rect_top_left[1]

        	graph_width, graph_height = graph.get_size()

        	rect_top_left = (min(max(rect_top_left[0] + move_vector[0], 0), graph_width - rect_width), min(max(rect_top_left[1] + move_vector[1], 0), graph_height - rect_height))

        	rect_bottom_right = (max(min(rect_bottom_right[0] + move_vector[0], graph_width), rect_width), max(min(rect_bottom_right[1] + move_vector[1], graph_height), rect_height))

        elif resizing:
        	if last_coord == None:
        		continue
        	resize_vector = tuple(map(lambda i, j: i - j, coord, last_coord))

        	rect_centre = ((rect_top_left[0] + rect_bottom_right[0])/2, (rect_top_left[1] + rect_bottom_right[1])/2)

        	adjusted_left = False
        	adjusted_top = False

        	if coord[0] < rect_centre[0]: # left
        		rect_top_left = (rect_top_left[0] + resize_vector[0], rect_top_left[1])
        		adjusted_left = True
        	else:
        		rect_bottom_right = (rect_bottom_right[0] + resize_vector[0], rect_bottom_right[1])
        		adjusted_left = False

        	if coord[1] < rect_centre[1]: # top	
        		rect_top_left = (rect_top_left[0], rect_top_left[1] + resize_vector[1])
        		adjusted_top = True
        	else:
        		rect_bottom_right = (rect_bottom_right[0], rect_bottom_right[1] + resize_vector[1])
        		adjusted_top = False

        	rect_width = rect_bottom_right[0] - rect_top_left[0]
        	rect_height = rect_bottom_right[1] - rect_top_left[1]

        	target_height_following_width = rect_width / target_aspect_ratio[0] * target_aspect_ratio[1] 
        	target_width_following_height = rect_height / target_aspect_ratio[1] * target_aspect_ratio[0]
        	
        	if target_height_following_width > rect_height:
        		if adjusted_top:
        			rect_top_left = (rect_top_left[0], rect_bottom_right[1] - target_height_following_width)
        		else:
        			rect_bottom_right = (rect_bottom_right[0], rect_top_left[1] + target_height_following_width)
        	elif target_width_following_height > rect_width:
        		if adjusted_left:
        			rect_top_left = (rect_bottom_right[0] - target_width_following_height, rect_top_left[1])
        		else:
        			rect_bottom_right = (rect_top_left[0] + target_width_following_height, rect_bottom_right[1])

        	if adjusted_left:
        		rect_top_left = (max(rect_top_left[0] + resize_vector[0], 0), rect_top_left[1])
        	else:
        	 	rect_bottom_right = (min(rect_bottom_right[0] + resize_vector[0], graph.get_size()[0]), rect_bottom_right[1])

        	if adjusted_top:
        		rect_top_left = (rect_top_left[0], max(rect_top_left[1] + resize_vector[1], 0))
        	else:
        		rect_bottom_right = (rect_bottom_right[0], min(rect_bottom_right[1] + resize_vector[1], graph.get_size()[1]))

        	rect_width = rect_bottom_right[0] - rect_top_left[0]
        	rect_height = rect_bottom_right[1] - rect_top_left[1]
        	target_height_following_width = rect_width / target_aspect_ratio[0] * target_aspect_ratio[1] 
        	target_width_following_height = rect_height / target_aspect_ratio[1] * target_aspect_ratio[0]

        	if target_height_following_width > rect_height:
        		if adjusted_left:
        			rect_top_left = (rect_bottom_right[0] - target_width_following_height, rect_top_left[1])
        		else:
        			rect_bottom_right = (rect_top_left[0] + target_width_following_height, rect_bottom_right[1])
        	elif target_width_following_height > rect_width:
        		if adjusted_top:
        			rect_top_left = (rect_top_left[0], rect_bottom_right[1] - target_height_following_width)
        		else:
        			rect_bottom_right = (rect_bottom_right[0], rect_top_left[1] + target_height_following_width)

        elif is_point_in_rect(coord, rect_top_left, rect_bottom_right):
        	moving = True
        else:
        	resizing = True

        last_coord = coord
        if prior_rect:
        	graph.delete_figure(prior_rect)

        prior_rect = graph.draw_rectangle(rect_top_left, rect_bottom_right, line_color='red')

    if event == "Next":
        im = Image.open(image_path)

        cropped_image = crop_image(im, 50, 50, 500, 500)
        resized_image = resize_image(cropped_image, 300, 300)
        save_image(resized_image, "test", "test")

    elif event == "-GRAPH-+UP":
        moving = False
        resizing = False
        