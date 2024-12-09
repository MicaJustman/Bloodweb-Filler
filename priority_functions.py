from os import walk, path
from cv2 import imread, COLOR_BGR2GRAY, cvtColor, matchTemplate, TM_CCOEFF_NORMED, minMaxLoc, rectangle

def read_templates_from_folder(folder_path):
    templates = []
    for root, dirs, files in walk(folder_path):
        for file in files:
            template_path = path.join(root, file)
            template = imread(template_path, COLOR_BGR2GRAY)
            templates.append(template)
    return templates


def template_matching(main_image, templates):
    gray = cvtColor(main_image, COLOR_BGR2GRAY)
    priority = []

    for template in read_templates_from_folder('Templates/Offerings'):
        template_gray = cvtColor(template, COLOR_BGR2GRAY)

        w, h = template_gray.shape[::-1]
        res = matchTemplate(gray, template_gray, TM_CCOEFF_NORMED)

        max_val = 1
        counter = 0
        while max_val > .7 and counter <= 4:
            counter += 1
            min_val, max_val, min_loc, max_loc = minMaxLoc(res)

            if max_val > .7:
                res[max_loc[1] - h // 2:max_loc[1] + h // 2 + 1, max_loc[0] - w // 2:max_loc[0] + w // 2 + 1] = 0
                priority.append((max_loc[0] + w / 2, max_loc[1] + h / 2))
                print(str(priority[len(priority) - 1]) + "  " + str(max_val))
                main_image = rectangle(main_image, (max_loc[0], max_loc[1]), (max_loc[0] + w + 1, max_loc[1] + h + 1), (255, 0, 0), 3)

    for template in read_templates_from_folder('Templates/' + templates):
        template_gray = cvtColor(template, COLOR_BGR2GRAY)

        w, h = template_gray.shape[::-1]
        res = matchTemplate(gray, template_gray, TM_CCOEFF_NORMED)

        max_val = 1
        counter = 0
        while max_val > .8 and counter <= 4:
            min_val, max_val, min_loc, max_loc = minMaxLoc(res)
            counter += 1

            if max_val > .8:
                res[max_loc[1] - h // 2:max_loc[1] + h // 2 + 1, max_loc[0] - w // 2:max_loc[0] + w // 2 + 1] = 0
                priority.append((max_loc[0] + w / 2, max_loc[1] + h / 2))
                print(str(priority[len(priority) - 1]) + "  " + str(max_val))
                main_image = rectangle(main_image, (max_loc[0], max_loc[1]), (max_loc[0] + w + 1, max_loc[1] + h + 1), (255, 0, 0), 3)

    return priority