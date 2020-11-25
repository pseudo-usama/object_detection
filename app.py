from flask import Flask, request, render_template
from config import *
from detector import detect_objs


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    img = request.files['img']
    img.save(f'{UPLOADED_IMGS_DIR}/{img.filename}')
    detect_objs(img.filename)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
