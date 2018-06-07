# -*- coding: utf-8 -*-
from mongoengine import *

class Apartment(EmbeddedDocument):
    id = StringField()
    bedrooms = IntField(min_value=0)
    halls = IntField(min_value=0)
    is_ziroom = BooleanField()
    pic_url = StringField()
    price = IntField()
    area = FloatField()
    title = StringField()

class District(EmbeddedDocument):
    pass

class Bizcircle(EmbeddedDocument):
    pass

class Community(EmbeddedDocument):
    id = IntField()
    name = StringField()
    apartments = DictField()


class City(Document):
    code = StringField()
    id = IntField()

