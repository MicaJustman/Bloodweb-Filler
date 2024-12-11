import math

import cv2

from screen_functions import showScreen


def classifyEdges(image, nodes):
    counter = 0
    processed = []
    lines = []

    line_template = cv2.imread("stored/line.png")
    red_line_template= cv2.imread("stored/red_line.png")
    entity_line_template = cv2.imread("stored/entity_line.png")

    for x in nodes:
        for y in nodes:
            if x != y and math.sqrt((x.position[0] - y.position[0])**2 + (x.position[1] - y.position[1])**2) < 200:
                if (x, y) not in processed and (y, x) not in processed:
                    processed.append((x, y))

    for x in processed:
        min_x = min(x[0].position[0], x[1].position[0])
        max_x = max(x[0].position[0], x[1].position[0])
        min_y = min(x[0].position[1], x[1].position[1])
        max_y = max(x[0].position[1], x[1].position[1])
        line = image[min_y - 10:max_y + 10, min_x - 10:max_x + 10]

        delta_x = x[1].position[0] - x[0].position[0]
        delta_y = x[1].position[1] - x[0].position[1]
        angle = math.atan2(delta_y, delta_x)

        angle_degrees = math.degrees(angle)

        center = (line.shape[1] // 2, line.shape[0] // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle_degrees, 1.0)
        abs_cos = abs(rotation_matrix[0, 0])
        abs_sin = abs(rotation_matrix[0, 1])

        new_width = int(line.shape[0] * abs_sin + line.shape[1] * abs_cos)
        new_height = int(line.shape[0] * abs_cos + line.shape[1] * abs_sin)

        rotation_matrix[0, 2] += (new_width / 2) - center[0]
        rotation_matrix[1, 2] += (new_height / 2) - center[1]

        line = cv2.warpAffine(line, rotation_matrix, (new_width, new_height), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
        cropped_line = line[int(line.shape[0] / 2) - 10: int(line.shape[0] / 2) + 10, 0: line.shape[1] - 0]

        result = cv2.matchTemplate(cropped_line, line_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val_line, min_loc, max_loc = cv2.minMaxLoc(result)
        result = cv2.matchTemplate(cropped_line, red_line_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val_red, min_loc, max_loc = cv2.minMaxLoc(result)
        result = cv2.matchTemplate(cropped_line, entity_line_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val_black, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val_line > .75 or max_val_red > .75 or max_val_black > .75:
            lines.append(x)

    return lines
