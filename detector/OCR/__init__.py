import pytesseract
from pytesseract import Output
import cv2
from config import *


def detect_text(img):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])

    texts = []

    for i in range(n_boxes):
        if OCR_MIN_THRESHOLD <= float(d['conf'][i]) and d['text'][i].strip() != '':
            texts.append({
                'topLeft': (d['left'][i], d['top'][i]),
                'dimensions': (d['width'][i], d['height'][i]),
                'text': d['text'][i]
            })

    return texts
