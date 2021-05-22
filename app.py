from os import rename as move_file
from flask import Flask, render_template, redirect
import json

# Local imports
from config import *
from detector import detect_objs, document_detertor
from DB import insert as insert_toDB
from DB.search import search as search_inDB
from validation import validate_new_img_req, validate_bounding_boxes_selector_req


app = Flask(__name__)


# Index page
@app.route('/')
def index():
    return render_template('index.html', template='default')
    # return render_template('index.html', template='document-bounding-boxes-selector', img_name='6dbf3c8d-baf4-11eb-883f-6c2b5950783c.jpg', img_path=INDEXED_IMGS_DIR+'6dbf3c8d-baf4-11eb-883f-6c2b5950783c.jpg', bounding_boxes=json.dumps([{'topLeft': (1076, 424), 'dimensions': (136, 84), 'text': 'This', 'distance': (912, 187)}, {'topLeft': (1260, 432), 'dimensions': (43, 63), 'text': 'is', 'distance': (1096, 195)}, {'topLeft': (1338, 428), 'dimensions': (325, 67), 'text': 'first', 'distance': (1174, 191)}, {'topLeft': (1527, 424), 'dimensions': (140, 84), 'text': 'text', 'distance': (1363, 187)}, {'topLeft': (55, 1128), 'dimensions': (124, 85), 'text': 'And', 'distance': (-109, 891)}, {'topLeft': (221, 1128), 'dimensions': (225, 85), 'text': "that's", 'distance': (57, 891)}, {'topLeft': (483, 1128), 'dimensions': (211, 85), 'text': 'second', 'distance': (319, 891)}, {'topLeft': (752, 1133), 'dimensions': (157, 66), 'text': 'line', 'distance': (588, 896)}, {'topLeft': (1754, 1207), 'dimensions': (67, 52), 'text': '(7', 'distance': (1590, 970)}, {'topLeft': (1127, 1287), 'dimensions': (126, 58), 'text': '——', 'distance': (963, 1050)}, {'topLeft': (1358, 1170), 'dimensions': (304, 180), 'text': 'oe', 'distance': (1194, 933)}, {'topLeft': (1694, 1214), 'dimensions': (103, 87), 'text': 'a!', 'distance': (1530, 977)}, {'topLeft': (1798, 1213), 'dimensions': (139, 101), 'text': 'me', 'distance': (1634, 976)}]))


# When user only submits a image/document
@app.route('/submit', methods=['POST'])
@validate_new_img_req
def submit(img_name, req_type):
    if req_type == 'image':
        objs = detect_objs(img_name)

        if objs is None:
            # TODO: Image should be Deleted
            return redirect('/')

        move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)
        insert_toDB(objs)

        return redirect('/')

    if req_type == 'document':
        objs, bbs = document_detertor(img_name)
        move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)
        return render_template('index.html', template='document-bounding-boxes-selector', img_name=img_name, img_path=INDEXED_IMGS_DIR+img_name, bounding_boxes=json.dumps(bbs))


# When user search for image/document
@app.route('/search', methods=['POST'])
@validate_new_img_req
def search(img_name, img_type):
    objs = detect_objs(img_name)

    if objs is None:
        return render_template('index.html', template='no_img_found')

    imgs = search_inDB(objs)
    move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)
    insert_toDB(objs)

    if imgs is None:
        return render_template('index.html', template='no_img_found')

    imgs = [INDEXED_IMGS_DIR+img for img in imgs]
    return render_template('index.html', template='gallary', imgs=imgs)


# When user enter document template
# This route used only after submitting of document
@app.route('/document-bounding-boxes-selector', methods=['POST'])
@validate_bounding_boxes_selector_req
def save_template(img_name, bounding_boxes_data):
    print(img_name)
    print(bounding_boxes_data)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
