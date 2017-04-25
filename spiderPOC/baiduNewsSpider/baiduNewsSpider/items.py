# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class BaidunewsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class articleTopicItem(Item):
    name = Field()
    article_id = Field()
    article_key = Field()
    article_name = Field()
    article_url = Field()
    article_content = Field()
    article_time = Field()
    crawl_time = Field()
    article_from = Field()
    click_num = Field()
    reply_num = Field()
    praise_num = Field()
    article_author = Field()
    image_urls = Field()
    scheduler_id = Field()
    area = Field()

