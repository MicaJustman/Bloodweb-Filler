import math
import cv2
import numpy as np
from numpy import uint16, around
from sklearn.cluster import KMeans
from win32gui import GetDesktopWindow, GetWindowRect
from screen_functions import grabImage, showScreen

def calculate_distance(point, center):
    x1, y1 = point[0], point[1]
    x2, y2 = center[0], center[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def detectNodes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=30,
        param1=30,
        param2=30,
        minRadius=32,
        maxRadius=38
    )

    with open('stored/Centers', 'r') as f:
        centers = [tuple(map(int, line.strip().split(','))) for line in f.readlines()]

    changeFile = False
    markCenters = True

    if circles is not None:
        circles = uint16(around(circles))

        if not markCenters:
            for circle in circles[0, :]:
                center = (circle[0], circle[1])
                radius = circle[2]
                cv2.circle(img, center, radius, (0, 255, 0), 2)
                cv2.circle(img, center, 2, (0, 0, 255), 3)

                if changeFile:
                    is_new_center = True
                    for existing_center in centers:
                        distance = math.sqrt((center[0] - existing_center[0]) ** 2 + (center[1] - existing_center[1]) ** 2)
                        if distance < 30:
                            is_new_center = False
                            break

                    if is_new_center:
                        with open('stored/Centers', 'a') as f:
                            f.write(f"{center[0]},{center[1]}\n")
        else:
            for center in centers:
                cv2.circle(img, center, 2, (0, 0, 255), 3)

    return img

def calculateLevels(web_center):
    distances = []
    with open('stored/Centers', 'r') as f:
        centers = [tuple(map(int, line.strip().split(','))) for line in f.readlines()]

        for center in centers:
            distances.append(calculate_distance(web_center, center))

        data = np.array(distances).reshape(-1, 1)

        kmeans = KMeans(n_clusters=3, random_state=42)
        kmeans.fit(data)

        clusters = sorted(kmeans.cluster_centers_.flatten().tolist())

        with open('stored/Levels', 'a') as f:
            f.write(f"{clusters[0]},{clusters[1]},{clusters[2]}\n")
    return

def sortNodes(image):
    centers = []
    levels = []

    bottom = []
    middle = []
    top = []

    with open('stored/Centers', 'r') as f:
        centers = [list(map(int, line.strip().split(','))) for line in f.readlines()]

    with open('stored/Levels', 'r') as f:
        line = f.readline().strip()
        levels = [float(x) for x in line.split(',')]

    for center in centers:
        distance = calculate_distance((center[0], center[1]), web_center)
        center_level = min(levels, key=lambda x: abs(x - distance))

        if len(center) == 2:
            if center_level == levels[0]:
                bottom.append(center +[1])
            elif center_level == levels[1]:
                middle.append(center + [2])
            else:
                top.append(center + [3])
        else:
            if center_level == levels[0]:
                bottom.append(center)
            elif center_level == levels[1]:
                middle.append(center)
            else:
                top.append(center)

    sorted_centers = bottom + middle + top

    center_node = cv2.imread('stored/center_node.png')
    result = cv2.matchTemplate(image, center_node, cv2.TM_CCOEFF_NORMED)
    min_val, max_val_line, min_loc, max_loc = cv2.minMaxLoc(result)

    with open('stored/Centers', 'w') as f:
        for x, y, l in sorted_centers:
            f.write(f"{x},{y},{l}\n")

        f.write(f"{max_loc[0] + center_node.shape[0] // 2},{max_loc[1] + center_node.shape[1] // 2},0")

hwnd = GetDesktopWindow()
dim = GetWindowRect(hwnd)
web_center = (683, 562)

rawImage = grabImage(dim[2], dim[3], 0, 0, hwnd)
#circles = detectNodes(rawImage)
#calculateLevels(web_center)
sortNodes(rawImage)
