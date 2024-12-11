import cv2
from numpy import array, sum

from graph_builder import GraphNode
from screen_functions import showScreen

def classifyNodes(image):
    height, width = image.shape[:2]
    patch_size = 80
    half_patch = patch_size // 2

    graph_nodes = []

    with open('stored/Centers', 'r') as f:
        centers = [list(map(int, line.strip().split(','))) for line in f.readlines()]

    for (x, y, l) in centers:
        left = max(x - half_patch, 0)
        top = max(y - half_patch, 0)
        right = min(x + half_patch, width)
        bottom = min(y + half_patch, height)

        patch = image[top:bottom, left:right]
        patch = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)

        lower_red = array([170, 0, 0])
        upper_red = array([255, 50, 50])
        mask = cv2.inRange(patch, lower_red, upper_red)
        reds = sum(mask > 0)  # check above 400

        lower_black = array([0, 0, 0])
        upper_black = array([8, 8, 8])
        mask = cv2.inRange(patch, lower_black, upper_black)
        blacks = sum(mask > 0)  # check above 1000

        patch = cv2.cvtColor(patch, cv2.COLOR_RGB2HSV)

        lower_brown = array([9, 60, 35])
        upper_brown = array([14, 130, 80])
        lower_white = array([0, 0, 130])
        upper_white = array([14, 20, 255])
        mask = cv2.inRange(patch, lower_brown, upper_brown)
        browns = sum(mask > 0)  # check above 800
        mask = cv2.inRange(patch, lower_white, upper_white)
        whites = sum(mask > 0)  # check above 50

        lower_yellow = array([16, 150, 55])
        upper_yellow = array([24, 255, 240])
        mask = cv2.inRange(patch, lower_yellow, upper_yellow)
        yellows = sum(mask > 0)  # check above 800

        lower_green = array([56, 110, 35])
        upper_green = array([66, 240, 120])
        mask = cv2.inRange(patch, lower_green, upper_green)
        greens = sum(mask > 0)  # check above 800

        lower_purple = array([135, 100, 40])
        upper_purple = array([145, 180, 120])
        mask = cv2.inRange(patch, lower_purple, upper_purple)
        purples = sum(mask > 0)  # check above 800

        lower_iri = array([168, 150, 50])
        upper_iri = array([175, 250, 180])
        mask = cv2.inRange(patch, lower_iri, upper_iri)
        iris = sum(mask > 0)  # check above 800

        if reds > 400:
            graph_node = GraphNode((x, y), l, 0)
            graph_nodes.append(graph_node)
        elif blacks > 1000:
            graph_node = GraphNode((x, y), l, 1)
            graph_nodes.append(graph_node)
        elif (browns > 800 and whites > 50) or yellows > 800 or greens > 800 or purples > 800 or iris > 800:
            graph_node = GraphNode((x, y), l, 2)
            graph_nodes.append(graph_node)

        if l == 0:
            graph_node = GraphNode((x, y), l, -1)
            graph_nodes.insert(0, graph_node)

    return graph_nodes