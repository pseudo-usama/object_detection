from flask import Flask, request, render_template
from config import *
from detector import detect_objs
from DB import insert as insert_toDB


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    img = request.files['img']
    img.save(f'{UPLOADED_IMGS_DIR}/{img.filename}')
    objs = detect_objs(img.filename)
    if objs is not None:
        insert_toDB(objs)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
