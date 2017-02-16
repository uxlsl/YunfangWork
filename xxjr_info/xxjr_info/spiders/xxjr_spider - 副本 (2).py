#coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from xxjr_info.items import XxjrInfoItem
from xxjr_info.settings import global_spider,DEFAULT_REQUEST_HEADERS
from scrapy import log,FormRequest
import os,re,time,sys,json,MySQLdb,copy,urllib
from scrapy.http.cookies import CookieJar
from redis import Redis
from scrapy_redis.spiders import RedisSpider
reload(sys)
sys.setdefaultencoding( "utf-8" )


class xxjr_info_spider(RedisSpider):
    
    spider_id = global_spider.get_spider_id()
    global_spider.spider_id_add()
    name = "xxjr_info_spider%s"%spider_id
    redis_key = 'xxjr:seed_info'
    
    allowed_domains = ["app.xxjr.com",]

    city_info = {}
    json_text = open('/home/chiufung/xxjr_info/xxjr_info/city_info.json','r').read()
    city_info_json = (json.loads(json_text,encoding='utf-8'))['attr']['allCity']
    for key in city_info_json:
    	for item_dict in city_info_json[key]:
    		city_info[item_dict['cityName']] = item_dict['cityId']

    print "success init city_info \n",city_info

    headers = DEFAULT_REQUEST_HEADERS


    def _item_init(self,item):

        item['City_name'] = ''
        item['City_id'] = ''
        item['Estate_name'] = ''
        item['Estate_id'] = ''
        item['Building_name'] = ''
        item['Building_id'] = ''
        item['House_name'] = ''
        item['House_id'] = ''

        return item

    def next_requests(self):

        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET')
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                # Queue empty.
                break
            data_dict = json.loads(data,encoding='utf-8')
            if not (data_dict.has_key('cityName') and data_dict.has_key('keyWord')):
            	# Data is unavailable.
            	break
            req = self._make_request_from_keyword(data_dict)
            if req:
                yield req
                found += 1
            else:
                print "Request not made from data: %s"%data

        if found:
            print"Read %s requests from '%s'"%(found, self.redis_key)


    def _get_cityID(self,cityName):

    	try:
    		return (cityName,self.city_info[cityName])
    	except Exception as e:
    		print Exception,":",e
    		return None
    	


    def _make_request_from_keyword(self,data_dict):

        url = 'https://app.xxjr.com/cpQuery/app/xxjrEval/queryEstate'
        cityName = data_dict['cityName']
        keyWord = data_dict['keyWord']
        cityTran = self._get_cityID(cityName)
        if cityTran:
            item = XxjrInfoItem()
            item = self._item_init(item)
            item['City_name'],item['City_id'] = cityTran
            city_id = item['City_id']
            if city_id in [4,9,189,121,17,74,3,43,45,
                            56,25,44,136,70,77,41,5,72,54,150,82,2,35,8,46,161,94,76,23,125,37,10,
                            16,40,26,49,71,1,97,7,29,24,88,58,55,47,83,38,6,101,84,22,53,52]:
                re_body = {'keyWord': keyWord, 'cityCode': str(city_id)}
                print re_body
                return  Request(url=url,
                                headers=self.headers,method='POST',dont_filter=True,
                                body=urllib.urlencode(re_body),
                                meta = {'item' : item,'city_id':city_id}, 
                                callback = self.parse_estate_page)
            else:
                return



    def parse_estate_page(self, response) :
        
        print response.body
        if response.body:
        	response.info_dict = json.loads(response.body)
        	if response.info_dict['attr']['names'] != [] and response.info_dict['attr']['ids'] != []:
        		name_list = response.info_dict['attr']['names']
        		ids_list = response.info_dict['attr']['ids']
        		for id_index in xrange(min(len(name_list),len(ids_list))):
        			try:
        				url = 'https://app.xxjr.com/cpQuery/app/xxjrEval/queryBuilding'
        				item = copy.deepcopy(response.meta['item'])
        				item['Estate_name'] = name_list[id_index]
        				Estate_id = item['Estate_id'] = ids_list[id_index]
        				city_id = response.meta['city_id']
        				re_body = {'keyWord': '', 'cityCode': str(city_id)}
        				re_body['estateId'] = Estate_id
        				print re_body
        				yield  Request(url=url,
			                            headers=self.headers,method='POST',dont_filter=True,
			                            body=urllib.urlencode(re_body),
			                            meta = {'item' : item,'city_id':city_id}, 
			                            callback = self.parse_building_page)
        			except Exception as e:
        				print Exception,":",e
        	else:
        		return
        else:
        	return



    def parse_building_page(self, response) :
        
        print response.body
        if response.body:
        	response.info_dict = json.loads(response.body)
        	if response.info_dict['attr']['names'] != [] and response.info_dict['attr']['ids'] != []:
        		name_list = response.info_dict['attr']['names']
        		ids_list = response.info_dict['attr']['ids']
        		for id_index in xrange(min(len(name_list),len(ids_list))):
        			try:
        				url = 'https://app.xxjr.com/cpQuery/app/xxjrEval/queryHouse'
        				item = copy.deepcopy(response.meta['item'])
        				item['Building_name'] = name_list[id_index]
        				Building_id = item['Building_id'] = ids_list[id_index]
        				city_id = response.meta['city_id']
        				re_body = {'keyWord': '', 'cityCode': str(city_id)}
        				re_body['buildId'] = Building_id
        				print re_body
        				yield  Request(url=url,
			                            headers=self.headers,method='POST',dont_filter=True,
			                            body=urllib.urlencode(re_body),
			                            meta = {'item' : item}, 
			                            callback = self.parse_house_page)
        			except Exception as e:
        				print Exception,":",e
        	else:
        		return
        else:
        	return




    def parse_house_page(self, response) :
        
        print response.body
        if response.body:
        	response.info_dict = json.loads(response.body)
        	if response.info_dict['attr']['names'] != [] and response.info_dict['attr']['ids'] != []:
        		name_list = response.info_dict['attr']['names']
        		ids_list = response.info_dict['attr']['ids']
        		for id_index in xrange(min(len(name_list),len(ids_list))):
        			try:
        				item = copy.deepcopy(response.meta['item'])
        				item['House_name'] = name_list[id_index]
        				House_id = item['House_id'] = ids_list[id_index]
        				yield  item
        			except Exception as e:
        				print Exception,":",e
        	else:
        		return
        else:
        	return