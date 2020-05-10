# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from bmw import settings


class BmwPipeline(object):   #将对象存储的磁盘中
    def __init__(self):
        #os.path.dirname(__file__)  #获取这个文件的路径
        #os.path.dirname(os.path.dirname(__file__))   #获取这个文件的上一级文件
        self.path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'images')   #放在大文件bmw下的images文件中
        if not os.path.exists(self.path):  #如果这个文件夹不存在
            os.mkdir(self.path)  #创建一个文件夹

    def process_item(self, item, spider):  #处理分类
        category=item['category']
        urls=item['urls']
        category_path=os.path.join(self.path,category)   #如果这个文件夹里面没有这个分类的信息，就将其变成
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        for url in urls:
            image_name=url.split('__')[-1]   # 这里是进行切割，有一定的规律在__后面的就是图片的url
            request.urlretrieve(url, os.path.join(category_path,image_name))   # 存入照片
        return item

class BMWImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):    # 这个方法是在发送请求之前调用。这个方法就是发送下载请求的
        request_objs=super(BMWImagesPipeline,self).get_media_requests(item,info)
        for request_obj in request_objs:
            request_obj.item=item
        return request_objs


    def file_path(self, request, response=None, info=None):   # 请求之后调用这个方法
        path=super(BMWImagesPipeline,self).file_path(request,response,info)
        # 这个方法是在图片将要被存储的时候，调用获取到图片的存储路径
        category=request.item.get('category')
        images_store=settings.IMAGES_STORE   # 这边这个已经在setting.当中已经设定好了。就是
        category_path=os.path.join(images_store,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace("full/","")   # 默认的话是有full/的（源码当中有） 下载下来的名字
        image_path=os.path.join(category_path,image_name)
        return image_path
