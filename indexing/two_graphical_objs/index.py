from math import ceil

from DB.schema import *


def index_data(graphicalObjs, BBs, imgName):
    indexed = {}

    nthAngleObj = ceil(graphicalObjs['angle'] / ANGLE_RATIO_RANGE)
    nthDistanceRatioObj = ceil(graphicalObjs['distanceRatio'] / DISTANCE_RATIO_RANGE)

    noOfSBB = len(BBs['SBBs'])
    noOfDBB = len(BBs['DBBs'])

    indexed[f'2.{nthAngleObj}.{nthDistanceRatioObj}.{noOfSBB}.{noOfDBB}'] = {
        'SBBs': BBs['SBBs'],
        'DBBs': BBs['DBBs'],
        'img': imgName
    }

    return indexed
