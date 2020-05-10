 # -*- coding: utf-8 -*-
import scrapy
import json

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']   #可以拿到请求头，通过这个网址

    def parse(self, response):
        user_agent=json.loads(response.text)['user-agent']
        yield scrapy.Request(self.start_urls[0],dont_filter=True)
        #防止爬虫去重，这里要设置一个ture的参数，那么就是为了防止只进行一次爬虫操作



