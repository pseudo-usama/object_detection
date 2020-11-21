import cv2
import numpy as np


def show(img):
    img = cv2.resize(img, None, fx=1, fy=1)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# Class names
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


def mark_objects(img, boxes, classIds, confidences):
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h, centerX, centerY = boxes[i]
            label = classes[classIds[i]]

            cv2.rectangle(img, (x, y), (x+w, y+h), colors[i], 2)
            cv2.putText(img, label, (x, y+30),
                        cv2.FONT_HERSHEY_PLAIN, 3, colors[i], 3)
