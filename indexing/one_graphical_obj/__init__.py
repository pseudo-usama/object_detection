from .graphical import process as process_graphical
from .index import index_data


def process_and_index(obj, BBs, imgName):
    processedGraphicalObj = process_graphical(obj)
    indexed = index_data(processedGraphicalObj, BBs, imgName)

    return indexed
