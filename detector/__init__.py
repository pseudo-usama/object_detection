"""
This module detect the graphical objects & text in images.
"""


import cv2

from .object_detector import detect_objects
from .OCR import detect_text

from config import *

from .show_img import show   # Debugging

from logger import log
LOGGER = log(__name__)


DEBUG_MODE = GLOBAL_DEBUG and False


def detect_objs_and_text(imgName):
    img = cv2.imread(f'{UPLOADED_IMGS_DIR}/{imgName}')

    graphicalObjs = detect_objects(img)
    textualObjs = detect_text(img)

    if DEBUG_MODE:
        show(img, objects=graphicalObjs, texts=textualObjs)

    LOGGER.info(f'Graphical objs: {len(graphicalObjs)}')
    LOGGER.info(f'Textual objs: {len(textualObjs)}')

    if DEBUG_MODE:
        print(graphicalObjs)
        print(textualObjs)
        pass

    return graphicalObjs, textualObjs
