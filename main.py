import cv2
import numpy as np
from show_images import mark_objects, show
from object_detection.detect import detect_objects, process_objects
from processing import find_origin, find_areas, find_area_ratios, find_angles, find_distances
from db import insert


image_name = 'office.jpg'


# Loading Image
img = cv2.imread(f'images/{image_name}')
height, width, channels = img.shape


objects = detect_objects(img)   # Detecting objects
classIds, confidences, boxes = process_objects(
    objects, width, height)  # Extracting detected objects


# Processing the objects
def calc_objects_attr():
    areas = find_areas(boxes)
    originIndex = find_origin(boxes, areas)
    area_ratios = find_area_ratios(areas[originIndex], areas)
    distances = find_distances(boxes, originIndex)
    angles = find_angles(boxes, originIndex)

    return area_ratios, distances, angles


# Insert to Database
def insert_to_DB(area_ratios, distances, angles):
    insert({
        'area_rations': area_ratios,
        'distances': distances,
        'angles': angles,
        'image_name': image_name
    })


if len(boxes) > 0:
    area_ratios, distances, angles = calc_objects_attr()
    insert_to_DB(area_ratios, distances, angles)
else:
    insert_to_DB([], [], [])


mark_objects(img, boxes, classIds, confidences)
show(img)
