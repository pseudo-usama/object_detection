from math import dist, atan, degrees


def find_areas(boxes):
    areas = [box[2]*box[3] for box in boxes]

    return areas


def find_origin(boxes, areas):
    if len(boxes) == 0:
        return None

    maxAria = max(areas)
    bigBoxesIndex = [i for i, aria in enumerate(areas) if aria == maxAria]

    if len(bigBoxesIndex) == 1:
        return bigBoxesIndex[0]

    # I've to write code
    # To find the first object
    return bigBoxesIndex[0]


def find_area_ratios(origin_area, areas):
    area_ratios = [area/origin_area for area in areas]

    return area_ratios


def find_distances(boxes, originIndex):
    origin = boxes[originIndex]
    distances = [dist([box[4], box[5]], [origin[4], origin[5]])
                 for box in boxes]

    return distances


def find_angles(boxes, originIndex):
    angles = []
    
    for box in boxes:
        x = box[4]
        y = box[5]

        angle = degrees(atan(abs(y/x)))

        if x < 0 and y > 0:     # 2nd Quadrant
            angle += 90
        elif x < 0 and y < 0:   # 3rd Quandrant
            angle += 180
        elif x > 0 and y < 0:   # 4th Quandrant
            angle += 270

        angles.append(angle)

    return angles
