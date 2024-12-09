import math
import cv2
from numpy import uint16, around
from win32gui import GetDesktopWindow, GetWindowRect
from screen_functions import grabImage, showScreen

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

    with open('Centers', 'r') as f:
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
                        with open('Centers', 'a') as f:
                            f.write(f"{center[0]},{center[1]}\n")
        else:
            for center in centers:
                cv2.circle(img, center, 2, (0, 0, 255), 3)

    return img

hwnd = GetDesktopWindow()
dim = GetWindowRect(hwnd)

rawImage = grabImage(dim[2], dim[3], 0, 0, hwnd)
circles = detectNodes(rawImage)
showScreen(circles)
