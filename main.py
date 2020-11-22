import cv2
import numpy as np
from show_images import show
from object_detection.detect import detect_objects, process_objects, remove_duplicated_objects
from processing import find_areas, sort_wrt_area, find_area_ratios, find_angles, find_distances
from db import insert


image_name = 'resturant.jpg'


# Loading Image
img = cv2.imread(f'images/{image_name}')
height, width, channels = img.shape


objects = detect_objects(img)   # Detecting objects
extractedObjects = process_objects(objects, width, height)
extractedObjects = remove_duplicated_objects(extractedObjects)


# Processing the objects
def calc_objects_attr():
    global extractedObjects

    find_areas(extractedObjects)
    extractedObjects = sort_wrt_area(extractedObjects)

    areaRatios = find_area_ratios(extractedObjects)
    distances = find_distances(extractedObjects)
    angles = find_angles(extractedObjects)

    return areaRatios, distances, angles


# Insert to Database
def insert_to_DB(area_ratios, distances, angles):
    insert({
        'area_rations': area_ratios,
        'distances': distances,
        'angles': angles,
        'image_name': image_name
    })


if len(extractedObjects) > 0:
    area_ratios, distances, angles = calc_objects_attr()
    insert_to_DB(area_ratios, distances, angles)
else:
    insert_to_DB([], [], [])


show(img, extractedObjects)
