"""
This module actually detect & process the object from image.
"""


import cv2
import numpy as np


net = cv2.dnn.readNet('detector/object_detector/yolov3-spp.weights',
                      'detector/object_detector/yolov3-spp.cfg')

layerNames = net.getLayerNames()
outputLayers = [layerNames[i[0]-1]for i in net.getUnconnectedOutLayers()]


def detect_objects(img):
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    height, width, channels = img.shape

    # Print all channels of images
    # for b in blob:
    #     for i, imgBlob in enumerate(b):
    #         cv2.imshow(str(i), imgBlob)

    net.setInput(blob)
    outs = net.forward(outputLayers)

    processed_objs = process_objects(outs, width, height)
    removed_duplicated_objs = remove_duplicated_objects(processed_objs)

    return removed_duplicated_objs


def process_objects(objects, width, height):
    detectedObjects = []
    for obj in objects:
        for detection in obj:
            scores = detection[5:]
            classId = np.argmax(scores).item()
            confidence = scores[classId]

            # TODO: have to add here constent value for confidence
            if confidence > 0.5:
                centerX = int(detection[0]*width)
                centerY = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)
                topLeft = (int(centerX-w/2), int(centerY-h/2))

                detectedObjects.append({
                    'center': (centerX, centerY),
                    'dimentions': (w, h),
                    'topLeft': topLeft,
                    'confidence': float(confidence),
                    'classId': classId
                })

    return detectedObjects


def remove_duplicated_objects(objects):
    boxes = []
    classIds = []
    confidences = []
    for obj in objects:
        boxes.append([
            int(obj['center'][0]-obj['dimentions'][0]/2),
            int(obj['center'][1]-obj['dimentions'][1]/2),
            obj['dimentions'][0],
            obj['dimentions'][1]
        ])
        classIds.append(obj['classId'])
        confidences.append(obj['confidence'])

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    remainingObjects = [obj for i, obj in enumerate(objects) if i in indexes]

    return remainingObjects


if __name__ == '__main__':
    print(
"""This is a module to detect objects from an image.
Try importing & calling detect_objects(cv2.imread(<path_to_your_image>))
And it will return the detected objects from the image.
Good luck ;)"""
)
