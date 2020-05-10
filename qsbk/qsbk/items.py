# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#处理数据类型
import scrapy


class QsbkItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    content = scrapy.Field()
    pass
