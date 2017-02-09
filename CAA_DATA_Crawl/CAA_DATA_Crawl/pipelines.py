# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from sqlalchemy import *
from sqlalchemy.orm import *

class CaaDataCrawlPipeline(object):

    _mysql_path = "mysql+pymysql://root:@192.168.6.8:3306/scrapy_data?charset=utf8"
    engine=create_engine(_mysql_path,echo=False)
    metadata=MetaData(engine)


    def __init__(self):
        self.CAA_DATA_Tab=Table('CAA_DATA_Tab',self.metadata,
                Column('id',Integer,primary_key=True,autoincrement=True),
                Column('Project_ID',VARCHAR(60),primary_key=True),
                Column('Project_Name',VARCHAR(60),index=True),
                Column('City_Name',VARCHAR(30),index=True),
                Column('Area_Code',VARCHAR(30),index=True),
                Column('Area_Name',VARCHAR(30),index=True),
                Column('Address',VARCHAR(255)),
                Column('Price_Avg',DECIMAL(10,2),index=True),
                mysql_engine='InnoDB',mysql_charset='utf8',
                )
        try:
            self.CAA_DATA_Tab.create()
        except Exception as e:
            print Exception,":",e  

  
    def process_item(self, item, spider):
        i = self.fang_bj_test.insert()
        try:
            i.execute(Project_ID=item['Project_ID'],
                        Project_Name=item['Project_Name'],
                        City_Name=itm['City_Name'],
                        Area_Name=item['Area_Name'],
                        Area_Code=item['Area_Code'],
                        Address=item['Address'],
                        Price_Avg=item['Price_Avg'])
        except Exception as e:
            print Exception,":",e
        
        return item
