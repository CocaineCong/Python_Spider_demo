# -*- coding: utf-8 -*-
import scrapy
import json

class IpporgSpider(scrapy.Spider):
    name = 'ipporg'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        orange=json.loads(response.text)['origin']

class IPProxyDownloadMiddleware(object):  # 代理ip


    def process_request(self,request,spider):
        pass

