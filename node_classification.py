import cv2
from numpy import array, sum
from screen_functions import showScreen

def classifyNodes(image):
    height, width = image.shape[:2]
    patch_size = 80
    half_patch = patch_size // 2

    # List to collect all patches and their coordinates
    predictions = []

    with open('stored/Centers', 'r') as f:
        centers = [tuple(map(int, line.strip().split(','))) for line in f.readlines()]

    for (x, y) in centers:
        # Calculate the bounding box for the patch centered at (x, y)
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
            predictions.append((x, y, 3, 0))
        elif blacks > 1000:
            predictions.append((x, y, 0, 0))
        elif browns > 800 and whites > 50:
            predictions.append((x, y, 2, 1))
        elif yellows > 800:
            predictions.append((x, y, 2, 2))
        elif greens > 800:
            predictions.append((x, y, 2, 3))
        elif purples > 800:
            predictions.append((x, y, 2, 4))
        elif iris > 800:
            predictions.append((x, y, 2, 5))
        else:
            predictions.append((x, y, 1, 0))


    return predictions

























'''transform = transforms.Compose([
    transforms.Resize((100, 100)),
    transforms.ToTensor(),
    transforms.Normalize([.5], [.5], [.5])
])

device = torch.device('cuda')


def evaluateImage(image, model):
    height, width = image.shape[:2]
    patch_size = 100
    half_patch = patch_size // 2

    # List to collect all patches and their coordinates
    patches = []

    with open('Centers', 'r') as f:
        centers = [tuple(map(int, line.strip().split(','))) for line in f.readlines()]

        for (x, y) in centers:
            # Calculate the bounding box for the patch centered at (x, y)
            left = max(x - half_patch, 0)
            top = max(y - half_patch, 0)
            right = min(x + half_patch, width)
            bottom = min(y + half_patch, height)

            patch = image[top:bottom, left:right]
            patch_pil = fromarray(patch)
            patch_tensor = transform(patch_pil).unsqueeze(0)
            patches.append(patch_tensor)

    patches_tensor = torch.cat(patches, dim=0).to(device)

    with torch.no_grad():
        outputs = model(patches_tensor)

    _, predicted_classes = torch.max(outputs, 1)
    predictions = [(centers[i][0], centers[i][1], predicted_classes[i].item()) for i in range(len(centers))]

    return predictions'''