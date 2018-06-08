# -*- coding: utf-8 -*-
from mongoengine import *


class Apartment(Document):
    id = StringField(primary_key=True)
    bedrooms = IntField(min_value=0)
    halls = IntField(min_value=0)
    is_ziroom = BooleanField()
    pic_url = StringField()
    price = IntField()
    area = FloatField()
    title = StringField()

    community_id = IntField()
    community_name = StringField()

    district_id = IntField()
    district_name = StringField()

    bizcircle_id = IntField()
    bizcircle_name = StringField()


# class Community(EmbeddedDocument):
#     id = IntField(primary_key=True)
#     name = StringField()
#     apartments = ListField(EmbeddedDocumentField(Apartment))
#
#
# class Bizcircle(EmbeddedDocument):
#     id = IntField(primary_key=True)
#     name = StringField()
#     communities = ListField(EmbeddedDocumentField(Community))
#
# class District(EmbeddedDocument):
#     id = IntField(primary_key=True)
#     name = StringField()
#     bizcircles = ListField(EmbeddedDocumentField(Bizcircle))
#
#
# class City(Document):
#     id = IntField(primary_key=True)
#     code = StringField()
#     name = StringField()
#     districts = ListField(EmbeddedDocumentField(District))
