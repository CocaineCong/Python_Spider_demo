# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
# JsonLinesItemExporter:这个是每次调用export_item的时候就吧这个item存储到硬盘当中.
# 坏处是每一个字典是一行,整个文件不是一个满足json格式的文件.
# 好处就是每次处理数据的时候就直接存储到硬盘当中,这样不会消耗内存,数据也比较安全.
class FangPipeline:
    def __init__(self):
        self.newhouse_fp=open('newhouse.json','wb')
        self.esfhouse_fp=open('esfhouse.json','wb')
        self.newhouse_exporter=JsonLinesItemExporter(self.newhouse_fp,ensure_ascii=False)
        self.esfhouse_exporter=JsonLinesItemExporter(self.esfhouse_fp,ensure_ascii=False)



    def process_item(self, item, spider):
        self.newhouse_exporter.export_item(item)  # item就是返回的数据
        self.esfhouse_exporter.export_item(item)  # 用export_item来进行返回
        return item

    def close_spider(self,spider):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()