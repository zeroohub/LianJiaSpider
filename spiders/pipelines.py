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


class CustomFilterPipeline(object):

    def process_item(self, item, spider):
        return item

    def house_good(self, house):
        if (not int(house['is_ziroom'])
                and int(house["frame_bedroom_num"]) >= 2
                and int(house["price_total"]) <= 6000):

            return True
        return False

    def notify(self):

        chat_id = 525052106
        token = ''
        bot = telegram.Bot(token=token)
        content = u"new house:\n"
        for house in self.added_apartments:
            content += u"{}|{}|{}: {}室{}厅 {}元 {}平米 距离{}{}站{}米, 链接: {}\n".format(
                house['district_name'],
                house['bizcircle_name'],
                house['community_name'],
                house['frame_bedroom_num'],
                house['frame_hall_num'],
                house['price_total'],
                house['rent_area'],
                house.get('subway_station', {}).get('line_name', ""),
                house.get('subway_station', {}).get('station_name', ""),
                house.get('subway_station', {}).get('distance', ""),
                'https://sh.lianjia.com/zufang/{}.html'.format(house['house_code'])
            )
        bot.send_message(chat_id, content)

        content = u'removed house:\n'
        for house in self.removed_apartments:
            content += u"{}|{}|{}: {}室{}厅 {}元 {}平米 距离{}{}站{}米, 链接: {}\n".format(
                house['district_name'],
                house['bizcircle_name'],
                house['community_name'],
                house['frame_bedroom_num'],
                house['frame_hall_num'],
                house['price_total'],
                house['rent_area'],
                house.get('subway_station', {}).get('line_name', ""),
                house.get('subway_station', {}).get('station_name', ""),
                house.get('subway_station', {}).get('distance', ""),
                'https://sh.lianjia.com/zufang/{}.html'.format(house['house_code'])
            )
        bot.send_message(chat_id, content)

    def close_spider(self, spider):
        client = pymongo.MongoClient()
        logs = client.lianjia_sh.logs
        apartments = client.lianjia_sh.apartments

        logs.insert_one({'started': spider.started, 'status': 'succeed'})
        last_two_logs = logs.find().sort('started', pymongo.DESCENDING)[:2]

        new_apartments = {a['house_code']: a for a in apartments.find({'started': last_two_logs[0]['started']})}
        old_apartments = {a['house_code']: a for a in apartments.find({'started': last_two_logs[1]['started']})}

        added_apartments = []
        removed_apartments = []
        for house_code, house in new_apartments.iteritems():
            if (house_code not in old_apartments
                    and self.house_good(house)):
                added_apartments.append(house)

        for house_code, house in old_apartments.iteritems():
            if (house_code not in new_apartments
                    and self.house_good(house)):
                removed_apartments.append(house)

        self.added_apartments = added_apartments
        self.removed_apartments = removed_apartments
        self.notify()
        client.close()

