from pymongo import MongoClient
import os
import json

client = MongoClient('mongodb://localhost:27017/')
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
            news_id = imported_collection.insert(d)
            print('inserted %s' % news_id)

