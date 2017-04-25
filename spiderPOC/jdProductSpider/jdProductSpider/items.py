# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class JdproductspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class productTopicItem(Item):
    name = Field()
    scheduler_id = Field()
    keyword = Field()
    product_code = Field()
    product_brand = Field()
    product_name = Field()
    product_keyword = Field()
    product_title = Field()
    product_cate1 = Field()
    product_cate2 = Field()
    product_cate3 = Field()
    product_attr1 = Field()
    product_attr2 = Field()
    product_attr3 = Field()
    product_addr = Field()
    comment_url = Field()
    comment_count = Field()
    good_count = Field()
    general_count = Field()
    poor_count = Field()
    createtime = Field()
    crawl_time = Field()
    product_from = Field()
    
class productCommentItem(Item):
    name = Field()
    topic_id = Field()
    product_code = Field()
    code = Field()
    guid = Field()
    comment_content = Field()
    comment_stars = Field()
    comment_praise = Field()
    comment_time = Field()
    current_time = Field()
    crawl_time = Field()

class productTagStatisticsItem(Item):
    name = Field()
    topic_id = Field()
    product_code = Field()
    code = Field()
    count = Field()
    tag = Field()
    crawl_time = Field()
    current_time = Field()



