from DB import read_objs_data, read_documents_data


def search_objs(objs):
    query = {key: True for key in objs}
    matches = read_objs_data(query)
    if matches is None:
        return None

    del matches['1']
    del matches['_id']

    imgs = flatten(matches)
    if imgs == []:
        return None

    withoutDuplicats = list(dict.fromkeys(imgs))
    return withoutDuplicats


def search_documents():
    pass


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
