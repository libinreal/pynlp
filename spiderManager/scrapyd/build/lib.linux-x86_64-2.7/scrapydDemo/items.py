# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyddemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class TieziItem(scrapy.Item):
    url=scrapy.Field()
    author=scrapy.Field()
    content=scrapy.Field()
    title=scrapy.Field()
class ImageItem(scrapy.Item):
    image_urls=scrapy.Field()
    image=scrapy.Field()
