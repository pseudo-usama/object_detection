# How to run
- First of all download the weights file from [here](https://pjreddie.com/media/files/yolov3-spp.weights). And place it [detector/object_detector](detector/object_detector)
- And install [tesseract-ocr](https://github.com/tesseract-ocr/tesseract) & [mongoDB](https://www.mongodb.com).
- Then install dependencies:
  - Using conda `conda env create -f requirements-conda.yml`
  - Using pip `pip install -r requirements-pip.txt`
- After this run the [app.py](app.py) file. And open localhost:port on your browser.

# Interface
![Image](images/project/interface.jpg)
