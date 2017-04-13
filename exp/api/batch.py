import json
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer

# time.sleep(20)
es = Elasticsearch(['es'])
consumer = KafkaConsumer('new_carpools_topic', group_id='carpool_index', bootstrap_servers=['kafka:9092'])
for message in consumer:
    new_carpool = (json.loads(message.value.decode('utf-8')))
    es.index(index='carpool_index', id=new_carpool['id'], body=new_carpool)
    es.indices.refresh(index='carpool_index')
    print('updated')
