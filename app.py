from os import rename as move_file
from flask import Flask, render_template, redirect
import json

# Local imports
from config import *
from detector import detect_objs, document_detertor
from DB import insert as insert_toDB
from DB.search import search as search_inDB
from validation import validate_submit_search_form, validate_bounding_boxes_selector_form


app = Flask(__name__)


# Index page
@app.route('/')
def index():
    return send_respose('default')


# When user only submits a image
@app.route('/submit-image', methods=['POST'])
@validate_submit_search_form
def img_submit(img_name):
    objs = detect_objs(img_name)

    if objs is None:
        # TODO: Image should be Deleted
        return redirect('/')

    move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)
    insert_toDB(objs)

    return redirect('/')


# Document user only submit a document
@app.route('/submit-document', methods=['POST'])
@validate_submit_search_form
def document_submit(img_name):
    objs, bbs = document_detertor(img_name)
    move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)

    return send_respose(
        template='document-bounding-boxes-selector',
        img={ 'name': img_name, 'path': INDEXED_IMGS_DIR },
        bounding_boxes=json.dumps(bbs),
        objs=json.dumps(objs)
    )


# When user search for image
@app.route('/search-image', methods=['POST'])
@validate_submit_search_form
def search(img_name):
    objs = detect_objs(img_name)

    if objs is None:
        return send_respose('no_img_found')

    imgs = search_inDB(objs)
    move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)
    insert_toDB(objs)

    if imgs is None:
        return send_respose('no_img_found')

    imgs = [INDEXED_IMGS_DIR+img for img in imgs]
    return send_respose('gallary', imgs=imgs)


@app.route('/search-document', methods=['POST'])
@validate_submit_search_form
def document_search(img_name):
    return 'asdf'


# When user enter document template
# This route used only after submitting of document
@app.route('/document-bounding-boxes-selector', methods=['POST'])
@validate_bounding_boxes_selector_form
def save_template(img_name, bounding_boxes_data):
    print(img_name)
    print(bounding_boxes_data)

    return redirect('/')


def send_respose(template, *args, **kwargs):
    return render_template('index.html', template=template, *args, **kwargs)


if __name__ == '__main__':
    app.run(debug=True)
