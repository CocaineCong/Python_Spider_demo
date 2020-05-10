# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    province = scrapy.Field()    # 省份
    city = scrapy.Field()        # 城市
    name = scrapy.Field()        # 小区名字
    price = scrapy.Field()       # 价格
    rooms = scrapy.Field()       # 几居,这是一个列表
    area = scrapy.Field()        # 面积
    address = scrapy.Field()     # 地址
    district = scrapy.Field()    # 行政区
    sale = scrapy.Field()        # 是否在售
    origin_url = scrapy.Field()  # 详细页面的url


class ESFHouseItem(scrapy.Item):
    province = scrapy.Field()    # 省份
    city = scrapy.Field()        # 城市
    name = scrapy.Field()        # 小区名字
    price = scrapy.Field()       # 价格
    unit=scrapy.Field()          # 单价
    rooms = scrapy.Field()       # 几居,这是一个列表
    floor = scrapy.Field()       # 几层
    area = scrapy.Field()        # 面积
    toward = scrapy.Field()      # 朝向
    year = scrapy.Field()        # 年代
    address = scrapy.Field()     # 地址
    district = scrapy.Field()    # 行政区
    sale = scrapy.Field()        # 是否在售
    origin_url = scrapy.Field()  # 详细页面的url