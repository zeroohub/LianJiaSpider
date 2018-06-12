# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import scrapy


def json_response(func):
    def wrap(self, response):
        data = json.loads(response.body_as_unicode())['data']
        return func(self, response, data)

    return wrap


def pick_id_names(data):
    return {k: v for k, v in data.iteritems() if k in ('id', 'name')}


house_url = 'https://{city_code}.lianjia.com/zufang/{house_code}.html'


class RentSpiderMixin(object):
    city_id = 0
    city_code = ''

    city_detail_url = 'https://ajax.lianjia.com/ajax/card/cityZufang?id={city_id}'
    district_list_url = 'https://ajax.lianjia.com/ajax/mapsearch/area/districtZufang?city_id={city_id}'
    bizcircle_list_url = ('https://ajax.lianjia.com/ajax/mapsearch/area/bizcircleZufang'
                          '?city_id={city_id}&district_id={district_id}')
    house_list_url = ('https://ajax.lianjia.com/ajax/housesell/area/bizcircleZufang'
                      '?ids={bizcircle_ids}&city_id={city_id}'
                      '&limit_offset={offset}&limit_count={count}')

    def start_requests(self):
        urls = [
            self.city_detail_url.format(city_id=self.city_id)
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_city,
                meta={})

    @json_response
    def parse_city(self, response, data):
        meta = {
            'city': {
                'id': data['city_id'],
                'name': data['city_name'],
                'code': self.city_code
            }
        }
        meta.update(response.meta)
        next_page = self.district_list_url.format(
            city_id=data['city_id'])
        yield response.follow(
            next_page,
            callback=self.parse_district,
            meta=meta)

    @json_response
    def parse_district(self, response, data):
        for district in data:
            meta = {
                'district': pick_id_names(district)
            }
            meta.update(response.meta)
            next_page = self.bizcircle_list_url.format(
                city_id=meta['city']['id'],
                district_id=meta['district']['id'])
            yield response.follow(
                next_page,
                callback=self.parse_bizcircle,
                meta=meta)

    @json_response
    def parse_bizcircle(self, response, data):
        for bizcircle in data:
            meta = {
                'bizcircle': pick_id_names(bizcircle)
            }
            meta.update(response.meta)
            total = bizcircle['house_count']
            step = 100
            for offset in range(0, total, step):
                count = min(step, total)
                next_page = self.house_list_url.format(
                    bizcircle_ids=meta['bizcircle']['id'],
                    count=count,
                    offset=offset,
                    city_id=meta['city']['id']
                )
                yield response.follow(
                    next_page,
                    callback=self.parse_house,
                    meta=meta)

    @json_response
    def parse_house(self, response, data):
        for house in data['list']:
            result = {
                'house': {k: v for k, v in house.iteritems() if k not in (
                    'appid',
                    'house_picture',
                    'house_picture_count',
                    'house_picture_db',
                )}
            }
            result.update(response.meta)
            yield result


class SHRentSpider(RentSpiderMixin, scrapy.Spider):
    name = 'sh_rent'
    city_id = 310000
    city_code = 'sh'
