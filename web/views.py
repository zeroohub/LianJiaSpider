# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.shortcuts import render

# Create your views here.
from web.models import Apartment


def arts_list(request):
    apts = Apartment.objects.filter(
        online_time__gte=datetime.now() - timedelta(days=1)
    ).filter(
        rent_price__lte=4000
    ).filter(
        rent_city_code='shz'
    ).order_by('rent_price')

    return render(request, 'web/index.html', {'apts': apts})