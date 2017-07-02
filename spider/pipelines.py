# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider.items import ApartmentItem


class ApartmentPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ApartmentItem):
            spider.log('save a new instance')
            spider.log(item)
            item.save()
        return item
