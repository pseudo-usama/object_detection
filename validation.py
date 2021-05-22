from os.path import splitext as splitFileName
from functools import wraps
from flask import request
from flask_api.status import HTTP_400_BAD_REQUEST
from uuid import uuid1

# Local imports
from config import *


def validate(callback):
    @wraps(callback)
    def chk_img_type_and_save(*args, **kwargs):
        if 'img' not in request.files:
            return """<h1>Bad request 400</h1><p>Add an image</p>""", HTTP_400_BAD_REQUEST
        elif 'img-type' not in request.form:
            return """<h1>Bad request 400</h1><p>Select some image type</p>""", HTTP_400_BAD_REQUEST

        req_type = request.form['img-type']
        img_file = request.files['img']
        if req_type != 'image' and req_type != 'document':
            return """<h1>Bad request 400</h1><p>Image type can only be 'image' or 'document'</p>""", HTTP_400_BAD_REQUEST

        img_name = save_file(img_file)

        return callback(img_name, req_type, *args, **kwargs)
    return chk_img_type_and_save


def save_file(img):
    img_name = str(uuid1())+splitFileName(img.filename)[1]
    img.save(UPLOADED_IMGS_DIR+img_name)

    return img_name
