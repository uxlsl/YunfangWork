#-*-coding=utf-8-*-

from __future__ import absolute_import
from celery import Celery
from kombu import Queue

app = Celery('async_html_update_service',
                broker="redis://192.168.6.4:6379/2",
                backend="redis://192.168.6.4:6379/3",
                include=['async_html_update_service.upload_service'])

app.conf.update(
            CELERY_DEFAULT_QUEUE='upload_queue')
