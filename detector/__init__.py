"""
This module detect the objects in images with the help of object_detector/detect/__init__.py
And then process detected objects data.
Like calculating area ratios, calculate angles etc
And then convert that results into a predefined database structure.
You can view that database structure at DB/structure.json
"""


import copy
from math import ceil
import cv2
from detector import index_data

# Object detection
from detector.object_detector import detect_objects
from detector.processing import *

# OCR
from detector.OCR import detect_text
from detector.process import find_distances_to_origin

# Indexing
from detector.index_data import index

# Debugging
from detector.show_images import show


DEBUG_MODE = True


def detect_objs_and_text(img_path):
    img = cv2.imread(img_path)

    graphicalObjs = detect_objects(img)
    textualObjs = detect_text(img)

    if DEBUG_MODE:
        show(img, objects=graphicalObjs, texts=textualObjs)

    graphicalObjs = calc_objects_attr(graphicalObjs)

    # print(graphical_objs)
    # print(textual_objs)

    ssb = textualObjs[0:-2]
    dbb = [{'topLeft': dbb['topLeft'], 'dimensions': dbb['dimensions'], 'regex': r'/^([a-zA-Z0-9_-]){3,5}$/'}
           for dbb in textualObjs[-3:-1]]

    indexed_data = index(graphicalObjs, ssb, dbb, img_path)

    print(indexed_data)


# Processing the objects
def calc_objects_attr(objs):
    data = {}

    find_areas(objs)
    objs = sort_wrt_area(objs)

    data['distanceRatio'] = find_distances(objs)
    data['angle'] = find_angles(objs)

    return data


#
# Document detector
#
