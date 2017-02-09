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
		url_format = 'http://esf.fang.com/house/'
		try:
			for page_index in range(1,31):
				url = url_format+'i3%s/'%(page_index)
				yield Request(url=url,
								method='GET',
								callback=self.parse,
								dont_filter=True,
								meta={'submit_time': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),'page_index':page_index,'batch_id':self.batch_id})
			self.batch_id += 1
		except Exception as e:
			print Exception,":",e

	def _item_init(self,item):
		item['fang_id'] = ''
		item['batch_id'] = ''
		item['submit_time'] = ''
		item['schedule_time'] = ''
		item['received_time'] = ''
		item['page_index'] = ''
		item['rank'] = ''
		item['update_tag'] = ''
		item['update_time'] = ''
		item['server_time'] = ''
		return item


	def parse(self, response):

		item = AnjukeItem()
		item = self._item_init(item)
		sel = Selector(response)
		item['batch_id'] = batch_id = response.meta['batch_id']
		item['submit_time'] =submit_time = response.meta['submit_time']
		item['schedule_time'] =schedule_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(response.meta['schedule_time'])))
		item['received_time'] =received_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(response.meta['received_time'])))
		item['page_index'] =page_index = response.meta['page_index']
		server_time = time.mktime(time.strptime(response.headers['Date'],"%a, %d %b %Y %H:%M:%S %Z")) + 8*3600
		item['server_time'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(server_time)))
		try:
			if sel.xpath('//div[@class="list sorry_word"]') != []:
				if 'retry_count' in response.meta:
					retry_count = int(response.meta['retry_count'])
				else:
					retry_count = 0
				if retry_count <=2:
					print "retry......"
					yield Request(url=response.url,
									method='GET',
									callback=self.parse,
									meta={'submit_time':submit_time,'schedule_time':schedule_time,'received_time':received_time,'retry_count':retry_count+1,'page_index':page_index,'batch_id':batch_id})
				else:
					return
			if len(sel.xpath('//div[@class="houseList"]/dl[@class="list rel"]'))>30:
				dl_list = sel.xpath('//div[@class="houseList"]/dl[@class="list rel"]')
				for dl_index in range(1,len(dl_list)):
					try:
						item['fang_id'] =fang_id = (re.search(r'\d_\d+',(dl_list[dl_index].xpath('./dd[@class="info rel floatr"]/p[@class="title"]/a/@href').extract()[0]))).group(0)
						item['rank'] =rank = 30*(page_index-1)+dl_index
						item['update_tag'] =update_tag = dl_list[dl_index].xpath('./dd[@class="info rel floatr"]/p[@class="gray6 mt10"]/span[@class="ml10 gray9"]/text()').extract()[0]
						if re.match(r'\d+秒前更新'.decode("utf-8"),update_tag):
							deviation = int(update_tag.replace('秒前更新'.decode("utf-8"),''))
							item['update_time'] = update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(server_time-deviation)))
						if re.match(r'\d+分钟前更新'.decode("utf-8"),update_tag):
							deviation = int(update_tag.replace('分钟前更新'.decode("utf-8"),''))*60
							item['update_time'] = update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(server_time-deviation)))
						if re.match(r'\d+小时前更新'.decode("utf-8"),update_tag):
							deviation = int(update_tag.replace('小时前更新'.decode("utf-8"),''))*3600
							item['update_time'] = update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(server_time-deviation)))
						if re.match(r'\d+天前更新'.decode("utf-8"),update_tag):
							deviation = int(update_tag.replace('天前更新'.decode("utf-8"),''))*3600*24
							item['update_time'] = update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(server_time-deviation)))
					except Exception as e:
						print Exception,":",e
					yield item
			else:
				dl_list = sel.xpath('//div[@class="houseList"]/dl[@class="list rel"]')
				for dl_index in range(0,len(dl_list)):
					try:
						item['fang_id'] =fang_id = (re.search(r'\d_\d+',(dl_list[dl_index].xpath('./dd[@class="info rel floatr"]/p[@class="title"]/a/@href').extract()[0]))).group(0)
						item['rank'] =rank = 30*(page_index-1)+dl_index+1
						item['update_tag'] =update_tag = dl_list[dl_index].xpath('./dd[@class="info rel floatr"]/p[@class="gray6 mt10"]/span[@class="ml10 gray9"]/text()').extract()[0]
						if re.match(r'\d+秒前更新'.decode("utf-8"),update_tag):
							deviation = int(update_tag.replace('秒前更新'.decode("utf-8"),''))
							item['update_time'] = update_time = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(server_time-deviation)))
						if re.match(r'\d+分钟前更新'.decode("utf-8"),update_tag):
							deviation = int(update_tag.replace('分钟前更新'.decode("utf-8"),''))*60
							item['update_time'] = update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(server_time-deviation)))
						if re.match(r'\d+小时前更新'.decode("utf-8"),update_tag):
							deviation = int(update_tag.replace('小时前更新'.decode("utf-8"),''))*3600
							item['update_time'] = update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(server_time-deviation)))
						if re.match(r'\d+天前更新'.decode("utf-8"),update_tag):
							deviation = int(update_tag.replace('天前更新'.decode("utf-8"),''))*3600*24
							item['update_time'] = update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(server_time-deviation)))
					except Exception as e:
						print Exception,":",e
					yield item
		except Exception as e:
			print Exception,":",e

		