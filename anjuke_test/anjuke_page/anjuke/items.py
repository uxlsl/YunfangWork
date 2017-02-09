# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class AnjukeItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fang_id = Field()
    batch_id = Field()
    submit_time = Field()
    schedule_time = Field()
    received_time = Field()
    server_time = Field()
    page_index = Field()
    rank = Field()
    update_tag = Field()
    update_time = Field()
    pass
