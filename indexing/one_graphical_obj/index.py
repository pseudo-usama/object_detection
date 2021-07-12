from DB.schema import *


def index_data(graphicalObj, BBs, imgName):
    indexed = {}

    nthWidthHeightRatioObj = graphicalObj['widthHeightRatio']

    noOfSBB = len(BBs['SBBs'])
    noOfDBB = len(BBs['DBBs'])

    indexed[f'1.{nthWidthHeightRatioObj}.{noOfSBB}.{noOfDBB}'] = {
        'SBBs': BBs['SBBs'],
        'DBBs': BBs['DBBs'],
        'img': imgName
    }

    return indexed
