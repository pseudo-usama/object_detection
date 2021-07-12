UPLOADED_IMGS_DIR = 'images/client/'
INDEXED_IMGS_DIR = 'images/indexed/'


OPEN_CV_MIN_THRESHOLD = 0.5     # Out of 1
OCR_MIN_THRESHOLD = 80          # Out of 100


MONGO = {
    'dbUrl': 'mongodb://localhost:27017',
    'client': 'image-based-search-engine',
    'collection': 'indexed-data'
}
