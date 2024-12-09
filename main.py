import shutil
from time import sleep

import keyboard
from cv2 import cvtColor, COLOR_BGR2RGB, COLOR_BGR2GRAY

from node_classification import classifyNodes
from line_classification import classifyLines
from priority_functions import template_matching
from screen_functions import grabImage, showScreen, showNodes, showLines, showTrees
from win32gui import GetWindowRect, GetDesktopWindow
from build_trees import buildTrees
from tree_interaction import move_and_click, move_and_click_list

hwnd = GetDesktopWindow()
rect = GetWindowRect(hwnd)
char = 'Chucky'
counter = 0

shutil.rmtree('data')

while True:
    screen = grabImage(830, 830, 265, 140, rect[0])
    screen = cvtColor(screen, COLOR_BGR2RGB)
    screen_gray = cvtColor(screen, COLOR_BGR2GRAY)

    matches = template_matching(screen, char)
    move_and_click_list(matches)

    image = grabImage(rect[2], rect[3], 0, 0, hwnd)
    nodes = classifyNodes(image)
    lines = classifyLines(image)
    trees = buildTrees(nodes, lines, image)

    showNodes(image, nodes, counter)
    showLines(image, lines, counter)
    showTrees(image, trees, counter)

    try:
        move_and_click((trees[0].root.node[0], trees[0].root.node[1]))
    except IndexError:
        sleep(2)
