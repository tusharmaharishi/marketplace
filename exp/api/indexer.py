import json
import sched
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer

es = Elasticsearch([{'host': 'es', 'port': 9200}])
sch = sched.scheduler(time.time, time.sleep)

def update_indices(sc):
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer',  bootstrap_servers=['kafka:9092'])
    for message in consumer:
        try:
            carpools = json.loads(message.value.decode('utf-8'))
        except ValueError as e:
            print(e.message)
        data = carpools.get('data')
        if data:
            new_carpool = data[0]
            res = es.index(index='listing_index', doc_type='listing', id=new_carpool['pk'], body=new_carpool)
            print(res['created'], new_carpool)
    es.indices.refresh(index='listing_index')
    sch.enter(20, 1, update_indices, (sc,))


sch.enter(20, 1, update_indices, (sch,))
sch.run()
