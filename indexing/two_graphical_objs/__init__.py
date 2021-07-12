from .graphical import process as process_graphical
from .index import index_data


def process_and_index(objs, BBs, imgName):
    processedGraphicalObjs = process_graphical(objs)
    indexed = index_data(processedGraphicalObjs, BBs, imgName)

    return indexed
