"""
This module detect the graphical objects & text in images.
"""


import cv2

from .object_detector import detect_objects
from .OCR import detect_text

from config import *

from .show_images import show   # Debugging


DEBUG_MODE = False


def detect_objs_and_text(imgName):
    img = cv2.imread(f'{UPLOADED_IMGS_DIR}/{imgName}')

    graphicalObjs = detect_objects(img)
    textualObjs = detect_text(img)

    if DEBUG_MODE:
        show(img, objects=graphicalObjs, texts=textualObjs)

    if DEBUG_MODE:
        print(graphicalObjs)
        print(textualObjs)
        pass

    return graphicalObjs, textualObjs
