# -*- coding: utf-8 -*-
import pymongo
from env import MONGO_URI, MONGO_DB


def house_good(house):
    if ('subway_station' in house
            and house['subway_station']['line_name'] == u'10号线'
            # and house.get('subway_station', {}).get('station_name', "") in (
            #         u'南京东路', u'天潼路', u'四川北路', u'海伦路', u'邮电新村')
            and not int(house['is_ziroom'])
            and int(house["frame_bedroom_num"]) >= 1
            and int(house["price_total"]) <= 6000):
        return True
    return False

def chunk_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def houses2str(houses):
    chunks = chunk_list(houses, 10)
    content_list = []
    for houses in chunks:
        content = u""
        for house in houses:
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
        content_list.append(content)
    return content_list


def notify(added, removed):
    from notfication.telegram_bot import send_message
    for houses, content in [(added, u"新添加房:\n"), (removed, u'删除的房:\n')]:
        for con in houses2str(houses):
            content += con
            send_message(content)


def check_new_houses():
    with pymongo.MongoClient(MONGO_URI) as client:
        db = client[MONGO_DB]

        logs = db.logs
        apartments = db.apartments

        last_two_logs = logs.find().sort('start_time', pymongo.DESCENDING)[:2]

        new_apartments = {a['house_code']: a for a in apartments.find({'crawl_id': last_two_logs[0]['crawl_id']})}
        old_apartments = {a['house_code']: a for a in apartments.find({'crawl_id': last_two_logs[1]['crawl_id']})}

    added_apartments = []
    removed_apartments = []
    for house_code, house in new_apartments.iteritems():
        if (house_code not in old_apartments
                and house_good(house)):
            added_apartments.append(house)

    for house_code, house in old_apartments.iteritems():
        if (house_code not in new_apartments
                and house_good(house)):
            removed_apartments.append(house)

    notify(added_apartments, removed_apartments)


def get_all_houses():
    with pymongo.MongoClient(MONGO_URI) as client:
        db = client[MONGO_DB]
        apartments = db.apartments
        logs = db.logs

        crawl_log = logs.find().sort('start_time', pymongo.DESCENDING)[1]
        added_apartments = [a for a in apartments.find(
            {'crawl_id': crawl_log['crawl_id']}) if house_good(a)]
        return houses2str(added_apartments)


if __name__ == '__main__':
    check_new_houses()
