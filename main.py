import os
import shutil
import threading
from time import sleep

from cv2 import cvtColor, COLOR_BGR2RGB, COLOR_BGR2GRAY

from node_classification import classifyNodes
from line_classification import classifyLines
from priority_functions import template_matching
from screen_functions import grabImage, showScreen, showNodes, showLines, showTrees
from win32gui import GetWindowRect, GetDesktopWindow
from build_trees import buildTrees
from tree_interaction import move_and_click, move_and_click_list, monitor_delete_key

hwnd = GetDesktopWindow()
rect = GetWindowRect(hwnd)
char = 'Nurse'
counter = 0
web_center = (683, 562)
save = True

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

    matches = template_matching(screen, char)
    move_and_click_list(matches)

    image = grabImage(rect[2], rect[3], 0, 0, hwnd)
    nodes = classifyNodes(image)
    lines = classifyLines(image)
    trees = buildTrees(nodes, lines, web_center, levels)

    showNodes(image, nodes, counter, save)
    showLines(image, lines, counter, save)
    showTrees(image, trees, counter, save)
    counter += 1

    try:
        move_and_click((trees[0].root.node[0], trees[0].root.node[1]))
    except IndexError:
        sleep(3.8)
