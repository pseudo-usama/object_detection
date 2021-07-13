from pymongo import MongoClient

from config import MONGO

from logger import log
LOGGER = log(__name__)



client = MongoClient(MONGO['dbUrl'])

DB = client[MONGO['client']]
COLLECTION = DB[MONGO['collection']]


def insert_to_db(data):
    COLLECTION.update_one({'_id': 1}, {'$push': data}, upsert=True)
    LOGGER.info('Data saved to DB')


def read_from_db(query):
    document = COLLECTION.find_one({'_id': 1}, query)
    if document is None:
        return None

    document.pop('_id', None)

    LOGGER.info('Data has been read from DB')
    return document
