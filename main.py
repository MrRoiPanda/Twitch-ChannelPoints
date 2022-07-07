import os
from time import sleep, time

import cv2
import keyboard
import mss
import numpy as np
import pyautogui

script_dir = os.path.dirname(__file__)

pyautogui.PAUSE = 0

sct = mss.mss()
screen = {
    'left': 0,
    'top': 0,
    'width': 2539,
    'height': 1439
}

def find_button(button_img):
    push = False
    while push == False:
        w = button_img.shape[1]
        h = button_img.shape[0]

        scr = np.array(sct.grab(screen))
        scr_remove = scr[:, :, :3]

        result = cv2.matchTemplate(scr_remove, button_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        print(f"Max Val: {max_val} Max Loc: {max_loc}")
        src = scr.copy()

        threshold = .80
        if max_val > threshold:
            cv2.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2)
            pyautogui.moveTo((max_loc[0] + w/2, max_loc[1] + h/2))
            sleep(.50)
            pyautogui.click()
            push = True
        sleep(.10)

print("Press 's' to start playing !")
print("Once started press 'q' to quit !")
keyboard.wait('s')
print("running ...")

faves_img = cv2.imread(os.path.join(script_dir, 'twitch-points.png'))

while True:
    waitTime = 300
    sleep(waitTime - time() % waitTime)
    find_button(faves_img)
    if keyboard.is_pressed('q'):
        break