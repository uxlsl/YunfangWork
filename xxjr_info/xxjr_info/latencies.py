import time

from scrapy.exceptions import NotConfigured
from twisted.internet import task
from scrapy import signals


class Latencies(object):
    """
    An extension that measures throughput and latencies.
    """
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler
        #self.interval = crawler.settings.getfloat('LATENCIES_INTERVAL')

        #if not self.interval:
        #    raise NotConfigured

        cs = crawler.signals
        cs.connect(self._request_scheduled, signal=signals.request_scheduled)
        cs.connect(self._response_received, signal=signals.response_received)

    def _request_scheduled(self, request, spider):
        #print request.headers
        #print request.url
        pass

    def _response_received(self, response, request, spider):
        print request.Cookie
        print request.url