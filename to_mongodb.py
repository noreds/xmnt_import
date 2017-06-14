from pymongo import MongoClient
from pymongo import errors as pymongo_errors
import os
import json

settings = json.load(open('settings.json'))
client = MongoClient('mongodb://'+settings['mongo']['url']+':27017/')

imported_news = 'imported'

# if news doesn't exist create news
try:
    client['news']
except IndexError:
    client['news'].create_database('news')

imported_db = client['news']

# if imported doesn't exist create news
try:
    imported_db[imported_news]
except IndexError:
    imported_db[imported_news].create_collection(imported_news)

imported_collection = imported_db[imported_news]

for fn in os.listdir(imported_news):
    filename = os.path.join(imported_news, fn)
    if os.path.isfile(filename):
        d = None
        with open(filename, 'r') as f:
            d = json.load(f)
            #print(parse.unquote(d['text']))

        if d:
            send = True
            news_id = imported_collection.insert(d, check_keys=False)
            print('inserted %s' % d['_id'])


