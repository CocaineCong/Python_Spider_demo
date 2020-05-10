# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi  # 这个是专门用来做数据库的
from pymysql import cursors


class JianshuPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'jianshu2',
            'charset': 'utf8',  # mysql的操作,mysql的编码方式
        }
        self.conn = pymysql.connect(**dbparams)  # 传入参数
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['content'], item['author'],
                                       item['avatar'], item['pub_time'], item['origin_url']
                                       , item['article_id']
                                       ))
        self.conn.commit()  # 这边是提交
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id) 
                            value (null,%s,%s,%s,%s,%s,%s,%s)
            """  # 放进数据库中的操作
            return self._sql
        return self._sql


class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'jianshu2',
            'charset': 'utf8',  # mysql的操作,mysql的编码方式
            'cursorclass': cursors.DictCursor  # 这边就是游标的类
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # 加载模块 进行连接
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id) 
                        value (null ,%s,%s,%s,%s,%s,%s,%s)  
            """  # 这个表名就是article 如果没有的话就是创建这些表头，如果有的话就是要求将其中直接返回数值
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item, spider)  # 这个runInteraction会将爬取过程变成异步的形式

        defer.addErrback(self.handle_error)  # 处理错误的函数

    def insert_item(self, cursor, item):
        self.cursor.execute(self.sql, (item['title'], item['content'], item['author'],
                                       item['avatar'], item['pub_time'], item['origin_url']
                                       , item['article_id']
                                       ))

    def handle_error(self, error, item, spider):  # 错误处理函数，传入错误，数据，还有就是哪个爬虫
        print("=" * 20 + "Error" + "=" * 20)
