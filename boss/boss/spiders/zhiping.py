# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from boss.items import BossItem


class ZhipingSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c100010000/?query=python&page=1']
    rules = (
        # 这边是匹配列表页的规则
        # https://www.zhipin.com/c100010000/?query=python&page=3&ka=page-3
        Rule(LinkExtractor(allow=r'.+\?query=python&page=3&ka=page-3'), follow=True),   # 这边是跟进一页一页的网页
        # 这里就是.+  .是匹配任意字符，然后+就是匹配多个 由于有?这个需要用转义字符在前面转义,
        # allow里面的正则表达式是匹配下一页的网页的格式，这个网页的内容不用进行数据的处理，所以就没有callback，只是需要跟进
        # 下面这边是匹配详情页面的规则
        # https://www.zhipin.com/job_detail/f34ed38ae2cb32bf0XB83di0Flc~.html
        Rule(LinkExtractor(allow=r'.+job_detail/[0-9a-zA-Z]+~.html'), callback='parse_job', follow=False),
        # 这个网页就是需要callback 而且不需要跟进
    )

    def parse_job(self, response):
        print(response.text)
        title=response.xpath("//div[@class='name']/h1/text()").get().strip()
        salary=response.xpath("//span[@class='salary']/text()").get().strip()
        job_info=response.xpath("//div[@class='job-primary detail-box']/div[@class='info-primary']/p/text()").get()  #不是直接子元素所以p标签下是要用//
        city=job_info[0]
        work_year=job_info[1]
        education=job_info[2]
        print(title,salary,job_info)
        item=BossItem(title=title,salary=salary,city=city,work_year=work_year,education=education)
        yield item  # 给pipelines








