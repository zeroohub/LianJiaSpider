# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import send_mail

from models import Apartment
from datetime import datetime, timedelta


def email_new_apartment():

    count = Apartment.good_room().filter(
        online_time__gte=datetime.now() - timedelta(hours=1)
    ).count()

    if count > 0:
        send_mail(
            'LianJia New Room Available',
            'new room {}'.format(count),
            from_email='',
            recipient_list=[''],
            fail_silently=False,
        )
