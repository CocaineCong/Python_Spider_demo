# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter

class WxappPipeline(object):
    def __int__(self):
        self.fp=open('wxjc.json','wb')
        self.exporter=JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.fp.close()