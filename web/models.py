# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

SH = 1
# Create your models here.
CITY_CODE_CHOICES = (
    (SH, 'sh')
)


class Apartment(models.Model):
    id = models.AutoField(primary_key=True)
    acreage = models.FloatField(null=True)
    building_year = models.SmallIntegerField(null=True)
    city_code = models.CharField(max_length=20, null=True)
    decoration = models.CharField(max_length=20, null=True)
    district_name = models.CharField(max_length=20, null=True)
    face = models.CharField(max_length=20, null=True)
    floor_state = models.CharField(max_length=50, null=True)
    house_rent_id = models.IntegerField(unique=True, db_index=True)
    house_type = models.CharField(max_length=20, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    lift_scale = models.CharField(max_length=20, null=True)
    look_count = models.IntegerField(null=True)
    metro_remark = models.CharField(max_length=100, null=True)
    online_time = models.DateTimeField(null=True)
    plate_id = models.IntegerField(null=True)
    plate_name = models.CharField(max_length=50, null=True)
    private_bathroom = models.IntegerField(null=True)
    property_name = models.CharField(max_length=50, null=True)
    property_no = models.IntegerField(null=True)
    rent_price = models.FloatField(null=True)
    rent_type = models.IntegerField(null=True)
    room = models.IntegerField(null=True)
    web_url = models.CharField(max_length=200, null=True)
    tags = models.CharField(max_length=500, null=True)
