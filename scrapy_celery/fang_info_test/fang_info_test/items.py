# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class Fang_Info_Test_Item(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    fang_id = Field()
    body = Field()
    version_time = Field()
    source_route = Field()

    pass
