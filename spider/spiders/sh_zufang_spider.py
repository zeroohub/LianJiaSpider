# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import scrapy
import json
district_url = 'http://soa.dooioo.com/api/v4/online/house/rent/listMapResult?access_token=7poanTTBCymmgE0FOn1oKp&client=pc&cityCode=sh&siteType=quyu&type=district&dataId=sh&showType=list&limit_count=2000'
plate_url = 'http://soa.dooioo.com/api/v4/online/house/rent/listMapResult?access_token=7poanTTBCymmgE0FOn1oKp&client=pc&cityCode=sh&siteType=quyu&type=plate&dataId={district_name}&showType=list&limit_count=2000'
village_url = 'http://soa.dooioo.com/api/v4/online/house/rent/listMapResult?access_token=7poanTTBCymmgE0FOn1oKp&client=pc&cityCode=sh&siteType=quyu&type=village&dataId={village_name}&showType=list&limit_count=2000'
community_url = 'http://soa.dooioo.com/api/v4/online/rent/zufang/search?access_token=7poanTTBCymmgE0FOn1oKp&client=pc&cityCode=sh&community_id={community_id}&limit_offset=1&limit_count=100'

class LianJiaSpider(scrapy.Spider):
    name = 'lianjia'

    start_urls = [district_url]

    def parse(self, response):
        jres = json.loads(response.body)

        for data in jres['dataList']:
            current_type = data['currentType']
            if current_type == 'village':
                next_page = community_url.format(community_id=data['dataId'])
                yield response.follow(next_page, self.parse_community)
            else:
                if current_type == 'district':
                    next_page = plate_url.format(district_name=data['dataId'])
                elif current_type == 'plate':
                    next_page = village_url.format(village_name=data['dataId'])
                else:
                    next_page = None
                yield response.follow(next_page, self.parse)

    def parse_community(self, response):
        jres = json.loads(response.body)
        for data in jres['data']['list']:
            yield {
                'url': data['webUrl'],
                'price': data['rentPrice']
            }
