# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem

class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']
    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'),follow=True),
    # Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),
    # 后面加上\d匹配数字,  callback='parse_item', 是解析爬取这个页面当中的信息,但是我们需要的是这个页面里面的页面的信息
        Rule(LinkExtractor(allow=r'.+article-.+\.html'),callback="parse_item",follow = False)
        # Rule(LinkExtractor(allow=r'.+article-.+\.html'),callback="parse_item",follow = False)
    # 第一个.是前面任意的,第二个是匹配任意字符,第三个前面有转义是普通的
            )


    def parse_item(self, response):
        title=response.xpath("//h1[@class='ph']/text()").get()
        author_p=response.xpath("//p[@class='authors']")
        author=author_p.xpath(".//a/text()").get()
        pub_time=author_p.xpath(".//span/text()").get()
        article_content=response.xpath("//td[@id='article_content']//text()").getall()
        content="".join(article_content)
        #print('author:%s/pub_time:%s' % (author,pub_time))
        item=WxappItem(title=title,author=author,pub_time=pub_time,content=content)  #对数据进行处理
        yield item #暂停一下，返回过去