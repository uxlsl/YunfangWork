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
	redis_key = 'anjuke_beijing_spider:data_url'
	
	allowed_domains = ["anjuke.com"]

	def _item_init(self,item):

		item['anjuke_id'] = ''
		item['deploy_time'] = ''
		item['Cur_url'] = ''
		item['City'] = ''
		item['District'] = ''
		item['Block'] = ''
		item['Estate'] = ''
		item['Title'] = ''
		item['Price'] = ''
		item['Layout'] = ''
		item['Decoration'] = ''
		item['Location'] = ''
		item['Area'] = ''
		item['Unit_Price'] = ''
		item['Years'] = ''
		item['Orientation'] = ''
		item['Downpayment'] = ''
		item['Type'] = ''
		item['Floor'] = ''
		item['Monthly_Payments'] = ''
		item['Desc'] = ''
		item['Agent'] = ''
		item['Agent_Phone'] = ''
		item['Agent_Company'] = ''

		return item



	def parse(self,response):

		sel = Selector(response)
		item = AnjukeItem()
		item = self._item_init(item)

		try:
			hourse_info = sel.xpath('//h4[@class="block-title houseInfo-title"]/span/text()').extract()[0]
			item['anjuke_id'] = (re.search(r"\d{9,}", hourse_info)).group(0)
			item['deploy_time'] = (re.search(r"\d{4}%s\d{2}%s\d{2}%s"%('年'.decode("utf-8"),'月'.decode("utf-8"),'日'.decode("utf-8")), hourse_info)).group(0)
		except Exception as e:
			print Exception,":",e
		try:
			item['Cur_url'] = response.url
		except Exception as e:
			print Exception,":",e
		try:
			item['City'] = (sel.xpath('//*[@id="content"]/div[1]/a[2]/text()').extract()[0]).replace('二手房'.decode("utf8"),'')
		except Exception as e:
			print Exception,":",e
		try:
			item['District'] = (sel.xpath('//*[@id="content"]/div[1]/a[3]/text()').extract()[0]).replace('二手房'.decode("utf8"),'')
		except Exception as e:
			print Exception,":",e
		try:
			item['Block'] = (sel.xpath('//*[@id="content"]/div[1]/a[4]/text()').extract()[0]).replace('二手房'.decode("utf8"),'')
		except Exception as e:
			print Exception,":",e
		try:
			item['Estate'] = sel.xpath('//*[@id="content"]/div[1]/a[4]/text()').extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Title'] = sel.xpath('//*[@id="content"]/div[@class="wrapper"]/h3[@class="long-title"]/text()').extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Price'] = (re.compile(r'<[^>]+>',re.S)).sub('',sel.xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[1]').extract()[0])
		except Exception as e:
			print Exception,":",e
		try:
			item['Layout'] = (sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/text()'%'房型：'.decode("utf8")).extract()[0]).replace('\n','').replace('\t','')
		except Exception as e:
			print Exception,":",e
		try:
			item['Decoration'] = sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/text()'%'装修程度：'.decode("utf8")).extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Location'] = (re.compile(r'<[^>]+>',re.S)).sub('',sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/p'%'位置：'.decode("utf8")).extract()[0]).replace('\n','').replace('\t','')
		except Exception as e:
			print Exception,":",e
		try:
			item['Area'] = sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/text()'%'面积：'.decode("utf8")).extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Unit_Price'] = sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/text()'%'房屋单价：'.decode("utf8")).extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Years'] = sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/text()'%'年代：'.decode("utf8")).extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Orientation'] = sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/text()'%'朝向：'.decode("utf8")).extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Downpayment'] = (sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/text()'%'参考首付：'.decode("utf8")).extract()[0]).replace('\n','').replace('\t','')
		except Exception as e:
			print Exception,":",e
		try:
			item['Type'] = sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/text()'%'类型：'.decode("utf8")).extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Floor'] = sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/text()'%'楼层：'.decode("utf8")).extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Monthly_Payments'] = sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[1]/div/dl[dt="%s"]/dd/span/text()'%'参考月供：'.decode("utf8")).extract()[0]
		except Exception as e:
			print Exception,":",e
		try:
			item['Desc'] = (re.compile(r'<[^>]+>',re.S)).sub('',sel.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/div/div[3]/div/div').extract()[0])
		except Exception as e:
			print Exception,":",e
		try:
			item['Agent'] = sel.xpath('//p[@class="broker-name"]/a/text()').extract()[0]
		except Exception as e:
			print Exception,":",
		try:
			item['Agent_Phone'] = (sel.xpath('//p[@class="broker-mobile"]/text()').extract()[0]).replace(' ','')
		except Exception as e:
			print Exception,":",e
		try:
			item['Agent_Company'] = sel.xpath('//div[@class="broker-company"]/a[1]/text()').extract()[0]
		except Exception as e:
			print Exception,":",e
		yield item
