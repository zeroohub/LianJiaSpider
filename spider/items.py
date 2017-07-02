# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import stringcase
from datetime import datetime
from scrapy_djangoitem import DjangoItem

from web.models import Apartment


class BaseDjangoItem(DjangoItem):
    def save(self, commit=True):
        modelargs = dict((k, self.get(k)) for k in self._values
                         if k in self._model_fields)
        for k, v in modelargs.iteritems():
            setattr(self.instance, k, v)
        if commit:
            self.instance.save()
        return self.instance


class ApartmentItem(BaseDjangoItem):
    django_model = Apartment

    @classmethod
    def preprocess(cls, data):
        for k, v in data.iteritems():
            if k == 'onlineTime':
                data[k] = datetime.fromtimestamp(v / 1e3)

    @classmethod
    def create_or_update(cls, data):
        cls.preprocess(data)

        house_rent_id = data.pop('houseRentId')
        obj, _ = cls.django_model.objects.get_or_create(house_rent_id=house_rent_id)
        item = ApartmentItem()
        item._instance = obj

        for f in obj._meta.get_fields():
            field = data.get(stringcase.camelcase(f.name), None)
            if field is not None:
                item[f.name] = field
        return item

