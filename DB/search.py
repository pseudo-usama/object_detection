from os import read
from nested_lookup import nested_lookup

from DB import read_objs_data, read_documents_data


def search_objs(objs, img_name):
    query = {key: True for key in objs}
    matches = read_objs_data(query)
    
    if matches is None:
        return None

    matches.pop('1', None)

    imgs = flatten(matches)
    if imgs == []:
        return None

    without_deplicats = list(dict.fromkeys(imgs))
    without_deplicats = [s for s in without_deplicats if sstr(img_name) in s]
    if len(without_deplicats) == 0:
        return None
    return without_deplicats


def search_documents(query, img_name):
    matches = read_documents_data(query)
    if matches is None:
        return None

    imgs = flatten(matches)

    if imgs == []:
        return None

    imgs = nested_lookup('imgName', imgs)
    imgs = [s for s in imgs if sstr(img_name) in s]

    if len(imgs) == 0:
        return None
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

def sstr(text):
    text = text[(text.index('--')+2):]
    return text
