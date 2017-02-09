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
    anjuke_id = Field()
    deploy_time = Field()
    Cur_url = Field()
    City = Field()
    District = Field()
    Block = Field()
    Estate = Field()
    Title = Field()
    Price = Field()
    Layout = Field()
    Decoration = Field()
    Location = Field()
    Area = Field()
    Unit_Price = Field()
    Years = Field()
    Orientation = Field()
    Downpayment = Field()
    Type = Field()
    Floor = Field()
    Monthly_Payments = Field()
    Desc = Field()
    Agent = Field()
    Agent_Phone = Field()
    Agent_Company = Field()
    pass
