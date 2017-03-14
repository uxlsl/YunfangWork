#-*-coding=utf-8-*-
from __future__ import absolute_import

import sys ,os
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

from celery import Celery
from kombu import Queue


app = Celery('spider_service')
app.config_from_object('celeryconf')
