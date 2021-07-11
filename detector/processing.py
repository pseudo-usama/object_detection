from math import atan, degrees, sqrt

from numpy import true_divide

def dist(p1, p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def find_areas(objects):
    for obj in objects:
        obj.update({'area': obj['size'][0]*obj['size'][1]})


def sort_wrt_area(objects):
    # Here we are sorting the object
    # W.R.T Area. If area is equal then
    # W.R.T its pos corner
    sortedObjects = sorted(objects, reverse=True, key=lambda obj:
                           (obj['area'], -obj['pos'][1], -obj['pos'][0]))

    return sortedObjects


def find_area_ratios(objects):
    originObjectArea = objects[0]['area']
    for obj in objects:
        obj.update({'areaRatio': obj['area']/originObjectArea})


def find_distances(objects):
    obj1 = {}
    obj1['width'] = objects[0]['size'][0]
    obj1['height'] = objects[0]['size'][1]
    obj1['pos'] = objects[0]['pos']
    obj1['topRight'] = (obj1['pos'][0]+obj1['width'], obj1['pos'][1])
    obj1['bottomLeft'] = (obj1['pos'][0], obj1['pos'][1]+obj1['height'])
    obj1['bottomRight'] = (obj1['pos'][0]+obj1['width'], obj1['pos'][1]+obj1['height'])

    obj2 = {}
    obj2['width'] = objects[1]['size'][0]
    obj2['height'] = objects[1]['size'][1]
    obj2['pos'] = objects[1]['pos']
    obj2['topRight'] = (obj2['pos'][0]+obj2['width'], obj2['pos'][1])
    obj2['bottomLeft'] = (obj2['pos'][0], obj2['pos'][1]+obj2['height'])
    obj2['bottomRight'] = (obj2['pos'][0]+obj2['width'], obj2['pos'][1]+obj2['height'])

    posDistance = distance(obj1['pos'], obj2['pos'])
    bottomRightDistance = distance(obj1['bottomRight'], obj2['bottomRight'])
    first_distance_ratio = posDistance / bottomRightDistance

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
