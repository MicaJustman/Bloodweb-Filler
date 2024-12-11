from time import time
from sklearn.cluster import KMeans
import cv2
import numpy as np
from win32gui import GetDesktopWindow, GetWindowRect
from screen_functions import grabImage, showScreen

def savePatches():
    hwnd = GetDesktopWindow()
    rect = GetWindowRect(hwnd)
    image = grabImage(rect[2], rect[3], 0, 0, hwnd)

    patch_size = 100
    half_patch = patch_size // 2
    counter = 10

    height, width = image.shape[:2]


    with open('stored/Centers', 'r') as f:
        centers = [tuple(map(int, line.strip().split(','))) for line in f.readlines()]

        for (x, y) in centers:
            left = max(x - half_patch, 0)
            top = max(y - half_patch, 0)
            right = min(x + half_patch, width)
            bottom = min(y + half_patch, height)

            patch = image[top:bottom, left:right]

            name = 'Nodes/' + str(int(time()) - 1700000000) + str(counter) + '.png'
            counter += 1
            cv2.imwrite(name, patch)


def top_colors_with_clustering(image_path, n_colors=5):
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    pixels = hsv_image.reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)

    cluster_centers = kmeans.cluster_centers_

    unique, counts = np.unique(kmeans.labels_, return_counts=True)
    sorted_indices = np.argsort(-counts)

    top_colors = cluster_centers[sorted_indices].astype(int)

    return top_colors

def visualize_colors(colors):
    # Create an image to visualize the colors
    swatch = np.zeros((100, 500, 3), dtype=np.uint8)

    # Divide the swatch into sections, one for each color
    section_width = swatch.shape[1] // len(colors)
    for i, color in enumerate(colors):
        start_x = i * section_width
        end_x = (i + 1) * section_width
        swatch[:, start_x:end_x] = color

    # Convert from HSV to BGR for visualization in OpenCV
    swatch_bgr = cv2.cvtColor(swatch, cv2.COLOR_HSV2BGR)
    cv2.imshow("Top Colors", swatch_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = "patch.png"
top_colors = top_colors_with_clustering(image_path, n_colors=5)
print(f"Top HSV colors (clustered): {top_colors}")
visualize_colors(top_colors)