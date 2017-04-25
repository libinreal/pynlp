#coding=utf-8
'''
@author: nancheng
'''
from BeautifulSoup import BeautifulSoup
import logging
import scrapy
from scrapydDemo.items import  *
class Spider_Two(scrapy.Spider):
    name="Spider_Two"
    allowed_domains = ["baidu.com"]
    start_urls = [
       "http://tieba.baidu.com/p/1037876907?see_lz=1",
    ] 
    def parse(self,response):
        logging.info("==爬虫Spider_Two的 parse start!==")
        item=ImageItem()
        infos=response.xpath('//cc/div/img')
        for info in infos:
            item['image_urls']=info.xpath("@src").extract()
            yield item

