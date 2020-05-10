# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem

class Bwm5Spider(scrapy.Spider):
    name = 'bwm5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/202.html']

    def parse(self, response):
        # SelectorList->list
        uiboxs=response.xpath("//div[@class='uibox']")[1:]  # 第一个全景图片获取不了就把第零个给切掉
        for uibox in uiboxs :
            category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()  # 分类
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            urls_ = list(map(lambda url:'https://car2.autoimg.cn'+url ,urls))
            item=BmwItem(category=category,image_urls=urls_)
            yield item  #返回给item 给item