# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewHouseItem, ESFHouseItem

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")  # 这边就是说class没有样式的东西
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s", "", province_text)  # 这边使用正则表达式将其中的换行符替换掉
            if province_text:
                province = province_text
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                # 创建新房的url连接
                url_model = city_url.split('//')  # 用//来进行分割
                scheme = url_model[0]
                domain = url_model[1]
                if 'bj.' in domain:
                    new_house_url = 'https://newhouse.fang.com/house/s/'
                    esf_url = "https://esf.fang.com/?ctm=1.bj.xf_search.head.143"  # 因为北京的url里面没有bj所以下面的这种方法是行不通的
                else:
                    new_house_url = scheme + '//' + 'newhouse.' + domain + "house/s/"
                    # 构建二手房的url链接
                    esf_url = scheme + '//' + 'esf.' + domain  # 二手房的部分链接可能不太行

                yield scrapy.Request(url=new_house_url, callback=self.parse_newhouse, meta={"info": (province, city)})

            yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={"info": (province, city)})


    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nhouse_list_content')]/ul/li")  # 这边这个就是包含了这个类标签的div元素
        for li in lis:
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            # house_type_list=li.xpath(".//div[contains(@class,'house_type clearfix')]//text()").getall()  #这种方法不太行
            # house_type_list=list(map(lambda x:re.sub(r"\s","",x),house_type_list))  #将其中的空格转换掉
            house_type_list = li.xpath(".//div[contains(@class,'house_type clearfix')]/a/text()").getall()
            house_type_list = list(map(lambda x: re.sub(r"\s", "", x), house_type_list))
            rooms = list(
                filter(lambda x: x.startswith("1" or "2" or "3" or "4" or "5"), house_type_list))  # 过滤掉不是以这些数字开头的
            area = li.xpath(".//[contains(@class,'house_type')]/text()").getall()
            area = "".join(area)
            area = re.sub(r"\s|—|/", "", area)  # 将括号里面的东西都替换成空字符
            address = li.xpath(".//div[@class='address']/a/@title").get  # 获取地址
            district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
            district = re.search(r".*\[(.+)\].*", district_text).group(1)  # 将其分组成前后两组，有一些地区是没有起前的东西的，所以就是要将其单独处理
            sale = li.xpath(".//div[contains(@class,'fangyuan pr')]/span/text()").get()
            price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r"\s|广告", "", price)  # 将空白字符串和广告全部变成一个空的字符串
            origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            origin_url = "https:" + origin_url
            item = NewHouseItem(name=name, rooms=rooms, area=area, address=address, district=district, sale=sale,
                                price=price, origin_url=origin_url, province=province, city=city)
            yield item

        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=response.url+next_url, callback=self.parse_newhouse,meta={"info": (province, city)})
            # 将值返回的函数值进行请求,调用给自己 url的urljoin是保证url的完整

    def parse_esf(self, response):
        province, city = response.meta.get('info')
        dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:
            item = ESFHouseItem(province=province, city=city)
            name = dl.xpath(".//p[@class='add_shop']/a/@title").get()
            infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
            infos = list(map(lambda x: re.sub(r"\s", "", x), infos))
            for info in infos:   # 有一些信息没有，所以就是要单独分析讨论
                if "厅" in info:
                    item['rooms'] = info
                elif "层" in info:
                    item['floor'] = info
                elif "向" in info:
                    item['toward'] = info
                elif "㎡" in info:
                    item['area']=info
                else:
                    item['year'] = info.replace("建筑年代: ", "")
            address=dl.xpath(".//p[@class='add_shop']/span/text()").get()
            item['address']=address
            price=dl.xpath(".//dd[@class='price_right']/span[1]/b/text()").get()
            item['price']=price
            unit=dl.xpath(".//dd[@class='price_right']/span[2]/text()").get()
            item['unit']=unit
            origin_url=dl.xpath(".//h4[@class='clearfix']/a/@href").get()
            origin_url=response.url+origin_url
            item['origin_url']=origin_url
            yield item
        next_url=response.xpath("//div[@id='list_D10_15']/p[1]/a/@href").get() # 用了get之后就会从SelectorList类型变成一个str类型
        yield scrapy.Request(url=response.url+next_url,callback=self.parse_esf,meta={"info":(province,city)})
                                # 可以将其中的url变成完整的东西

