from math import ceil

from DB.schema import *


def index_data(BBs, imgName):
    indexed = {}

    noOfSBB = len(BBs['SBBs'])
    noOfDBB = len(BBs['DBBs'])

    indexed[f'0.{noOfSBB}.{noOfDBB}'] = {
        'SBBs': BBs['SBBs'],
        'DBBs': BBs['DBBs'],
        'img': imgName
    }

    return indexed
