from pymongo import MongoClient
import os
import json

# client = MongoClient('mongodb://hans:noooz@52.59.186.178:27017/')
client = MongoClient('mongodb://hans:noooz@localhost:27017/')
imported_db = client['news']
imported_collection = imported_db['imported']

imported_news = 'imported'

all_tags = {}

items = {}

import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

for fn in os.listdir(imported_news):
    filename = os.path.join(imported_news, fn)
    if os.path.isfile(filename):
        d = None
        with open(filename, 'r') as f:
            d = json.load(f)
            # print(parse.unquote(d['text']))

        item_tags = {}
        for entity in d['item']['metadata']['entities']:
            if entity['type'] != 'XMN-TAG':
                entity_uri = entity['uri']
                print(entity['label'])
                print(entity['score'])

                # tags appear more than once on an item - we count the first one here
                if not item_tags.get(entity_uri, False):
                    item_tags[entity_uri] = entity

                    if not all_tags.get(entity_uri, False):
                        all_tags[entity_uri] = {
                            'label': entity['label'],
                            'items': [d['item']['fullText']]}
                    else:
                        all_tags[entity_uri]['items'].append(d['item']['fullText'])

                # append to item overview
                if not items.get(d['_id'], False):
                    items[d['_id']] = {'tags': item_tags,
                                       'item': d}

for tag_id, value in all_tags.items():
    print(value['label'])
    print(length(value['items']))
