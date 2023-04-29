import cv2
import os
from time import sleep
import re

target_folder = r"J:\Petru\Projects\Results\Vid5"
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


playback_list = sorted_alphanumeric(os.listdir(target_folder))
index = 0
step = 100
while index < len(playback_list)-1:
    os.chdir(target_folder)
    file = cv2.imread(playback_list[index])
    cv2.imshow('playback', file)

    k = cv2.waitKey(5)

    if k == 97: # A key
        index = index - step
        if index < 0:
            index = 0

    elif k == 100: # D KeyHelp.py
        index = index + step

    elif k == 27:
        break

    elif k == 32:  # spacebar
        sleep(0.2)
    else:
        index = index + 1
        sleep(0.2)

    print(index)

    if index > len(playback_list) - 1:
        break
