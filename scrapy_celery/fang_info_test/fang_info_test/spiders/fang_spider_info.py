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
from scrapy_redis import connection
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
import fang_info_test.log_mysql as log_mysql
reload(sys)
sys.setdefaultencoding( "utf-8" )


class fang_info_spider(CrawlSpider):
    
    global_spider.spider_id_add()
    name = "fang_info_spider"


    def parse(self, response):
        log_mysql.log_in_mysql(response.url,"Get")
        print "Get : ",response.url
