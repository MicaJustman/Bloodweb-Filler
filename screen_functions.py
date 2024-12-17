import os
from win32con import SRCCOPY
from win32gui import GetWindowDC, ReleaseDC, DeleteObject
from win32ui import CreateDCFromHandle, CreateBitmap
from numpy import frombuffer, uint8
import cv2
def grabImage(width, height, offset_width, offset_height, DBDhwnd):
    wDC = GetWindowDC(DBDhwnd)
    dcObj = CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height), dcObj, (offset_width, offset_height), SRCCOPY)

    bmpinfo = dataBitMap.GetInfo()
    bmpstr = dataBitMap.GetBitmapBits(True)
    img = frombuffer(bmpstr, dtype=uint8)
    img = img.reshape((bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    ReleaseDC(DBDhwnd, wDC)
    DeleteObject(dataBitMap.GetHandle())
    return img

colors = {
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Blue": (255, 0, 0),
    "Yellow": (0, 255, 255),
    "Cyan": (255, 255, 0),
    "Magenta": (255, 0, 255),
    "Orange": (175, 96, 26),
    "Grey": (93, 109, 126),
    "Brown": (109, 76, 65),
    "Pink": (186, 104, 200),
    "Black": (0, 0, 0),
    "White": (255, 255, 255)
}

def save(image, name, counter):
    if not os.path.exists('data/' + str(counter) + '/'):
        os.makedirs('data/' + str(counter) + '/')

    file_path = os.path.join('data/' + str(counter) + '/', name)
    cv2.imwrite(file_path, image)
    return file_path

def showScreen(img):
    cv2.imshow("Captured Window", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def showNodes(img, nodes, s, counter=0):
    image = img.copy()
    for node in nodes:
        center = (node.position[0], node.position[1])

        if node.type == -1: # Center Node
            cv2.circle(image, center, 5, colors["White"], 14)
        if node.type == 0:  # Red Nodes
            cv2.circle(image, center, 5, colors["Red"], 14)
        if node.type == 1:  # Black Nodes
            cv2.circle(image, center, 5, colors["Blue"], 14)
        if node.type == 2:  # Green Nodes
            cv2.circle(image, center, 5, colors["Green"], 14)

    if s:
        save(image, "nodes.png", counter)
    else:
        showScreen(image)

def showEdges(img, lines, counter, s):
    image = img.copy()
    for x in lines:
        cv2.line(image, x[0].position, x[1].position, colors["Green"], 2, cv2.LINE_AA)

    if s:
        save(image, "lines.png", counter)
    else:
        showScreen(image)

def showGraphs(img, graphs, edges, s, counter=0):
    image = img.copy()
    counter = 0

    for graph in graphs:
        for edge in edges:
            if edge[0] in graph.nodes and edge[1] in graph.nodes:
                cv2.line(image, edge[0].position, edge[1].position, list(colors.values())[counter], 4, cv2.LINE_AA)

        for node in graph.roots:
            cv2.circle(image, node.position, 7, list(colors.values())[counter], 16)

        counter += 1

    if s:
        save(image, "graphs.png", counter)
    else:
        showScreen(image)