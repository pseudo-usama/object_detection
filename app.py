from os import rename as move_file
from flask import Flask, render_template, redirect
import json

# Local imports
from config import *
from detector import detect_objs, document_detertor, index_document_data, index_bounding_boxes
from DB import insert_graphical_img_data, insert_document_data
from DB.search import search_objs as search_objs_in_db, search_documents as search_documents_in_db
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
    insert_graphical_img_data(objs)

    return redirect('/')


# Document user only submit a document
@app.route('/submit-document', methods=['POST'])
@validate_submit_search_form
def document_submit(img_name):
    objs, bbs = document_detertor(img_name)

    if objs is None or bbs is None:
        return send_respose('no-bb-or-objs')
    
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
def img_search(img_name):
    returned = detect_objs(img_name, add_deviation=True)

    if returned is None:
        # TODO: The image should be deleted
        return send_respose('no_img_found')

    objs, objs_for_search = returned

    imgs = search_objs_in_db(objs_for_search, img_name)

    move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)
    insert_graphical_img_data(objs)

    if imgs is None:
        return send_respose('no_img_found')

    imgs = [INDEXED_IMGS_DIR+img for img in imgs]
    return send_respose('gallary', imgs=imgs)


# When user request to verify document
@app.route('/search-document', methods=['POST'])
@validate_submit_search_form
def document_search(img_name):
    objs, bbs = document_detertor(img_name)

    if objs is None or bbs is None:
        # TODO: Case for 0 or 1 objs
        # TODO: The image should be deleted
        return send_respose('no_img_found')

    indexed = index_bounding_boxes(objs, True, len(bbs), add_deviation=True)
    imgs = search_documents_in_db(indexed, img_name)
    # print(indexed)
    if imgs is None:
        return send_respose('no_img_found')

    imgs = [INDEXED_IMGS_DIR+img for img in imgs]
    return send_respose('gallary', imgs=imgs)


# When user submit document template
# Then server send the bounding boxes to client to select types of bounding boxes
# This route used only when user submits types of bounding boxes
@app.route('/document-bounding-boxes-selector', methods=['POST'])
@validate_bounding_boxes_selector_form
def save_template(img_name, objs, bounding_boxes):
    toDB = index_document_data(img_name, objs, bounding_boxes)
    insert_document_data(toDB)
    return redirect('/')


def send_respose(template, *args, **kwargs):
    return render_template('index.html', template=template, *args, **kwargs)


if __name__ == '__main__':
    print(f'\n{" "*10}*'*5)
    app.run(debug=True)
