from os.path import splitext as splitFileName
from functools import wraps
from subprocess import call
from flask import request
from flask_api.status import HTTP_400_BAD_REQUEST
from uuid import uuid1

# Local imports
from config import *


def validate_new_img_req(callback):
    @wraps(callback)
    def validate_and_save_img(*args, **kwargs):
        if 'img' not in request.files:
            return BAD_REQUEST('Add an image'), HTTP_400_BAD_REQUEST
        elif 'img-type' not in request.form:
            return BAD_REQUEST('Select some image type'), HTTP_400_BAD_REQUEST

        req_type = request.form['img-type']
        img_file = request.files['img']
        if req_type != 'image' and req_type != 'document':
            return BAD_REQUEST("Image type can only be 'image' or 'document'"), HTTP_400_BAD_REQUEST

        img_name = save_file(img_file)

        return callback(img_name, req_type, *args, **kwargs)
    return validate_and_save_img


def save_file(img):
    img_name = str(uuid1())+splitFileName(img.filename)[1]
    img.save(UPLOADED_IMGS_DIR+img_name)

    return img_name


def validate_bounding_boxes_selector_req(callback):
    wraps(callback)

    def validate_bounding_boxes_form(*args, **kwargs):
        if 'img-name' not in request.form:
            return BAD_REQUEST('Image name not found.')
        elif 'bounding-boxes-data' not in request.form:
            return BAD_REQUEST('No bounding boxes data found.')

        img_name = request.form['img-name']
        bounding_boxes_data = request.form['bounding-boxes-data']

        return callback(img_name, bounding_boxes_data, *args, **kwargs)
    return validate_bounding_boxes_form


def BAD_REQUEST(msj=''):
    return f'<h1>Bad request</h1><p>{msj}</p>'
