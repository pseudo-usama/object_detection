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

    # Image type document
    objs, bbs = document_detertor(img_name)
    move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)
    print(type(objs), type(bbs))
    return render_template(
        'index.html',
        template='document-bounding-boxes-selector',
        img={ 'name': img_name, 'path': INDEXED_IMGS_DIR },
        bounding_boxes=json.dumps(bbs),
        objs=json.dumps(objs)
    )


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
