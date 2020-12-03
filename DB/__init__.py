from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
db = client['object_detection']
collection = db['object_detection']


def insert(data):
    collection.update_one({'_id': 1}, {'$push': data}, upsert=True)


def read(query):
    document = collection.find_one({'_id': 1}, query)
    return document
