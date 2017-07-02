# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import stringcase
from scrapy_djangoitem import DjangoItem

from web.models import Apartment


class ApartmentItem(DjangoItem):
    django_model = Apartment

    @classmethod
    def create_or_update(cls, data):
        house_rent_id = data.pop('houseRentId')
        django_object = cls.django_model(house_rent_id=house_rent_id)
        item = ApartmentItem()
        item._instance = django_object

        for f in ApartmentItem.django_model._meta.get_fields():
            field = data.get(stringcase.camelcase(f.name), None)
            if field is not None:
                item[f.name] = field
        return item

