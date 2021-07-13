from .zero_graphical_objs import process_and_index as process_and_index_zero_graphical_objs
from .one_graphical_obj import process_and_index as process_and_index_one_graphical_obj
from .two_graphical_objs import process_and_index as process_and_index_two_graphical_objs

from logger import log
LOGGER = log(__name__)


def process_and_index(graphicalObjs, BBs, imgName):
    indexedData = None
    
    if len(graphicalObjs) == 0:
        indexedData = process_and_index_zero_graphical_objs(BBs, imgName)
    elif len(graphicalObjs) == 1:
        indexedData = process_and_index_one_graphical_obj(graphicalObjs[0], BBs, imgName)
    elif len(graphicalObjs) == 2:
        indexedData = process_and_index_two_graphical_objs(graphicalObjs, BBs, imgName)
    else:
        pass

    LOGGER.info('Data has been indexed')
    return indexedData
