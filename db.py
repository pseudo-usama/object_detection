import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['object_detection']
collection = db['object_detection']


def insert(data):
    collection.update_one({'_id': 1}, {'$push': data}, upsert=True)
