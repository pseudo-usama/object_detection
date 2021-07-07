from math import ceil
from DB.schema import *


def index(graphicalObjs, sbb, dbb, imgName):
    indexed = {}

    nthAngleObj = ceil(graphicalObjs['angle'] / ANGLE_RATIO_RANGE)
    nthDistanceRatioObj = ceil(graphicalObjs['distanceRatio'] / DISTANCE_RATIO_RANGE)

    noOfSBB = len(sbb)
    noOfDBB = len(dbb)

    indexed[f'{nthAngleObj}.{nthDistanceRatioObj}.{noOfSBB}.{noOfDBB}'] = {
        'sbb': sbb,
        'dbb': dbb
    }

    return indexed
