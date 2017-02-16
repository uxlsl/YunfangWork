# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class XxjrInfoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    City_name = Field()
    City_id = Field()
    Estate_name = Field()
    Estate_id = Field()
    Building_name = Field()
    Building_id = Field()
    House_name = Field()
    House_id = Field()

    pass
