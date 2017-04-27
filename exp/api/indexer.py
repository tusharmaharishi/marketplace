import json
import os
import sched
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer


def update_indices(sc):
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    for message in consumer:
        try:
            res_json = json.loads(message.value.decode('utf-8'))
        except ValueError as e:
            print(e.message)
        data = res_json.get('data')
        if data:
            new_listing = data[0]
            if 'password' in new_listing['fields']:
                new_listing['fields'].pop('password', None)
            if new_listing['model'] == 'marketplace.user':
                es.index(index='user_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
                es.index(index='main_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
            elif new_listing['model'] == 'marketplace.carpool':
                es.index(index='carpool_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
                es.index(index='main_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
    es.indices.refresh(index='user_index')
    es.indices.refresh(index='carpool_index')
    es.indices.refresh(index='main_index')
    sch.enter(20, 1, update_indices, (sc,))


if __name__ == '__main__':
    try:
        es = Elasticsearch([{'host': 'es', 'port': 9200}])
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    finally:
        es = Elasticsearch([{'host': 'es', 'port': 9200}])
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        sch = sched.scheduler(time.time, time.sleep)
        db = {}
        print(os.getcwd())
        with open('./fixtures/db.json') as f:
            db = json.load(f)
        for listing in db:
            if 'password' in listing['fields']:
                listing['fields'].pop('password', None)
            if listing['model'] == 'marketplace.user':
                es.index(index='user_index', doc_type='listing', id=listing['pk'], body=listing)
                es.index(index='main_index', doc_type='listing', id=listing['pk'], body=listing)
            elif listing['model'] == 'marketplace.carpool':
                es.index(index='carpool_index', doc_type='listing', id=listing['pk'], body=listing)
                res = es.index(index='main_index', doc_type='listing', id=listing['pk'], body=listing)
        es.indices.refresh(index='user_index')
        es.indices.refresh(index='carpool_index')
        es.indices.refresh(index='main_index')
        sch.enter(20, 1, update_indices, (sch,))
        sch.run()
