import cv2
import numpy as np


net = cv2.dnn.readNet('object_detection/yolov3-spp.weights',
                      'object_detection/yolov3-spp.cfg')

layerNames = net.getLayerNames()
outputLayers = [layerNames[i[0]-1]for i in net.getUnconnectedOutLayers()]


def detect_objects(img):
    blob = cv2.dnn.blobFromImage(
        img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Print all channels of images
    # for b in blob:
    #     for i, imgBlob in enumerate(b):
    #         cv2.imshow(str(i), imgBlob)

    net.setInput(blob)
    outs = net.forward(outputLayers)

    return outs


def process_objects(objects, width, height):
    classIds = []
    confidences = []
    boxes = []
    for obj in objects:
        for detection in obj:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]

            if confidence > 0.5:
                centerX = int(detection[0]*width)
                centerY = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                topLeftX = int(centerX-w/2)
                topLeftY = int(centerY-h/2)
                # bottomRight = (int(centerX+w/2), int(centerY+h/2))

                boxes.append([topLeftX, topLeftY, w, h, centerX, centerY])
                confidences.append(float(confidence))
                classIds.append(classId)

    return classIds, confidences, boxes
