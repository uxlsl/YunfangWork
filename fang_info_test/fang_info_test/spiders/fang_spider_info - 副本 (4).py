#coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from fang_info_test.items import Fang_Info_Test_Item
from fang_info_test.settings import global_spider
from scrapy import log,FormRequest
import re,time,sys,json,MySQLdb,copy,hashlib
from redis import Redis
from scrapy.http.cookies import CookieJar
from scrapy_redis.spiders import RedisSpider
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
reload(sys)
sys.setdefaultencoding( "utf-8" )


class fang_info_spider(RedisSpider):
	
	spider_id = global_spider.get_spider_id()
	global_spider.spider_id_add()
	name = "fang_info_spider%s"%spider_id
	redis_key = 'HouseNew:start_urls'
	
	allowed_domains = ["fang.com"]

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
			data = json.loads(fetch_one(self.redis_key))
			if (not data) or ("source_url" not in data):
				break
			item = Fang_Info_Test_Item()
			item = self._item_init(item)
			source_route_dict = {}
			if "source" in data:
				source_route_dict['source'] = data['source']
			if "city" in data:
				source_route_dict['city'] = data['city']
			if "type" in data:
				source_route_dict['type'] = data['type']
			source_route_dict['key_route'] = self.redis_key
			item['source_route'] = json.dumps(source_route_dict)
			req = Request(url=data['source_url'],
							method='GET',
							callback=self.parse,
							dont_filter=True)
			if req:
				yield req
				found += 1
			else:
				self.logger.debug("Request not made from data: %s", data)

		if found:
			self.logger.debug("Read %s requests from '%s'", found, self.redis_key)


	def parse(self, response):

		sel = Selector(response)
		
		try:
			fang_info = {'title':'','info':'','desc':'','pic_tab':''}
			url = item['url'] = response.url
			fang_id = item['fang_id'] = (re.search(r'\d+_\d+',url)).group(0)
			item['body'] = (response.body).decode('gbk').encode('utf8')
			yield item

		except Exception as e:
			print Exception,":",e
