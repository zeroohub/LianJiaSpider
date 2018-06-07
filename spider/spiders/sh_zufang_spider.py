# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import scrapy
import json

city_detail_url = 'https://ajax.lianjia.com/ajax/card/cityZufang?id={city_id}'
district_list_url = 'https://ajax.lianjia.com/ajax/mapsearch/area/districtZufang?city_id={city_id}'
district_detail_url = 'https://ajax.lianjia.com/ajax/card/districtZufang?id={district_id}'
bizcircle_list_url = 'https://ajax.lianjia.com/ajax/mapsearch/area/bizcircleZufang?city_id={city_id}'
bizcircle_detail_url = 'https://ajax.lianjia.com/ajax/card/bizcircleZufang?id={bizcircle_id}'
bizcircle_house_list_url = ('https://ajax.lianjia.com/ajax/housesell/area/bizcircleZufang?'
                            'ids={bizcircle_ids}&'
                            'limit_offset={offset}&limit_count={count}&city_id={city_id}')
house_url = 'https://{city_code}.lianjia.com/zufang/{house_code}.html'


class LianJiaSpider(scrapy.Spider):
    name = 'lianjia'
    city_id = 310000
    city_code = 'sh'

    def start_requests(self):
        urls = [
            bizcircle_list_url.format(city_id=self.city_id)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        body = json.loads(response.body)
        if len(body['data']) == 0:
            raise Exception

        for bizcircle in body['data']:
            total = bizcircle['house_count']
            step = 100
            for offset in range(0, total, step):
                count = min(step, total)
                next_page = bizcircle_house_list_url.format(
                    bizcircle_ids=bizcircle['id'],
                    count=count,
                    offset=offset,
                    city_id=self.city_id
                )
                yield response.follow(next_page, callback=self.parse_house)

    def parse_house(self, response):
        body = json.loads(response.body)
        for house in body['data'].get('list', []):
            if house['house_code'][:2].upper() != self.city_code.upper():
                yield {
                    'house_url': house_url.format(city_code=self.city_code,
                                                  house_code=house['house_code'])}

