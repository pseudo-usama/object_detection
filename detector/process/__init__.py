def find_distances_to_origin(boundingBoxes, origin):
    for boundingBox in boundingBoxes:
        boundingBox.update(
            {'distance': distance(boundingBox['topLeft'], origin)}
        )


# def find_distances_to_origin(boundingBoxes):
#     for boundingBox in boundingBoxes:
#         print(boundingBox['text'])

def distance(p1, p2):
    return(p1[0]-p2[0], p1[1]-p2[1])
