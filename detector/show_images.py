import cv2
import numpy as np


def show(img, objects=None):
    if objects is not None:
        mark_objects(img, objects)

    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def mark_objects(img, objects):
    for i, obj in enumerate(objects):
        label = classes[obj['classId']]

        bottomRight = (obj['topLeft'][0]+obj['dimentions'][0],
                       obj['topLeft'][1]+obj['dimentions'][1])
        topLeft = obj['topLeft']
        cv2.rectangle(img, topLeft, bottomRight, colors[i], 2)
        cv2.putText(img, label, topLeft,
                    cv2.FONT_HERSHEY_PLAIN, 3, colors[i], 3)


# Reading the class names
classes = []
with open('detector/coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
# Defining different colors for each class
colors = np.random.uniform(0, 255, size=(len(classes), 3))
