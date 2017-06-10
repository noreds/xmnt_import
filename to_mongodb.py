from pymongo import MongoClient
from pymongo import errors as pymongo_errors
import os
import json

client = MongoClient('mongodb://hans:noooz@52.59.186.178:27017/')
#client = MongoClient('mongodb://hans:noooz@localhost:27017/')
imported_db = client['news']
imported_collection = imported_db['imported']

imported_news = 'imported'

for fn in os.listdir(imported_news):
    filename = os.path.join(imported_news, fn)
    if os.path.isfile(filename):
        d = None
        with open(filename, 'r') as f:
            d = json.load(f)
            #print(parse.unquote(d['text']))

        if d:
            send = True
            try:
                news_id = imported_collection.insert(d, check_keys=False)
                print('inserted %s' % d['_id'])
            except pymongo_errors.DuplicateKeyError:
                print('item %s exists' % d['_id'])


