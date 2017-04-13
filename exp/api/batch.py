import json
import sched
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer

es = Elasticsearch([{'host': 'es', 'port': 9200}])
sch = sched.scheduler(time.time, time.sleep)

def update_indices(sc):
    print('helppppppp')
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer',  bootstrap_servers=['kafka:9092'])
    for message in consumer:
        new_carpool = json.loads(message.value.decode('utf-8'))['data'][0]
        print(new_carpool)
        res = es.index(index='listing_index', doc_type='listing', id=new_carpool['pk'], body=new_carpool)
        print(res['created'])
    es.indices.refresh(index='listing_index')
    print('refresh')
    sch.enter(20, 1, update_indices, (sc,))


sch.enter(20, 1, update_indices, (sch,))
sch.run()
