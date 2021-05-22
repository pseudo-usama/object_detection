from os import rename as move_file
from flask import Flask, render_template, redirect

# Local imports
from config import *
from detector import detect_objs
from DB import insert as insert_toDB
from DB.search import search as search_inDB
from validation import validate


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', template='default')


@app.route('/submit', methods=['POST'])
@validate
def submit(img_name, req_type):
    objs = detect_objs(img_name)

    if objs is None:
        # TODO: Image should be Deleted
        return redirect('/')

    move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)
    insert_toDB(objs)

    return redirect('/')


@app.route('/search', methods=['POST'])
@validate
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


if __name__ == '__main__':
    app.run(debug=True)
