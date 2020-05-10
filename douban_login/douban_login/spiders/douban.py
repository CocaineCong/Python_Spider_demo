# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from PIL import Image


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/login'] # 登陆接口，有fromdata的那个接口
    login_urls = 'http://douban.com/login'

    def parse(self, response):
        fromdata={
            'name': '',
            'password':''
        }
        captcha_url=response.css('img#captcha_image::attr(src').get()  #这里是将验证码抓取到
        if captcha_url :
            captcha=self.regonize_captcha(captcha_url)
            fromdata['captcha-solution']=captcha
            captcha_id=response.xpath("//input[@name='captcha-id]/@value").get()  #得到这个验证码
            fromdata['captcha-id']=captcha_id     #验证码的id
        yield scrapy.FormRequest(url=self.login_urls,fromdata=fromdata,callback=self.parse_after_login)


    def parse_after_login(self,response):
        if response.url=="https://www.douban.com/" :   #如果url等于这个就是说明登陆成功了
            print('login successfully')
        else:
            print('login false')

    def regonize_captcha(self,image_url):
        request.urlretrieve(image_url,'captcha.png')  #保存到磁盘
        image=Image.open('captcha.png')
        image.show()
        captcha=input('请输入验证码')
        return captcha


    def parse_page(self,response):
        with open("douban.html","w",encoding='utf-8') as fp:
            fp.write(response.text)


