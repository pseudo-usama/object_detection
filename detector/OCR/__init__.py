from detector.OCR.sub_imgs import find_sub_imgs
from detector.OCR.recognize_lines import recognize_lines

def detect_text(img):
    subImgs = find_sub_imgs(img)
    lines = find_lines_in_sub_imgs(img, subImgs)
    lines = sort_lines(lines)

    return lines


def find_lines_in_sub_imgs(img, subImgs):
    lines = []

    for x, y, w, h in subImgs:
        # Cropping the text block for giving input to OCR
        cropped = img[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        newLines = recognize_lines(cropped)
        newLines = [{**line, 'topLeft': (line['topLeft'][0]+x, line['topLeft'][1]+y)} for line in newLines]
        lines += newLines

    return lines


def sort_lines(lines):
    return sorted(lines, key=lambda line: (line['topLeft'][1], line['topLeft'][0]))
