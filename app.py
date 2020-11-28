from os import rename as move_file
from os.path import splitext as splitFileName
from uuid import uuid1
from flask import Flask, request, render_template, redirect
from config import *
from detector import detect_objs
from DB import insert as insert_toDB


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
    if objs is not None:
        # Now search in database
        # Move submited img results in DB
        # And Move img to INDEXED_IMGS_DIR
        # return results
        # return no objects detected msj
        pass


def save_file():
    img = request.files['img']
    imgName = str(uuid1())+splitFileName(img.filename)[1]
    img.save(UPLOADED_IMGS_DIR+imgName)

    return imgName


if __name__ == '__main__':
    app.run(debug=True)
