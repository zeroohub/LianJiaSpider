# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.core.mail import send_mail
from django.template.loader import get_template

from models import Apartment
from datetime import datetime, timedelta


def email_new_apartment():

    apts = Apartment.objects.filter(
        online_time__gte=datetime.now() - timedelta(days=1)
    ).filter(
        rent_price__lte=4000
    ).filter(
        rent_city_code='shz'
    ).order_by('rent_price')

    template = get_template('web/index.html')
    result = template.render({'apts': apts})

    send_mail(
        'LianJia New Room Available',
        from_email='',
        recipient_list=[''],
        fail_silently=False,
        html_message=result
    )
