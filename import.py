import paho.mqtt.client as paho
import os
import ssl
import json
import time
from urllib import parse


path = os.path.dirname(os.path.realpath(__file__))
print(path)

awshost = "a1sqsm2m5a5t5j.iot.eu-central-1.amazonaws.com"
awsport = 8883
clientId = "xminutes-news-%s" % os.urandom(6)
thingName = "xminutes-news"
caPath = "%s/modules/keys/aws-iot-rootCA.crt" % path
certPath = "%s/modules/keys/sub_cert.pem" % path
keyPath = "%s/modules/keys/sub_privkey.pem" % path

topic = "news/publisher/#"

imported_news = 'imported'
if not os.path.isdir(imported_news):
    os.mkdir(imported_news)


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    ret = client.subscribe(topic, 1)
    return ret


def on_message(client, userdata, msg):
    print("topic: " + msg.topic)  # news/publisher/noz.de

    try:
        news = json.loads(msg.payload.decode('utf-8'))
        source = news.get('source', 'no-source')
        text = news.get('item', {}).get('fullText', '')
        text = parse.unquote(text)
        #print(json.dumps(news, indent=2))

        print(source)
        print(text)
        filename = '%s_%s.json' % (source, time.time())
        with open(os.path.join(imported_news, filename), 'w+') as f:
            json.dump({'source': source, 'text': text}, f, ensure_ascii=False)

    except Exception as e:
        print('%s' % e)

if __name__ == '__main__':

    mqttc = paho.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.tls_set(caPath,
                  certfile=certPath,
                  keyfile=keyPath,
                  cert_reqs=ssl.CERT_REQUIRED,
                  tls_version=ssl.PROTOCOL_TLSv1_2,
                  ciphers=None)

    mqttc.connect(awshost, awsport, keepalive=60)
    mqttc.loop_forever()