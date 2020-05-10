# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
from qsbk.items import QsbkItem

class QskbSpiderSpider(scrapy.Spider):
    name = 'qs_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain="https://www.qiushibaike.com"

    def parse(self, response):
        # 列表
        duanzidivs=response.xpath("//div[@class='col1 old-style-col1']/div")   # 这边的这个类型是SelectorList
        for duanzidiv in duanzidivs:
            author = duanzidiv.xpath(".//h2/text()").get()    # 这边将其变成unicode的类型.
            content = duanzidiv.xpath(".//div[@class='content']//text()").getall()  # 这里getall就是会其中所有的信息提取出来,返回列表
            content="".join(content).strip()        # 将列表放进去，就会自动将其变成字符串,然后要将其中的空格删去
            item=QsbkItem(author=author,content=content)   #返回到定义的类当中,那个类就是处理数据类型的,固定参数就不会有其他的数据渗入
            yield item
            # duanzi={"author":author,"content":content}
            # yield duanzi #暂停一下,将duanzi返回
        next_url=response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get() # last只是找到li标签的最后一个标签
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url,callback=self.parse)  # 执行方法 同一个类中调用其他的方法时需要加self
            # yield 只是暂停一下，先返回还会继续执行, return是返回就结束了。
            # 这边这个base_domain不是本函数的方法，是属于类的，所以要加上self,而next_url是这个方法所以不用
            # 而parse是类的方法,不是自己定义的方法,所以要加上self
