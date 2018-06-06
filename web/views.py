# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.shortcuts import render
# Create your views here.
from web.models import Apartment


def arts_list(request):
    apts = Apartment.good_room().filter(
        online_time__gte=datetime.now() - timedelta(days=1)
    )
    return render(request, 'web/index.html', {'apts': apts})