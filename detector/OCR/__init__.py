import pytesseract
from pytesseract import Output
from config import *


def detect_text(img):
    detected_texts = pytesseract.image_to_data(img, output_type=Output.DICT)

    bounding_boxes = process_texts_data(detected_texts)
    return bounding_boxes


def process_texts_data(texts):
    bounding_boxes = []

    n_boxes = len(texts['level'])
    for i in range(n_boxes):
        if OCR_MIN_THRESHOLD <= float(texts['conf'][i]) and texts['text'][i].strip() != '':
            bounding_boxes.append({
                'topLeft': (texts['left'][i], texts['top'][i]),
                'dimensions': (texts['width'][i], texts['height'][i]),
                'text': texts['text'][i],
                'conf': texts['conf'][i]
            })

    return bounding_boxes
