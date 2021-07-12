from pymongo import MongoClient

from config import MONGO


client = MongoClient(MONGO['DB_URL'])

DB = client[MONGO['CLIENT']]
COLLECTION = DB[MONGO['COLLECTION']]


def insert_to_db(data):
    COLLECTION.update_one({'_id': 1}, {'$push': data}, upsert=True)


def read_from_db(query):
    document = COLLECTION.find_one({'_id': 1}, query)
    if document is None:
        return None

    document.pop('_id', None)
    return document
