from os import read
from nested_lookup import nested_lookup

from DB import read_objs_data, read_documents_data


def search_objs(objs):
    query = {key: True for key in objs}
    matches = read_objs_data(query)
    if matches is None:
        return None

    del matches['1']

    imgs = flatten(matches)
    if imgs == []:
        return None

    without_deplicats = list(dict.fromkeys(imgs))
    return without_deplicats


def search_documents(query):
    matches = read_documents_data(query)
    if matches is None:
        return None

    imgs = flatten(matches)

    if imgs == []:
        return None

    imgs = nested_lookup('imgName', imgs)
    return imgs


def flatten(mydict):
    values = []
    for val in mydict.values():
        if isinstance(val, dict):
            values += flatten(val)
        elif isinstance(val, list):
            values += val
        else:
            values.append(val)

    return values
