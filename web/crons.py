# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.core.mail import send_mail
from django.forms.models import model_to_dict

from models import Apartment
from datetime import datetime, timedelta


def email_new_apartment():
    apts = Apartment.objects.filter(
        online_time__gte=datetime.now() - timedelta(days=1)
    ).filter(
        rent_price__lte=4000
    )
    apts_dict = []
    for a in apts:
        na = model_to_dict(a)
        for k, v in na.iteritems():
            if isinstance(v, datetime):
                na[k] = v.isoformat()
        apts_dict.append(na)


    send_mail(
        'LianJia New Room Available',
        json.dumps(apts_dict),
        '',
        [''],
        fail_silently=False,
    )
