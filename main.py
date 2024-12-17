import os
import shutil
import threading
from time import sleep

from cv2 import cvtColor, COLOR_BGR2RGB, COLOR_BGR2GRAY, imread

from graph_builder import buildGraph
from node_classification import classifyNodes
from edge_classification import classifyEdges
from priority_functions import template_matching
from screen_functions import grabImage, showScreen, showNodes, showEdges, showGraphs
from win32gui import GetWindowRect, GetDesktopWindow
from tree_interaction import move_and_click, move_and_click_list, monitor_delete_key

hwnd = GetDesktopWindow()
rect = GetWindowRect(hwnd)
char = 'Nurse'
counter = 0
save = False

with open('stored/Levels', 'r') as f:
    line = f.readline().strip()
    levels = [float(x) for x in line.split(',')]

if os.path.exists('data'):
    shutil.rmtree('data')

exit_event = threading.Event()
key_thread = threading.Thread(target=monitor_delete_key, args=(exit_event,))
key_thread.daemon = True
key_thread.start()

while not exit_event.is_set():
    screen = grabImage(830, 830, 265, 140, rect[0])
    screen = cvtColor(screen, COLOR_BGR2RGB)
    screen_gray = cvtColor(screen, COLOR_BGR2GRAY)

    '''matches = template_matching(screen, char)
    move_and_click_list(matches)'''

    #image = grabImage(rect[2], rect[3], 0, 0, hwnd)
    image = imread('stored/screen.png')
    nodes = classifyNodes(image)
    edges = classifyEdges(image, nodes)

    graph = buildGraph(nodes, edges, image)
    #showNodes(image, graph, save)
    showGraphs(image, graph, edges, save)

    #showNodes(image, nodes, save, counter)
    #showEdges(image, edges, save, counter)
    counter += 1

    break
