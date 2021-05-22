# These function are just for debugging purposes


import cv2
import numpy as np


# This function marks detected obecjs & texts
# And show in a window
def show(img, objects=None, texts=None):
    if objects is not None:
        mark_objects(img, objects)
    if texts is not None:
        mark_texts(img, texts)

    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Marks the given objects
def mark_objects(img, objects):
    for i, obj in enumerate(objects):
        label = classes[obj['classId']]

        bottomRight = (obj['topLeft'][0]+obj['dimentions'][0],
                       obj['topLeft'][1]+obj['dimentions'][1])
        topLeft = obj['topLeft']
        cv2.rectangle(img, topLeft, bottomRight, colors[i], 2)
        cv2.putText(img, label, topLeft,
                    cv2.FONT_HERSHEY_PLAIN, 3, colors[i], 3)


# Marks the given texts
def mark_texts(img, texts):
    for text in texts:
        bottomRight = (text['topLeft'][0]+text['dimensions']
                       [0], text['topLeft'][1]+text['dimensions'][1])
        cv2.rectangle(img, text['topLeft'], bottomRight, (0, 255, 0), 2)


# Reading the class names
classes = []
with open('detector/coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
# Defining different colors for each class
colors = np.random.uniform(0, 255, size=(len(classes), 3))
