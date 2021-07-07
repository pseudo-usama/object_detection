from math import atan, degrees, sqrt

from numpy import true_divide

def dist(p1, p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


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
    obj1 = {}
    obj1['width'] = objects[0]['dimentions'][0]
    obj1['height'] = objects[0]['dimentions'][1]
    obj1['topLeft'] = objects[0]['topLeft']
    obj1['topRight'] = (obj1['topLeft'][0]+obj1['width'], obj1['topLeft'][1])
    obj1['bottomLeft'] = (obj1['topLeft'][0], obj1['topLeft'][1]+obj1['height'])
    obj1['bottomRight'] = (obj1['topLeft'][0]+obj1['width'], obj1['topLeft'][1]+obj1['height'])

    obj2 = {}
    obj2['width'] = objects[1]['dimentions'][0]
    obj2['height'] = objects[1]['dimentions'][1]
    obj2['topLeft'] = objects[1]['topLeft']
    obj2['topRight'] = (obj2['topLeft'][0]+obj2['width'], obj2['topLeft'][1])
    obj2['bottomLeft'] = (obj2['topLeft'][0], obj2['topLeft'][1]+obj2['height'])
    obj2['bottomRight'] = (obj2['topLeft'][0]+obj2['width'], obj2['topLeft'][1]+obj2['height'])

    topLeftDistance = distance(obj1['topLeft'], obj2['topLeft'])
    bottomRightDistance = distance(obj1['bottomRight'], obj2['bottomRight'])
    first_distance_ratio = topLeftDistance / bottomRightDistance

    topRightDistance = distance(obj1['topRight'], obj2['topRight'])
    bottomLeftDistance = distance(obj1['bottomLeft'], obj2['bottomLeft'])
    second_distance_ratio = topRightDistance / bottomLeftDistance

    final_distance_ratio = first_distance_ratio / second_distance_ratio

    return final_distance_ratio


def find_angles(objects):
    x = objects[0]['center'][0] - objects[1]['center'][0]
    y = objects[0]['center'][1] - objects[1]['center'][1]

    angle = degrees(atan(abs(y/x)))

    if x < 0 and y > 0:     # 2nd Quadrant
        angle = 180 - angle
    elif x < 0 and y < 0:   # 3rd Quandrant
        angle += 180
    elif x > 0 and y < 0:   # 4th Quandrant
        angle = 360 - angle

    return angle


def distance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**(1/2)
