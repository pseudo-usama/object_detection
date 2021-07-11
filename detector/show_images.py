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

    scale_factor = min(
        1000 / img.shape[0],
        1000 / img.shape[1]
    )

    img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Marks the given objects
def mark_objects(img, objects):
    for i, obj in enumerate(objects):
        label = classes[obj['classId']]

        bottomRight = (obj['pos'][0]+obj['size'][0],
                       obj['pos'][1]+obj['size'][1])
        pos = obj['pos']
        cv2.rectangle(img, pos, bottomRight, colors[i], 2, 500)
        cv2.putText(img, label, pos,
                    cv2.FONT_HERSHEY_PLAIN, 3, colors[i], 3)


# Marks the given texts
def mark_texts(img, texts):
    for text in texts:
        bottomRight = (text['pos'][0]+text['size']
                       [0], text['pos'][1]+text['size'][1])
        cv2.rectangle(img, text['pos'], bottomRight, (0, 255, 0), 2)


# Reading the class names
classes = []
with open('detector/coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
# Defining different colors for each class
colors = np.random.uniform(0, 255, size=(len(classes), 3))
