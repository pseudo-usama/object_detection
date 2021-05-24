from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
db = client['object_detection']

object_collection = db['object_detection']
document_collection = db['document_detection']


def insert_graphical_img_data(data):
    object_collection.update_one({'_id': 1}, {'$push': data}, upsert=True)

def insert_document_data(data):
    document_collection.update_one({'_id': 1}, {'$push': data}, upsert=True)


def read_objs_data(query):
    document = object_collection.find_one({'_id': 1}, query)
    return document

def read_documents_data(query):
    pass
