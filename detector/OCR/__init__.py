from .sub_imgs import find_sub_imgs
from .recognize_lines import recognize_lines

from config import GLOBAL_DEBUG
from ..show_img import mark_bounding_box


DEBUG_MODE = GLOBAL_DEBUG and True


def detect_text(img):
    subImgs = find_sub_imgs(img)
    if DEBUG_MODE:
        # print(subImgs)
        print(len(subImgs))
        mark_bounding_box(img, subImgs)

    lines = find_lines_in_sub_imgs(img, subImgs)
    lines = sort_lines(lines)

    return lines


def find_lines_in_sub_imgs(img, subImgs):
    lines = []

    for i in range(len(subImgs)):
        x, y = subImgs[i]['pos']
        w, h = subImgs[i]['size']

        # Cropping the text block for giving input to OCR
        cropped = img[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        newLines = recognize_lines(cropped)
        newLines = [{**line, 'pos': (line['pos'][0]+x, line['pos'][1]+y)} for line in newLines]
        lines += newLines

    return lines


def sort_lines(lines):
    return sorted(lines, key=lambda line: (line['pos'][1], line['pos'][0]))
