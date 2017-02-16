#coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from fang_info_test.items import Fang_Info_Test_Item
from fang_info_test.settings import global_spider
from fang_info_test.settings import Redis_key
from scrapy import log,FormRequest
import re,time,sys,json,MySQLdb,copy,hashlib
from redis import Redis
from scrapy.http.cookies import CookieJar
from scrapy_redis.spiders import RedisSpider
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
import fang_info_test.log_mysql as log_mysql
reload(sys)
sys.setdefaultencoding( "utf-8" )

DEFAULT_START_URLS_BATCH_SIZE = 16
DEFAULT_START_URLS_KEY = '%(name)s:start_urls'

class fang_info_spider(RedisSpider):
    
    spider_id = global_spider.get_spider_id()
    global_spider.spider_id_add()
    name = "fang_info_spider%s"%spider_id
    redis_key = Redis_key
    
    allowed_domains = ["fang.com"]

    def setup_redis(self, crawler=None):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if self.server is not None:
            return

        if crawler is None:
            # We allow optional crawler argument to keep backwards
            # compatibility.
            # XXX: Raise a deprecation warning.
            crawler = getattr(self, 'crawler', None)

        if crawler is None:
            raise ValueError("crawler is required")

        settings = crawler.settings

        if self.redis_key is None:
            self.redis_key = settings.get(
                'REDIS_START_URLS_KEY', DEFAULT_START_URLS_KEY,
            )

        self.redis_key = self.redis_key % {'name': self.name}

        if not self.redis_key.strip():
            raise ValueError("redis_key must not be empty")

        if self.redis_batch_size is None:
            self.redis_batch_size = settings.getint(
                'REDIS_START_URLS_BATCH_SIZE', DEFAULT_START_URLS_BATCH_SIZE,
            )

        try:
            self.redis_batch_size = int(self.redis_batch_size)
        except (TypeError, ValueError):
            raise ValueError("redis_batch_size must be an integer")

        self.logger.info("Reading start URLs from redis key '%(redis_key)s' "
                         "(batch size: %(redis_batch_size)s)", self.__dict__)

        self.server = connection.from_settings(crawler.settings)
        # The idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(self.request_dropped, signal=signals.request_dropped)


    def request_dropped(self, request, spider):
        log_mysql.log_in_mysql(response.url,'dropped')
        logger.debug(
                "Ignoring request %(response)r: Dropped",
                {'response': response}
            )

    def _item_init(self,item):
        item['fang_id'] = ''
        item['url'] = ''
        item['body'] = ''
        item['version_time'] = int(time.time())
        item['source_route'] = ''
        return item


    def next_requests(self):
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET')
        fetch_one = self.server.spop if use_set else self.server.lpop

        found = 0

        while found < self.redis_batch_size:
            data_raw = fetch_one(self.redis_key)
            if not data_raw:
                break
            data = json.loads(data_raw)
            if "source_url" not in data:
                break
            item = Fang_Info_Test_Item()
            item = self._item_init(item)
            source_route_dict = {}
            if "source" in data:
                source_route_dict['source'] = data['source'].encode('utf-8')
            if "city" in data:
                source_route_dict['city'] = data['city'].encode('utf-8')
            if "type" in data:
                source_route_dict['type'] = data['type'].encode('utf-8')
            source_route_dict['key_route'] = self.redis_key
            print source_route_dict
            item['source_route'] = json.dumps(source_route_dict,ensure_ascii=False)
            req = Request(url=data['source_url'],
                            method='GET',
                            callback=self.parse,
                            dont_filter=True,
                            meta={"item":item})
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %s", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)


    def parse(self, response):

        sel = Selector(response)
        item = response.meta['item']
        try:
            fang_info = {'title':'','info':'','desc':'','pic_tab':''}
            url = item['url'] = response.url
            fang_id = item['fang_id'] = (re.search(r'\d+_\d+',url)).group(0)
            item['body'] = (response.body).decode('gbk').encode('utf8')
            yield item

        except Exception as e:
            print Exception,":",e
