from math import dist, atan, degrees


def find_areas(objects):
    for obj in objects:
        obj.update({'area': obj['dimentions'][0]*obj['dimentions'][1]})


def sort_wrt_area(objects):
    # Here we are sorting the object
    # W.R.T Area
    # If area is equal then
    # W.R.T its topLeft corner
    sortedObjects = sorted(objects, key=lambda obj:
                           (obj['area'], obj['topLeft'][1], obj['topLeft'][0]))

    return sortedObjects


def find_area_ratios(objects):
    originObjectArea = objects[0]['area']
    areaRatios = [obj['area']/originObjectArea for obj in objects]
    return areaRatios


def find_distances(objects):
    originObjectCenter = objects[0]['center']
    distances = [dist(obj['center'], originObjectCenter)
                 for obj in objects]

    return distances


def find_angles(objects):
    angles = []

    for obj in objects:
        x = obj['center'][0]
        y = obj['center'][1]
        angle = degrees(atan(abs(y/x)))

        if x < 0 and y > 0:     # 2nd Quadrant
            angle = 180 - angle
        elif x < 0 and y < 0:   # 3rd Quandrant
            angle += 180
        elif x > 0 and y < 0:   # 4th Quandrant
            angle = 360 - angle

        angles.append(angle)

    return angles
