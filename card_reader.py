import cv2
import numpy as np
import pyautogui
import os

TEMPLATE_DIR = 'templates/'
THRESHOLD = 0.8

def take_card_screenshot(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save('current_card.png')
    return 'current_card.png'

def recognize_card(image_path):
    card_img = cv2.imread(image_path)
    card_img_gray = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)

    best_match = None
    highest_val = 0

    for filename in os.listdir(TEMPLATE_DIR):
        template = cv2.imread(os.path.join(TEMPLATE_DIR, filename), 0)
        result = cv2.matchTemplate(card_img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > highest_val:
            highest_val = max_val
            best_match = filename

    if highest_val >= THRESHOLD and best_match:
        value, _, suit = best_match.replace('.png', '').split('_')
        return value, suit
    else:
        return None, None
