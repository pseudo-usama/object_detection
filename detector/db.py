import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['object_detection']
collection=db['object_detection']


def insert(data):
    collection.insert_one(data)
