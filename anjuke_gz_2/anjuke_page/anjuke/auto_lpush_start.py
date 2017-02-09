# -*- coding: utf-8 -*-

import random,urllib,json,base64

from scrapy.exceptions import NotConfigured
from twisted.internet import task
from scrapy import signals
from redis import Redis


class auto_lpush(object):
    """
    An extension that measures throughput and latencies.
    """
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler
        self.interval = crawler.settings.getfloat('AUTO_LPUSH_INTERVAL')
        print "time delay %s"%(self.interval)

        if not self.interval:
            raise NotConfigured

        cs = crawler.signals
        cs.connect(self._spider_closed, signal=signals.spider_closed)

        r = Redis()
        #r.lpush('anjuke_spider:start_urls','http://guangzhou.anjuke.com/sale/')
        self.task = task.LoopingCall(self._push)
        self.task.start(self.interval)


    def _spider_closed(self, spider, reason):
        if self.task.running:
            self.task.stop()

    def _push(self):
        try:
            r = Redis()
            r.lpush('anjuke_spider:start_urls','http://guangzhou.anjuke.com/sale/')
        except Exception as e:
            print Exception,":",e