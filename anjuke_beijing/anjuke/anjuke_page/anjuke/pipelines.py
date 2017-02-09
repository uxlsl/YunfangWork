# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import MySQLdb

#************iniitialize insert option****************#
sql = "INSERT INTO anjuke (`Cur_url`,`City`,`District`,`Block`,`Estate`,`Title`,`Price`,`Layout`,`Decoration`,`Location`,`Area`,`Unit_Price`,`Years`,`Orientation`,`Downpayment`,`Type`,`Floor`,`Monthly_Payments`,`Desc`,`Agent`,`Agent_Phone`,`Agent_Company`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


class AnjukePipeline(object):

	def __init__(self):
		global sql
		#self.wb = Workbook()
		#self.ws = self.wb.active
		#self.ws.append(['URL','brand_year_car_version_part_sub','info','desc','price','URL_pic'])
		self.db = MySQLdb.connect("192.168.10.31","root","",charset='utf8')
		self.db.select_db('scrapy_data')
		self.cur = self.db.cursor()
		
	def process_item(self, item, spider):
		line = [item['Cur_url'],
				item['City'],
				item['District'],
				item['Block'],
				item['Estate'],
				item['Title'],
				item['Price'],
				item['Layout'],
				item['Decoration'],
				item['Location'],
				item['Area'],
				item['Unit_Price'],
				item['Years'],
				item['Orientation'],
				item['Downpayment'],
				item['Type'],
				item['Floor'],
				item['Monthly_Payments'],
				item['Desc'],
				item['Agent'],
				item['Agent_Phone'],
				item['Agent_Company']]
		self.cur.execute(sql,line)
		self.db.commit()
		#line = [item['Url_crawl'],item['brand_year_car_version_part_sub']]
		#self.ws.append(line)
		#self.wb.save('E:/rockauto_link_s.xlsx')
		return item

	#def spider_closed(self,spider):
	#	self.file.close()
