from DB import read


def search(objs):
    db = read()
    if db is None:
        return None

    data = extract_similar_valued_imgs(db, objs)
    if data == {}:
        return None

    imgs = flatten(data)
    withoutDuplicats = list(dict.fromkeys(imgs))
    return withoutDuplicats


def extract_similar_valued_imgs(originalDict, refDict):
    ret = {}
    for key, subdict in refDict.items():
        if key in originalDict:
            if not isinstance(originalDict[key], dict):
                # we found a value so don't keep recursing
                ret[key] = originalDict[key]
            else:
                # found another dict so merge subdicts
                merged = extract_similar_valued_imgs(
                    originalDict[key], subdict)
                if len(merged) > 0:
                    ret[key] = merged
    return ret


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
