"""
This module detect the objects in images with the help of object_detector/detect/__init__.py
And then process detected objects data.
Like calculating area ratios, calculate angles etc
And then convert that results into a predefined database structure.
You can view that database structure at DB/structure.json
"""


from math import ceil
import cv2
from config import *
from DB.schema import *

# Object detection
from detector.object_detector import detect_objects
from detector.processing import *

# OCR
from detector.OCR import detect_text
from detector.process import find_distances_to_origin

# Debugging
from detector.show_images import show


def detect_objs(img_name):
    img = cv2.imread(UPLOADED_IMGS_DIR+img_name)    # Loading Image

    objs = detect_objects(img)   # Detecting objects
    if len(objs) == 0:
        return None

    objects = calc_objects_attr(objs)
    toDB = index_for_DB(objects, img_name)

    # Just debugging purposes
    print(toDB)
    show(img, objs)

    return toDB


def document_detertor(img_name):
    img = cv2.imread(UPLOADED_IMGS_DIR+img_name)    # Loading image

    objs = detect_objects(img)
    if len(objs) == 0:
        return None

    boundingBoxes = None
    if len(objs) == 2:
        boundingBoxes = detect_text(img)
        find_distances_to_origin(boundingBoxes, objs[0])

    objects = calc_objects_attr(objs)
    toDB = index_for_DB(objects, img_name)

    show(img, objs, boundingBoxes)
    print(toDB)

    return toDB

# Processing the objects
def calc_objects_attr(extractedObjects):
    find_areas(extractedObjects)
    extractedObjects = sort_wrt_area(extractedObjects)

    find_area_ratios(extractedObjects)
    find_distances(extractedObjects)
    find_angles(extractedObjects)

    return extractedObjects


# Index the data according to database schema
def index_for_DB(objects, imgName):
    data = {}
    for i, obj in enumerate(objects):
        if i == 0:
            data['1'] = imgName
            continue

        nthAreaRatioObj = ceil(obj['areaRatio']/AREA_RATIO_RANGE)
        nthAngleObj = ceil(obj['angle']/ANGLE_RANGE)
        if i == 1:
            data[f'2.{nthAreaRatioObj}.{nthAngleObj}'] = imgName
            continue

        nthDistanceobj = ceil(obj['distanceRatio']/DISTANCE_RATIO_RANGE)

        data[f'{i+1}.{nthAreaRatioObj}.{nthDistanceobj}.{nthAngleObj}'] = imgName

    return data


if __name__ == "__main__":
    print(
"""This is the module to detecte objects & texts in images.
Try importing & calling detect_objs(<path_to_your_image>)
And it will return an dictionary of detected objects & texts.
Good luck ;)"""
)
