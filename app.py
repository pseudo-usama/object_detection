from os import rename as move_file
from os.path import splitext as splitFileName
from uuid import uuid1
from flask import Flask, request, render_template, redirect
from config import *
from object_detector import detect_objs
from DB import insert as insert_toDB
from DB.search import search as search_inDB


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', data={'error': 'no_data_and_error'})


@app.route('/submit', methods=['POST'])
def submit():
    imgName = save_file()
    objs = detect_objs(imgName)
    if objs is not None:
        move_file(UPLOADED_IMGS_DIR+imgName, INDEXED_IMGS_DIR+imgName)
        insert_toDB(objs)

    return redirect('/')


@app.route('/search', methods=['POST'])
def search():
    imgName = save_file()
    objs = detect_objs(imgName)

    if objs is None:
        return render_template('index.html', data={'error': 'no_img_found'})

    imgs = search_inDB(objs)
    move_file(UPLOADED_IMGS_DIR+imgName, INDEXED_IMGS_DIR+imgName)
    insert_toDB(objs)

    if imgs is None:
        return render_template('index.html', data={'error': 'no_img_found'})

    return render_template('index.html', data={'error': '', 'imgs': [INDEXED_IMGS_DIR+img for img in imgs]})


def save_file():
    img = request.files['img']
    imgName = str(uuid1())+splitFileName(img.filename)[1]
    img.save(UPLOADED_IMGS_DIR+imgName)

    return imgName


if __name__ == '__main__':
    app.run(debug=True)
