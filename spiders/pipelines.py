# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid
from datetime import datetime

import pymongo
import telegram

class FormatPipeline(object):
    def process_item(self, item, spider):
        district = item['district']
        bizcircle = item['bizcircle']
        house = item['house']

        house['district_id'] = district['id']
        house['district_name'] = district['name']
        house['bizcircle_id'] = bizcircle['id']
        house['bizcircle_name'] = bizcircle['name']
        return house


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db, stats):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        stats.set_value('crawl_id', uuid.uuid4().hex)
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'rent_house'),
            stats=crawler.stats
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        apartments = self.db.apartments
        house = {
            'start_time': self.stats.get_value('start_time'),
            'crawl_id': self.stats.get_value('crawl_id'),
            'created': datetime.now()
        }
        house.update(item)
        apartments.insert_one(house)
        return item

    def close_spider(self, spider):
        logs = self.db.logs
        logs.insert_one(self.stats.get_stats())
        self.client.close()


