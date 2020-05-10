# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):   # 储存数据的
    # define the fields for your item here like:
    # name = scrapy.Field()
    # item=BossItem(title=title,salary=salary,city=city,work_year=work_year,education=education)
    title = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    work_year = scrapy.Field()
    education = scrapy.Field()
