# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import ArticleItem

class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (       # *这个是可有可无as
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-zA-z]{12}.*'), callback='parse_detail', follow=True),   #这边是通过ajax来爬取下来的
    )

    def parse_detail(self, response):
        title=response.xpath("//h1[@class='_1RuRku']/text()").get()
        avatar=response.xpath("//a[@class='_1OhGeD']/img/@src").get()
        author=response.xpath("//span[@class='FxYr8x']/a/text()").get()
        pub_time=response.xpath("//div[@class='s-dsoj']/time/text()").get()
        content=response.xpath("//article[@class='_2rhmJa']").get()
        #url=https://www.jianshu.com/p/c393e145d6a7
        urll=response.url
        origin_url=urll
        article_id=urll.split('/')[-1]
        content=response.xpath("//div[@class='show-content']").get()
        work_count=response.xpath("//span[@class='wordage']/text()").get()
        comment_count=response.xpath("//span[@class='comments-count']/text()").get()
        read_count=response.xpath("//span[@class='read-count']/text()").get()
        like_count=response.xpath("//span[@class='likes-count']/text()").get()
        subjects=response.xpath("//div[@class='include-collection']/a/div/text()").getall()  # 返回的是列表，mysql存储不了列表，只能是变成字符串】
        subject=",".join(subjects)




        item=ArticleItem(
            title=title,
            avatar=avatar,
            author=author,
            pub_time=pub_time,
            origin_url=response.url,
            article_id=article_id,
            content=content,
            subject=subject,
            work_count=work_count,
            comment_count=comment_count,
            read_count=read_count,
            like_count=read_count
        )
        yield item