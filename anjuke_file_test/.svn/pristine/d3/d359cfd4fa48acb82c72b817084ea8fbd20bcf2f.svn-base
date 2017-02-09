#coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from anjuke.items import AnjukeItem
from anjuke.settings import global_spider
from scrapy import log,FormRequest
import re,time,sys,json,MySQLdb,copy
from redis import Redis
from scrapy.http.cookies import CookieJar
from scrapy_redis.spiders import RedisSpider
reload(sys)
sys.setdefaultencoding( "utf-8" )


class anjuke_spider(RedisSpider):
	
	spider_id = global_spider.get_spider_id()
	global_spider.spider_id_add()
	name = "anjuke_spider%s"%spider_id
	redis_key = 'anjuke_spider:start_urls'
	custom_settings = {
    'EXTENSIONS':{'scrapy.telnet.TelnetConsole': None,'anjuke.auto_lpush_start.auto_lpush':400},}
	allowed_domains = ["anjuke.com"]

			
	def parse(self, response):

		url_format = 'http://guangzhou.anjuke.com/sale/'
		upper_bound = 1000
		division = 500
		step = upper_bound/division
		for section_index in range(division):

			spider_upper_bound = (step)*(section_index + 1)
			spider_lower_bound = (step)*(section_index)
			if spider_lower_bound >= 999:
				spider_upper_bound = 99999
			print spider_upper_bound,spider_lower_bound
			try:
				r = Redis()
				for page_index in range(1,51):
					url = url_format+('o5-p%s/'%page_index)+('?to_price=%s&from_price=%s'%(spider_upper_bound,spider_lower_bound))
					print url
					r.sadd('anjuke_spider:page_url',url)
				#r.lpush('anjuke_spider:start_urls','http://guangzhou.anjuke.com/sale/')
			except Exception as e:
				print Exception,":",e

