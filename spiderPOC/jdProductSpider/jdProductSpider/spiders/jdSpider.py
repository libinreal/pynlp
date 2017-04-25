#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from scrapy.contrib.loader import ItemLoader
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

from jdProductSpider.SpiderUtil import StringUtils
from jdProductSpider.items import productTopicItem, productCommentItem, productTagStatisticsItem  

import json
import scrapy
import time
import datetime

class jdSpider(BaseSpider):
    name = "jd_Spider"
    allowed_domains = ["search.jd.com", "club.jd.com", "item.jd.com"]
    start_key = ['python']
    start_urls = []
    key = ""
    source = "京东商城"
    
    def __init__(self):
        self.key = 'iphone6'
        url = "https://search.jd.com/Search?keyword=%s&enc=utf-8&wq=&pvid=d3b24f41d9df4376a491a7181cdb4173"%(self.key)
        self.start_urls.append(url)
    
    def parse(self, response):
        content = response.body
        content = content.decode('utf-8', 'ignore').encode('gb2312', 'ignore')

        sel = Selector(response)
        product_urls = sel.xpath('//div[@id="J_goodsList"]/ul/li[@class="gl-item"]/div/div[@class="p-img"]/a/@href').extract()
        
        for product_url in product_urls:
            link = product_url
            if product_url.find("http:")<0:
                link = "http:" + link
            
            print link
            yield Request(url=link, callback=self.parse_product_attr)
            #break

    
    def parse_product_attr(self, response):
        sel = Selector(response)
        product_detail = sel.xpath('//div[@id="detail"][@class="ETab"]').extract_first()
        sel_detail = Selector(text=product_detail)
  
        item_topic = productTopicItem()

        item_topic["product_title"] = sel.xpath('//head/title/text()').extract_first();
        item_topic["product_brand"] = sel_detail.xpath('//ul[@id="parameter-brand"]/li/a/text()').extract_first();
        item_topic["product_name"]  = sel_detail.xpath('//ul[@class="parameter2 p-parameter-list"]/li[1]/@title').extract_first();
        item_topic["product_code"]  = sel_detail.xpath('//ul[@class="parameter2 p-parameter-list"]/li[2]/@title').extract_first();
        
        item_topic["product_attr1"] = ""
        item_topic["product_attr2"] = ""
        item_topic["product_attr3"] = ""
        list_attr  = sel_detail.xpath('//ul[@class="parameter1 p-parameter-list"]/li').extract();
        i = 0
        for a in list_attr:
            sel_attr = Selector(text=a)
            i = i + 1
            attr = sel_attr.xpath('//div/p/text()').extract_first()
            if i == 1:
               item_topic["product_attr1"] = attr
            elif i == 2:
                item_topic["product_attr2"] = attr
            elif i == 3:
                item_topic["product_attr3"] = attr
       
        item_topic["comment_url"] = response.url
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        
        item_topic["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        link = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv33667&productId=%s&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0"%(item_topic["product_code"])
    
        print "\n", "="*20, " product list ", "="*20
        print "product_title:\t", item_topic["product_title"] 
        print "product_code:\t", item_topic["product_code"]
        print "product_name:\t", item_topic["product_name"].decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        print "product_brand:\t", item_topic["product_brand"].decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        print "product_attr1:\t", item_topic["product_attr1"].decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        print "product_attr2:\t", item_topic["product_attr2"].decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        print "product_attr3:\t", item_topic["product_attr3"].decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        print "comment_url:\t", item_topic["comment_url"]
        print "\n"
       
        request = Request(url=link, callback=self.parse_product)
        request.meta['item_topic'] = item_topic
        yield request
        

    def parse_product(self, response):
        item_topic = response.meta['item_topic']

        strJson = response.body
        strJson = StringUtils.get_center_part_string(strJson, "(", ")")
        
        strJson = strJson.decode('gb2312', 'ignore').encode('utf-8', 'ignore')
        jsonRoot = json.loads(strJson)
        #print strJson
        
        # item topic
        goodCount = jsonRoot["productCommentSummary"]["goodCount"]
        generalCount = jsonRoot["productCommentSummary"]["generalCount"]
        poorCount = jsonRoot["productCommentSummary"]["poorCount"]
        commentCount = jsonRoot["productCommentSummary"]["commentCount"]
        product_code = self.name + "_" + item_topic["product_code"]
 
        InfoProductTopic = ItemLoader(item=productTopicItem(), response=response)
        InfoProductTopic.add_value('name', "productTopicItem")
        InfoProductTopic.add_value('scheduler_id', 0)
        InfoProductTopic.add_value('keyword', self.key)
        InfoProductTopic.add_value('product_title', item_topic["product_title"])
        InfoProductTopic.add_value('product_code', product_code)
        InfoProductTopic.add_value('product_name', item_topic["product_name"])
        InfoProductTopic.add_value('product_brand', item_topic["product_brand"])
        InfoProductTopic.add_value('product_attr1', item_topic["product_attr1"])
        InfoProductTopic.add_value('product_attr2', item_topic["product_attr2"])
        InfoProductTopic.add_value('product_attr3', item_topic["product_attr3"])
        InfoProductTopic.add_value('product_keyword', self.key)
        InfoProductTopic.add_value('product_addr', "")
        InfoProductTopic.add_value('good_count', goodCount)
        InfoProductTopic.add_value('general_count', generalCount)
        InfoProductTopic.add_value('poor_count', poorCount)
        InfoProductTopic.add_value('comment_url', item_topic["comment_url"])
        InfoProductTopic.add_value('comment_count', commentCount)
        InfoProductTopic.add_value('crawl_time', item_topic["crawl_time"])
        InfoProductTopic.add_value('product_from', self.source)
        
        yield InfoProductTopic.load_item()
        
        # item comment tag
        jsonTags = jsonRoot["hotCommentTagStatistics"]
        for jsonTag in jsonTags:            
            InfoProductTags = ItemLoader(item=productTagStatisticsItem(), response=response)
            InfoProductTags.add_value('name', "productTagStatisticsItem")
            InfoProductTags.add_value('product_code', product_code)
            InfoProductTags.add_value('code', jsonTag["id"])
            InfoProductTags.add_value('tag', jsonTag["name"])
            InfoProductTags.add_value('count', jsonTag["count"])
            InfoProductTags.add_value('crawl_time', item_topic["crawl_time"])

            yield InfoProductTags.load_item()
        
        item_topic["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # item comments
        for page in range(1,100):
            link = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv33667&productId=%s&score=0&sortType=5&page=%d&pageSize=10&isShadowSku=0"%(item_topic["product_code"], page)
            
            request = Request(url=link, callback=self.parse_product_comment)
            request.meta['item_topic'] = item_topic
            yield request
            
        
    def parse_product_comment(self, response):
        item_topic = response.meta['item_topic']
        product_code = self.name + "_" + item_topic["product_code"]

        strJson = response.body
        strJson = StringUtils.get_center_part_string(strJson, "(", ")")
        
        strJson = strJson.decode('gb2312', 'ignore').encode('utf-8', 'ignore')
        jsonRoot = json.loads(strJson)
        
        productId = jsonRoot["productCommentSummary"]["productId"]
        for jsonComment in jsonRoot["comments"]:
            InfoProductComment = ItemLoader(item=productCommentItem(), response=response)
            InfoProductComment.add_value('name', "productCommentItem")
            InfoProductComment.add_value('code', jsonComment["id"])
            InfoProductComment.add_value('product_code', product_code)
            InfoProductComment.add_value('guid', jsonComment["nickname"])
            InfoProductComment.add_value('comment_content', jsonComment["content"])
            InfoProductComment.add_value('comment_stars', jsonComment["score"])
            InfoProductComment.add_value('comment_praise', 0)
            InfoProductComment.add_value('comment_time', jsonComment["creationTime"])
            InfoProductComment.add_value('crawl_time', item_topic["crawl_time"])
            
            yield InfoProductComment.load_item()
            


        
        
     
        
        

        
    
    
