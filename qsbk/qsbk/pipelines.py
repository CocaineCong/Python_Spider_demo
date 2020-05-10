# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting  不要忘记这个,要去setting里面将其中的ITEM_PIPELINES给取消注释
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 这里是对爬下来的数据格式进行处理


import json

# class QsbkPipeline(object):
#     def __init__(self):
#         self.fp=open("duanzi.json",'w',encoding='utf-8') # 打开文件,传入bytes类型
#
#     def open_spider(self,spider):  #爬虫开始
#         print("爬虫开始")
#
#     def process_item(self, item, spider):  # item是爬虫返回的数据
#         item_json=json.dumps(dict(item),ensure_ascii=False)  #要将item变成字典才能变成json,以为一开始就是,两个列表, 一定要将这个ascii给变成False不然就会是ascii编码
#         self.fp.write(item_json+'\n')
#         return item
#
#     def close_spider(self,spider): #爬虫结束
#         print("爬虫结束了")

# from scrapy.exporters import JsonItemExporter   # 导入json导出器
#
# class QsbkPipeline(object):
#     def __init__(self):
#         self.fp=open("duanzi.json",'wb')  # 以二进制的方式打开
#         self.exporter=JsonItemExporter(self.fp, ensure_ascii=False,encoding='utf-8')  # 创建一个导入的对象
#         self.exporter.start_exporting()  # 开始导入
#
#
#     def open_spider(self,spider):  # 爬虫开始
#         print("爬虫开始")
#
#     def process_item(self, item, spider):  # item是爬虫返回的数据
#         self.exporter.export_item(item)  # 用export_item来进行返回
#         return item
#
#     def close_spider(self,spider): #爬虫结束
#         self.exporter.finish_exporting()
#         self.fp.close()
#         print("爬虫结束了")

from scrapy.exporters import JsonLinesItemExporter   # 导入json导出器，有lines， 一行一行的来，数据量多的话就用这个
from scrapy import Request


class QsbkPipeline(object):
    def __init__(self):
        self.fp=open("duanzi.json",'wb')  # 以二进制的方式打开
        self.exporter=JsonLinesItemExporter(self.fp, ensure_ascii=False,encoding='utf-8')  # 创建一个导入的对象
            # 这边不需要开始导入之类的


    def open_spider(self,spider):  # 爬虫开始
        print("爬虫开始")

    def process_item(self, item, spider):  # item是爬虫返回的数据
        self.exporter.export_item(item)  # 用export_item来进行返回
        return item

    def close_spider(self,spider): #爬虫结束
        # self.exporter.finish_exporting()  也不需要什么结束导入
        self.fp.close()
        print("爬虫结束了")
