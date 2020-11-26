from math import ceil
import cv2
import numpy as np
from config import *
from DB.schema import *
from detector.show_images import show
from detector.object_detection.detect import *
from detector.processing import *


def detect_objs(imgName):
    # Loading Image
    img = cv2.imread(UPLOADED_IMGS_DIR+imgName)
    height, width, channels = img.shape

    objects = detect_objects(img)   # Detecting objects
    extractedObjects = process_objects(objects, width, height)
    extractedObjects = remove_duplicated_objects(extractedObjects)

    if len(extractedObjects) > 0:
        objects = calc_objects_attr(extractedObjects)
        toDB = index_for_DB(objects, imgName)

        return toDB

    # show(img, extractedObjects)
    return None


# Processing the objects
def calc_objects_attr(extractedObjects):
    find_areas(extractedObjects)
    extractedObjects = sort_wrt_area(extractedObjects)

    find_area_ratios(extractedObjects)
    find_distances(extractedObjects)
    find_angles(extractedObjects)

    return extractedObjects


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
    print("...")
