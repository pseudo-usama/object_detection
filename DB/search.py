from DB import read


def search(objs):
    query = {key: True for key in objs}
    matches = read(query)
    if matches is None:
        return None

    del matches['1']
    del matches['_id']

    imgs = flatten(matches)
    if imgs == []:
        return None

    withoutDuplicats = list(dict.fromkeys(imgs))
    return withoutDuplicats


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
