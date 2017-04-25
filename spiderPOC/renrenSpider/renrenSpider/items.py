# s*- coding: utf-8 -*-
########################################################################
# author:
#    chaosju 
#
# decription:
#     Define here the models for your scraped items
#
# help documentation:
#     http://doc.scrapy.org/en/latest/topics/items.html
#######################################################################
from scrapy.item import Item, Field


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
    
    
class articleCommentItem(Item):
    name = Field()
    article_id = Field()
    article_code = Field()
    guid = Field()
    comment_content = Field()
    comment_stars = Field()
    comment_praise = Field()
    comment_time = Field()
    current_time = Field()
    crawl_time = Field()

