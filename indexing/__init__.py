from .zero_graphical_objs import process_and_index as process_and_index_zero_graphical_objs
from .one_graphical_obj import process_and_index as process_and_index_one_graphical_obj


def process_and_index(graphicalObjs, BBs, imgName):
    if len(graphicalObjs) == 0:
        return process_and_index_zero_graphical_objs(BBs, imgName)
    elif len(graphicalObjs) == 1:
        return process_and_index_one_graphical_obj(graphicalObjs[0], BBs, imgName)
