# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from sqlalchemy import *
from sqlalchemy.orm import *

class AnjukePipeline(object):

	_mysql_path = "mysql+pymysql://root:@192.168.6.8:3306/scrapy_data?charset=utf8"
	engine=create_engine(_mysql_path,echo=False)
	metadata=MetaData(engine)

	def __init__(self):
		
		self.fang_bj_test=Table('fang_bj_test',self.metadata,
				Column('id',Integer,primary_key=True,autoincrement=True),
				Column('fang_id',VARCHAR(20),primary_key=True),
				Column('batch_id',VARCHAR(8),primary_key=True),
				Column('submit_time',VARCHAR(30)),
				Column('schedule_time',VARCHAR(30)),
				Column('received_time',VARCHAR(30)),
				Column('server_time',VARCHAR(30)),
				Column('page_index',VARCHAR(8)),
				Column('rank',VARCHAR(8)),
				Column('update_tag',VARCHAR(30)),
				Column('update_time',VARCHAR(30)),
				mysql_engine='InnoDB',mysql_charset='utf8',
				)
		try:
			self.fang_bj_test.create()
		except Exception as e:
			print Exception,":",e
		
    
	def process_item(self, item, spider):
		
		i = self.fang_bj_test.insert()
		try:
			i.execute(fang_id = item['fang_id'],
					batch_id = item['batch_id'],
					submit_time = item['submit_time'],
					schedule_time = item['schedule_time'],
					received_time = item['received_time'],
					server_time = item['server_time'],
					page_index = item['page_index'],
					rank = item['rank'],
					update_tag = item['update_tag'],
					update_time = item['update_time'])
		except Exception as e:
			print Exception,":",e
		
		return item
