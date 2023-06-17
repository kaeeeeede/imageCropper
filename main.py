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
    images = []

    for file in os.listdir(path):
        images.append(f"{path}/{file}")

    return images

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

dragging = False
start_point = end_point = prior_rect = None

def load_image_on_graph(graph, image_path):
	im = Image.open(image_path)
	w,h = im.size

	graph.change_coordinates((0, w), (h, 0))

	graph.draw_image(image_path, location=(0,0))
	graph.set_size(im.size)

load_image_on_graph(graph, "test.png")

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break    

    if event == "-GRAPH-":
        x, y = values["-GRAPH-"]

        if not dragging:
            start_point = (x, y)
            dragging = True
        else:
            end_point = (x, y)

        if prior_rect:
            graph.delete_figure(prior_rect)
            
        if None not in (start_point, end_point):
            prior_rect = graph.draw_rectangle(start_point, end_point, line_color='red')

    elif event == "-GRAPH-+UP":
        dragging = False