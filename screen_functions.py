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
    "Black": (0, 0, 0)
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

def showNodes(img, nodes, counter, s):
    image = img.copy()
    for (x, y, node_type, subclass) in nodes:
        center = (x, y)
        cv2.circle(image, (683, 562), 5, (255, 0, 0), 14)

        if node_type == 0:  # Black Nodes
            cv2.circle(image, center, 5, colors["Black"], 14)
        if node_type == 1:  # Blank Nodes
            cv2.circle(image, center, 5, colors["Green"], 14)
        if node_type == 2:  # Green Nodes
            if subclass == 1:
                cv2.circle(image, center, 40, (51, 64, 92), 5)
            elif subclass == 2:
                cv2.circle(image, center, 40, (51, 189, 255), 5)
            elif subclass == 3:
                cv2.circle(image, center, 40, (55, 204, 47), 5)
            elif subclass == 4:
                cv2.circle(image, center, 40, (188, 19, 236), 5)
            elif subclass == 5:
                cv2.circle(image, center, 40, (59, 29, 152), 5)
        if node_type == 3:  # Red Nodes
            cv2.circle(image, center, 5, colors["Red"], 14)

    if s:
        save(image, "nodes.png", counter)
    else:
        showScreen(image)

def showLines(img, lines, counter, s):
    image = img.copy()
    for x in lines:
        cv2.line(image, x[0], x[1], colors["Green"], 2, cv2.LINE_AA)

    if s:
        save(image, "lines.png", counter)
    else:
        showScreen(image)

def showTrees(img, trees, counter, s):
    image = img.copy()
    color_list = list(colors.values())
    counter = 0

    for tree in trees:
        treenodes = tree.traverse()
        change_color = False

        for treenode in treenodes:
            if tree.root.parent is None and len(tree.root.children) == 0:
                cv2.circle(image, (treenode.node[0], treenode.node[1]), 40, colors["Black"], 4)
            else:
                cv2.circle(image, (treenode.node[0], treenode.node[1]), 40, color_list[counter], 4)
                change_color = True

            if tree.corrupted:
                cv2.circle(image, (tree.root.node[0], tree.root.node[1]), 7 , colors["Black"], 18)

            if tree.root.parent is None:
                cv2.putText(image, str(tree.children_tally()), (tree.root.node[0] - 5, tree.root.node[1] + 7), cv2.FONT_HERSHEY_SIMPLEX, .7, color_list[counter], 2, 1)

        if change_color:
            counter += 1

    if s:
        save(image, "tree.png", counter)
    else:
        showScreen(image)