from time import sleep

import keyboard
from pyautogui import moveTo, mouseDown, mouseUp

def move_and_click(location):
    moveTo(location[0], location[1], duration=0.1)
    mouseDown()
    sleep(0.1)
    mouseUp()
    moveTo(10, 10, duration=0.1)
    sleep(.5)


def move_and_click_list(matches):
    for location in matches:
        x, y = location
        moveTo(x + 265, y + 140, duration=0.1)
        mouseDown()
        sleep(0.1)
        mouseUp()
        moveTo(275, 150, duration=0.1)
        sleep(1.3)

def monitor_delete_key(event):
    while True:
        if keyboard.is_pressed('alt'):
            event.set()
            return
        sleep(0.1)