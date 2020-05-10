# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter


class BossPipeline(object):    # 保存数据
    def __init__(self):
        self.fp=open('jobs.json','wb')
        self.exporter=JsonLinesItemExporter(self.fp,ensure_ascii=False)

    def process_item(self, item, spider):
        self.exporter.export_item(item)  # 将这写数据传给这个类进行数据的处理
        return item

    def close_spider(self,spider):
        self.fp.close()     # 记得最后要关闭文件

