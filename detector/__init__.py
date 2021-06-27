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


DEBUG_MODE = True


def detect_objs(img_name, add_deviation=False):
    img = cv2.imread(UPLOADED_IMGS_DIR+img_name)    # Loading Image

    objs = detect_objects(img)   # Detecting objects

    if DEBUG_MODE:
        show(img, objs) # Just debugging purposes

    if len(objs) == 0:
        return None, None

    objects = calc_objects_attr(objs)
    data, data_to_search = index_for_DB(objects, img_name, add_deviation=add_deviation)   # Contains data for DB, and maybe data for search

    print(f'\n\n{data}\n\n{data_to_search}\n\n')

    return data, data_to_search


# Processing the objects
def calc_objects_attr(extractedObjects):
    find_areas(extractedObjects)
    extractedObjects = sort_wrt_area(extractedObjects)

    find_area_ratios(extractedObjects)
    find_distances(extractedObjects)
    find_angles(extractedObjects)

    return extractedObjects


# Index the data according to database schema
def index_for_DB(objects, imgName, add_deviation=False):
    data = {}
    data_for_search = {}
    no_of_objs = len(objects)
    
    for i, obj in enumerate(objects):
        if i == 0:
            data[f'1.{no_of_objs}.{obj["classId"]}'] = imgName
            data_for_search[f'1.{no_of_objs}.{obj["classId"]}'] = imgName
            continue

        nthAreaRatioObj = ceil(obj['areaRatio']/OBJ_AREA_RATIO_RANGE)
        nthAngleObj = ceil(obj['angle']/OBJ_ANGLE_RANGE)
        if i == 1:
            data[f'2.{nthAreaRatioObj}.{nthAngleObj}.{no_of_objs}'] = imgName
            data_for_search[f'2.{nthAreaRatioObj}.{nthAngleObj}.{no_of_objs}'] = imgName
            if add_deviation:
                for nAreaObj in range(nthAreaRatioObj-OBJ_AREA_DEVIATION, nthAreaRatioObj+OBJ_AREA_DEVIATION+1, OBJ_AREA_RATIO_RANGE):
                    for nAngleObj in range(nthAngleObj-OBJ_ANGLE_DEVIATION, nthAngleObj+OBJ_ANGLE_DEVIATION+1, OBJ_DISTANCE_RATIO_RANGE):
                        data_for_search[f'2.{nAreaObj}.{nAngleObj}.{no_of_objs}'] = imgName
            continue

        nthDistanceobj = ceil(obj['distanceRatio']/OBJ_DISTANCE_RATIO_RANGE)

        data[f'{i+1}.{nthAreaRatioObj}.{nthDistanceobj}.{nthAngleObj}.{no_of_objs}'] = imgName
        data_for_search[f'{i+1}.{nthAreaRatioObj}.{nthDistanceobj}.{nthAngleObj}.{no_of_objs}'] = imgName
        if add_deviation:
            for nAreaObj in range(nthAreaRatioObj-OBJ_AREA_DEVIATION, nthAreaRatioObj+OBJ_AREA_DEVIATION+1, OBJ_AREA_RATIO_RANGE):
                for nDistObj in range(nthDistanceobj-OBJ_DISTANCE_DEVIATION, nthDistanceobj+OBJ_DISTANCE_DEVIATION+1, OBJ_DISTANCE_RATIO_RANGE):
                    for nAngleObj in range(nthAngleObj-OBJ_ANGLE_DEVIATION, nthAngleObj+OBJ_ANGLE_DEVIATION+1, OBJ_AREA_RATIO_RANGE):
                        data_for_search[f'{i+1}.{nAreaObj}.{nDistObj}.{nAngleObj}.{no_of_objs}'] = imgName

    if add_deviation:
        # Removing duplicates
        new_data_for_search = copy.deepcopy(data_for_search)

        for key in data_for_search.keys():
            dubs = [k for k in data_for_search.keys() if key in k]
            if len(dubs) > 2:
                del new_data_for_search[key]
        
        return data, new_data_for_search

    return data, None


# 
# Document detector
# 
def document_detertor(img_name):
    img = cv2.imread(UPLOADED_IMGS_DIR+img_name)    # Loading image

    detected_objs = detect_objects(img)
    bounding_boxes = detect_text(img)

    # if len(detected_objs) == 0:
    #     if DEBUG_MODE:
    #         show(img, [])  # Just for debugging
    #     return None, None

    origin = (0, 0)
    if len(detected_objs) > 1:
        origin = detected_objs[0]['topLeft']
    find_distances_to_origin(bounding_boxes, origin)

    if len(bounding_boxes) == 0:
        return None, None

    processed_objs = []
    if len(detected_objs) > 1:
        processed_objs = calc_objects_attr(detected_objs)
    # indexed_objs = index_for_DB(processed_objs, img_name) # TODO: I've changed the index_for_DB() parameters.

    # Just for debugging
    # print(processed_objs, '\n\n\n', bounding_boxes)
    if DEBUG_MODE:
        show(img, detected_objs, bounding_boxes)

    return processed_objs, bounding_boxes


def index_document_data(img_name, objs, bounding_boxes):
    arranged_bounding_boxes = arrange_bounding_boxes_types(img_name, objs, bounding_boxes)
    indexed_data = index_bounding_boxes(objs, arranged_bounding_boxes, len(bounding_boxes), add_deviation=False)
    return indexed_data


def arrange_bounding_boxes_types(img_name, objs, bounding_boxes):
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
        'imgName': img_name,
        'sbb': sbb,
        'dbb': dbb,
        'ubb': ubb
    }

    return arranged_bounding_boxes


def index_bounding_boxes(objs, data_to_save, no_of_bounding_boxes, add_deviation=False):
    data = {}
    data_for_search = {}
    no_of_bounding_boxes = no_of_bounding_boxes

    if len(objs) == 0:
        # Here -2 is to indicate on. of objects is 0
        if add_deviation:
            for nBoundingBox in range(no_of_bounding_boxes-DOC_BOUNDING_BOXES_DEVIATION, no_of_bounding_boxes+DOC_BOUNDING_BOXES_DEVIATION+1):
                data_for_search[f'-2.{nBoundingBox}'] = data_to_save

            return data_for_search

        data[f'-2.{no_of_bounding_boxes}'] = data_to_save
        return data

    if len(objs) == 1:
        # Here -1 is to indicate on. of objects is 1
        if add_deviation:
            for nBoundingBox in range(no_of_bounding_boxes-DOC_BOUNDING_BOXES_DEVIATION, no_of_bounding_boxes+DOC_BOUNDING_BOXES_DEVIATION+1):
                data_for_search[f'-1.{nBoundingBox}'] = data_to_save

            return data_for_search

        data[f'-1.{no_of_bounding_boxes}'] = data_to_save
        return data

    for i, obj in enumerate(objs):
        if i == 0:
            continue

        nth_angle_obj = ceil(obj['angle']/DOC_ANGLE_RANGE)
        nth_area_ratio_obj = ceil(obj['areaRatio']/DOC_AREA_RATIO_RANGE)

        data[f'{str(nth_angle_obj)}.{str(nth_area_ratio_obj)}.{str(no_of_bounding_boxes)}'] = data_to_save

        if add_deviation:
            for nAngleObj in range(nth_angle_obj-OBJ_ANGLE_DEVIATION, nth_angle_obj+OBJ_ANGLE_DEVIATION+1, DOC_ANGLE_RANGE):
                for nAreaObj in range(nth_area_ratio_obj-DOC_AREA_DEVIATION, nth_area_ratio_obj+DOC_AREA_DEVIATION+1, DOC_AREA_RATIO_RANGE):
                    # print('1234', nth_area_ratio_obj, nAreaObj)
                    for nBoundingBox in range(no_of_bounding_boxes-DOC_BOUNDING_BOXES_DEVIATION, no_of_bounding_boxes+DOC_BOUNDING_BOXES_DEVIATION+1):
                        data_for_search[f'{nAngleObj}.{nAreaObj}.{nBoundingBox}'] = data_to_save

    if add_deviation:
        # Removing duplicates
        new_data_for_search = copy.deepcopy(data_for_search)

        for key in data_for_search.keys():
            dubs = [k for k in data_for_search.keys() if key in k]
            if len(dubs) > 2:
                del new_data_for_search[key]

        print(data_for_search)
        return new_data_for_search

    return data


if __name__ == "__main__":
    print(
"""This is the module to detecte objects & texts in images.
Try importing & calling detect_objs(<path_to_your_image>)
And it will return an dictionary of detected objects & texts.
Good luck ;)"""
)
