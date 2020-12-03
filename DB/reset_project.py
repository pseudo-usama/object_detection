"""
This drops the database.
And delete all indexed images.
"""

from pymongo import MongoClient
import os


def drop_database():
    client = MongoClient('mongodb://localhost:27017')
    client.drop_database('object_detection')


def delete_indexed_imgs():
    files = os.listdir('static/indexed-images/')
    files.remove('.gitignore')
    for file in files:
        os.remove('static/indexed-images/'+file)


if __name__ == "__main__":
    drop_database()
    delete_indexed_imgs()
    print('Success!')
