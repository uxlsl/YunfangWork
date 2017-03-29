# -*- coding:utf-8 -*-
import datetime
from house.stat import agent_stat


def run():
    start = datetime.datetime(2017, 3, 1, 0, 0, 0)
    end = datetime.datetime(2017, 3, 31, 0, 0, 0)
    agent_stat(start, end)
