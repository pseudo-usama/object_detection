from math import dist, atan, degrees


def find_areas(objects):
    for obj in objects:
        obj.update({'area': obj['dimentions'][0]*obj['dimentions'][1]})


def sort_wrt_area(objects):
    # Here we are sorting the object
    # W.R.T Area. If area is equal then
    # W.R.T its topLeft corner
    sortedObjects = sorted(objects, reverse=True, key=lambda obj:
                           (obj['area'], -obj['topLeft'][1], -obj['topLeft'][0]))

    return sortedObjects


def find_area_ratios(objects):
    originObjectArea = objects[0]['area']
    for obj in objects:
        obj.update({'areaRatio': obj['area']/originObjectArea})


def find_distances(objects):
    if len(objects) < 2:
        return

    # Distance between two largest objects
    originObjectCenter = objects[0]['center']
    distance = dist(originObjectCenter, objects[1]['center'])

    for obj in objects[2:]:
        obj.update({'distanceRatio':
                    dist(obj['center'], originObjectCenter)/distance})


def find_angles(objects):
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

        obj.update({'angle': angle})
