from pymongo import MongoClient
import os
import json

# client = MongoClient('mongodb://hans:noooz@52.59.186.178:27017/')
client = MongoClient('mongodb://hans:noooz@localhost:27017/')
imported_db = client['news']
imported_collection = imported_db['imported']

imported_news = 'imported'

all_tags_with_items = {}

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

                    if not all_tags_with_items.get(entity_uri, False):
                        all_tags_with_items[entity_uri] = {
                            'label': entity['label'],
                            'items': [d['item']['fullText']]}
                    else:
                        all_tags_with_items[entity_uri]['items'].append(d['item']['fullText'])

                # append to item overview
                if not items.get(d['_id'], False):
                    items[d['_id']] = {'tags': item_tags,
                                       'item': d}

from numpy import array
from scipy.cluster.vq import vq, kmeans, whiten

all_bin_tags = []

for item in items.values():
    #print(item)
    binary_tags = [1 if x in item['tags'] else 0 for x in all_tags_with_items.keys()]
    #print(binary_tags)
    print('items bin tags: %s' % len(binary_tags))
    all_bin_tags.append(binary_tags)

print('len of all items: %s ' % len(all_bin_tags))

features = array(all_bin_tags)
whitened = whiten(features)

# book = array((whitened[0],whitened[2]))  # should be the k guess (fixed to 20 because was 2)

print(len(kmeans(whitened, 20)[0]))

for centroid in (kmeans(whitened, 20)[0]):
    print(centroid)

print('_____________')
#print(all_tags.items())