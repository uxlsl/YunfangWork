# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from sqlalchemy import *
from sqlalchemy.orm import *

class XxjrInfoPipeline(object):

    _mysql_path = "mysql+pymysql://root:@192.168.6.8:3306/scrapy_data?charset=utf8"
    engine=create_engine(_mysql_path,echo=False)
    metadata=MetaData(engine)

    def __init__(self):
        
        self.xxjr_info=Table('xxjr_info',self.metadata,
                Column('id',Integer,primary_key=True,autoincrement=True),
                Column('City_name',VARCHAR(20)),
                Column('City_id',VARCHAR(20)),
                Column('Estate_name',VARCHAR(50)),
                Column('Estate_id',VARCHAR(20)),
                Column('Building_name',VARCHAR(60)),
                Column('Building_id',VARCHAR(20)),
                Column('House_name',VARCHAR(70)),
                Column('House_id',VARCHAR(20)),
                mysql_engine='InnoDB',mysql_charset='utf8'
                )
        try:
            self.xxjr_info.create()
        except Exception as e:
            print Exception,":",e
        
    
    def process_item(self, item, spider):
        
        i = self.xxjr_info.insert()
        try:
            i.execute(City_name = item['City_name'],
                    City_id = item['City_id'],
                    Estate_name = item['Estate_name'],
                    Estate_id = item['Estate_id'],
                    Building_name = item['Building_name'],
                    Building_id = item['Building_id'],
                    House_name = item['House_name'],
                    House_id = item['House_id'])
        except Exception as e:
            print Exception,":",e
        
        return item
