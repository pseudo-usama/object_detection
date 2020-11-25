import cv2
import numpy as np
from config import *
from detector.show_images import show
from detector.object_detection.detect import detect_objects, process_objects, remove_duplicated_objects
from detector.processing import find_areas, sort_wrt_area, find_area_ratios, find_angles, find_distances
from detector.db import insert


def detect_objs(imgName):
    # Loading Image
    img = cv2.imread(f'{UPLOADED_IMGS_DIR}{imgName}')
    height, width, channels = img.shape


    objects = detect_objects(img)   # Detecting objects
    extractedObjects = process_objects(objects, width, height)
    extractedObjects = remove_duplicated_objects(extractedObjects)

    if len(extractedObjects) > 0:
        area_ratios, distances, angles = calc_objects_attr(extractedObjects)
        insert_to_DB(area_ratios, distances, angles, imgName)
    else:
        insert_to_DB([], [], [], imgName)

    show(img, extractedObjects)


# Processing the objects
def calc_objects_attr(extractedObjects):
    find_areas(extractedObjects)
    extractedObjects = sort_wrt_area(extractedObjects)

    areaRatios = find_area_ratios(extractedObjects)
    distances = find_distances(extractedObjects)
    angles = find_angles(extractedObjects)

    return areaRatios, distances, angles


# Insert to Database
def insert_to_DB(areaRatios, distances, angles, imgName):
    insert({
        'area_rations': areaRatios,
        'distances': distances,
        'angles': angles,
        'image_name': imgName
    })


if __name__ == "__main__":
    print("Assalam o Alaikum")
