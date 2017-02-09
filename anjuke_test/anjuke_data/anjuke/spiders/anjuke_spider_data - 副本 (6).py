#coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from anjuke.items import AnjukeItem
from anjuke.settings import global_spider
from scrapy import log,FormRequest
import re,time,sys,json,MySQLdb,copy,hashlib
from redis import Redis
from scrapy.http.cookies import CookieJar
from scrapy_redis.spiders import RedisSpider
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
reload(sys)
sys.setdefaultencoding( "utf-8" )


class anjuke_spider(CrawlSpider):
	
	spider_id = global_spider.get_spider_id()
	global_spider.spider_id_add()
	name = "anjuke_spider%s"%spider_id
	batch_id = 0
	start_urls = []
	r = Redis(host="192.168.10.39")
	
	allowed_domains = ["fang.com"]


	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = cls(*args, **kwargs)
		spider._set_crawler(crawler)
		spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
		return spider

	def spider_idle(self):
		for req in self.start_requests():
			self.crawler.engine.crawl(req, spider=self)
		raise DontCloseSpider

	def start_requests(self):
		url_format = 'http://esf.fang.com/chushou/3_%s.htm'
		try:
			for id_code in self.r.zrevrange('house:zset',0,1000):
				url = url_format%(id_code)
				print url
				yield Request(url=url,
								method='GET',
								callback=self.parse,
								dont_filter=True)
		except Exception as e:
			print Exception,":",e

	def _item_init(self,item):
		item['fang_id'] = ''
		item['url'] = ''
		item['body'] = ''
		return item


	def parse(self, response):

		sel = Selector(response)
		item = AnjukeItem()
		item = self._item_init(item)
		try:
			fang_info = {'title':'','info':'','desc':'','pic_tab':''}
			url = item['url'] = response.url
			fang_id = item['fang_id'] = (re.search(r'\d+_\d+',url)).group(0)
			item['body'] = (response.body).decode('gbk').encode('utf8')


			try:
				fang_info['title'] = sel.xpath('//div[@class="mainBoxL"]/div[@class="title"]').extract()[0]
			except Exception as e:
				print Exception,":",e
			try:
				fang_info['info'] = sel.xpath('//div[@class="houseInfor clearfix"]/div[@class="inforTxt"]').extract()[0]
			except Exception as e:
				print Exception,":",e

			try:
				fang_info['desc'] = sel.xpath('//div[@id="hsPro-pos"]/div[@class="describe mt10"]').extract()[0]
			except Exception as e:
				print Exception,":",e

			try:
				fang_info['pic_tab'] = sel.xpath('//div[@id="hsPic-pos"]').extract()[0]
			except Exception as e:
				print Exception,":",e

			m = hashlib.md5()
			m.update(str(fang_info))
			follow_value = m.hexdigest()
			yield item

		except Exception as e:
			print Exception,":",e
