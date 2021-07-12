from .zero_graphical_objs import process_and_index as process_and_index_zero_graphical_objs


def process_and_index(graphicalObjs, BBs, imgName):
    if len(graphicalObjs) == 0:
        return process_and_index_zero_graphical_objs(BBs, imgName)
