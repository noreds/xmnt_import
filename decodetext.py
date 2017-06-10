## hopefully obsolete now...

from urllib import parse
import os
import json

imported_news = 'imported'
decoded_news = 'decoded'

if not os.path.isdir(decoded_news):
    os.mkdir(decoded_news)


for fn in os.listdir(imported_news):
    filename = os.path.join(imported_news, fn)
    if os.path.isfile(filename):
        d = None
        with open(filename, 'r') as f:
            d = json.load(f)
            #print(parse.unquote(d['text']))

        with open(decoded_news + '/' + fn, 'w+', encoding='utf8') as f:
            d['text'] = parse.unquote(d['text'])
            json.dump(d, f, ensure_ascii=False )


