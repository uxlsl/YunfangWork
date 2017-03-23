# -*- coding:utf-8 -*-

"""通知统计任务"""
import datetime
from django.conf import settings

from house.models import SyncHouse, SendTaskHistory
from house.utils import feed_agent
from celery import Celery


def run():
    day = datetime.datetime.combine(
            datetime.datetime.now().date(),
            datetime.time(0,0,0))
    while True:
        if SyncHouse.objects.filter(created_at__gt=day):
            feed_agent()
            celery = Celery(**settings.CELERY_SETTING)
            celery.send_task("stat")
            SendTaskHistory().save()
            break

