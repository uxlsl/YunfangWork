#coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from CAA_DATA_Crawl.items import CaaDataCrawlItem
from CAA_DATA_Crawl.settings import global_spider
from CAA_DATA_Crawl.settings import DEFAULT_REQUEST_HEADERS as default_headers
from scrapy import log,FormRequest
import re,time,sys,json,MySQLdb,copy
from redis import Redis
from scrapy.http.cookies import CookieJar
from scrapy_redis.spiders import RedisSpider
reload(sys)
sys.setdefaultencoding( "utf-8" )


class CaaSpiderSpider(RedisSpider):

    spider_id = global_spider.get_spider_id()
    global_spider.spider_id_add()
    name = "anjuke_spider%s"%spider_id
    allowed_domains = ['htvaluer.com']
    redis_key = 'CAA_Search:seed'

    class CaaSpiderFormRequest(FormRequest):
        def __init__(self, *args, **kwargs):
            formdata = kwargs.pop('formdata', None)
            if formdata and kwargs.get('method') is None:
                kwargs['method'] = 'POST'

            super(FormRequest, self).__init__(*args, **kwargs)

            if formdata:
                items = formdata.items() if isinstance(formdata, dict) else formdata
                querystr = str(items)
                if self.method == 'POST':
                    self.headers.setdefault(b'Content-Type', b'application/x-www-form-urlencoded')
                    self._set_body(querystr)
                else:
                    return

    def parse_item(self, response):
        
