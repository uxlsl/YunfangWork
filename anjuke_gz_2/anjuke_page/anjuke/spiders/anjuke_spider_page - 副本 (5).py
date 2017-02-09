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
	redis_key = 'anjuke_spider:page_url'
	
	allowed_domains = ["anjuke.com"]


	def parse(self,response):

		sel = Selector(response)
		try:
			cur_page = sel.xpath('//div[@class="multi-page"]/i[@class="curr"]/text()').extract()[0]
			links = SgmlLinkExtractor(allow=(r'http://.+.anjuke.com/prop/view/.+'),restrict_xpaths=('//ul[@id="houselist-mod"]'),unique=0).extract_links(response)
			r = Redis()
			for link in links:
				try:
					anjuke_id = (re.search(r'A\d+',link.url)).group(0).replace('A','')
					filte_flag = r.sismember('anjuke_gz:history',anjuke_id)
					if not filte_flag:
						r.sadd('anjuke_spider:data_url', link.url)
						r.sadd('anjuke_gz:history',anjuke_id)
				except Exception as e:	
					print Exception,":",e
		except Exception as e:
			print Exception,":",e