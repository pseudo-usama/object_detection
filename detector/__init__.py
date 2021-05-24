"""
This module detect the objects in images with the help of object_detector/detect/__init__.py
And then process detected objects data.
Like calculating area ratios, calculate angles etc
And then convert that results into a predefined database structure.
You can view that database structure at DB/structure.json
"""


from math import ceil
import cv2
from numpy import printoptions
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

        nthAreaRatioObj = ceil(obj['areaRatio']/OBJ_AREA_RATIO_RANGE)
        nthAngleObj = ceil(obj['angle']/OBJ_ANGLE_RANGE)
        if i == 1:
            data[f'2.{nthAreaRatioObj}.{nthAngleObj}'] = imgName
            continue

        nthDistanceobj = ceil(obj['distanceRatio']/OBJ_DISTANCE_RATIO_RANGE)

        data[f'{i+1}.{nthAreaRatioObj}.{nthDistanceobj}.{nthAngleObj}'] = imgName

    return data


# 
# Document detector
# 
def document_detertor(img_name):
    img = cv2.imread(UPLOADED_IMGS_DIR+img_name)    # Loading image

    detected_objs = detect_objects(img)
    if len(detected_objs) == 0:
        return None

    bounding_boxes = None
    if len(detected_objs) == 2:
        bounding_boxes = detect_text(img)
        find_distances_to_origin(bounding_boxes, detected_objs[0])

    processed_objs = calc_objects_attr(detected_objs)
    indexed_objs = index_for_DB(processed_objs, img_name)

    # show(img, detected_objs, bounding_boxes)
    print(processed_objs, '\n\n\n', bounding_boxes)

    return processed_objs, bounding_boxes


def index_document(img_name, objs, bounding_boxes):
    sbb = []
    dbb = []
    ubb = []

    # Arranging bounding boxes according to their category
    for bb in bounding_boxes:
        if bb['bounding_box_type'] == 'static':
            sbb.append(bb)
        elif bb['bounding_box_type'] == 'dynamic':
            dbb.append(bb)
        elif bb['bounding_box_type'] == 'unique':
            ubb.append(bb)
        else:   # Not a text
            pass

        del bb['bounding_box_type']

    arranged_bounding_boxes = {
        'sbb': sbb,
        'dbb': dbb,
        'ubb': ubb,
        'imgName': img_name
    }

    indexed_data = index_bounding_boxes(objs, arranged_bounding_boxes, len(bounding_boxes))
    return indexed_data


def index_bounding_boxes(objs, data_to_save, no_of_bounding_boxes):
    data = {}

    for i, obj in enumerate(objs):
        if i == 0:
            continue

        nth_angle_obj = str(ceil(obj['angle']/DOC_ANGLE_RANGE))
        nth_area_ratio_obj = str(ceil(obj['areaRatio']/DOC_AREA_RATIO_RANGE))

        data[nth_angle_obj] = {
            nth_area_ratio_obj: {
                str(no_of_bounding_boxes): data_to_save
            }
        }

        return data


if __name__ == "__main__":
    print(
"""This is the module to detecte objects & texts in images.
Try importing & calling detect_objs(<path_to_your_image>)
And it will return an dictionary of detected objects & texts.
Good luck ;)"""
)
