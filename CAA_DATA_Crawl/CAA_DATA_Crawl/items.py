# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item

class CaaDataCrawlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Project_ID = Field()
    Project_Name = Field()
    City_Name = Field()
    Area_Code = Field()
    Area_Name = Field()
    Address = Field()
    Price_Avg = Field()

    pass
