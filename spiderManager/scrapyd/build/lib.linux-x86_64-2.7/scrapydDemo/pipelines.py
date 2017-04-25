# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from  pymongo import *
from scrapydDemo.items import  *
# import scrapydDemo.spiders.Spider_One
# import scrapydDemo.spiders.Spider_Two
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import logging
class ScrapyddemoPipeline(object):
    def process_item(self, item, spider):
#         if isinstance(spider, Spider_One):
        self.tieba.insert_one(dict(item))
        return item
    def open_spider(self,spider):
   # if isinstance(spider, Spider_One):
        logging.info("==open_spider调用成功==")
        self.connect_mongodb()
    def close_spider(self,spider):
        #if isinstance(spider, Spider_One):
        self.client.close()
        logging.info("==close_spider调用成功==")
    def connect_mongodb(self):
        logging.info("==ScrapyddemoPipeline初始化 创建mongodb数据库连接==")
        self.client = MongoClient()
        self.db =self.client.tieba
        self.tieba = self.db.tieba
class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        logging.info("===info in get_media_requests is"+str(info) +"===")
        if isinstance(item, ImageItem):
            for image_url in item['image_urls']:
                    yield scrapy.Request(url=image_url)
    def item_completed(self, results, item, info):
        logging.info("===info in item_completed is"+str(info) +"===")
        if isinstance(item, ImageItem):
            image = [x['path'] for ok, x in results if ok]
            if not image:
                    raise DropItem("===Item contains no images item里面没有image item==")
            item['image'] = image
            return item