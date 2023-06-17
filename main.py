import PySimpleGUI as sg
from PIL import Image

def crop_image(image, x_offset, y_offset, width, height):
	crop_box = (x_offset, y_offset, width + x_offset, height + y_offset)
	
	result = image.crop(crop_box)

	return result

image_path = r'test.png'

layout = [[sg.Graph(
    canvas_size=(400, 400),
    graph_bottom_left=(0, 0),
    graph_top_right=(400, 400),
    key="-GRAPH-",
    change_submits=True,  # mouse click events
    drag_submits=True), ],
    [sg.Text(key='info', size=(60, 1))]]

window = sg.Window("Cropper", layout, finalize=True)
graph = window["-GRAPH-"]

def load_image_on_graph(graph, image_path):
	im = Image.open(image_path)
	graph.draw_image(image_path, location=(0,400))
	graph.set_size(im.size)

load_image_on_graph(graph, "test.png")

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break  # exit
