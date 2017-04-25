#coding=utf-8

import urllib2
import urllib
import cookielib
import re
import HTMLParser

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from scrapy.contrib.loader import ItemLoader
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

from taobaoSpider.SpiderUtil import StringUtils
from taobaoSpider.items import productTopicItem, productCommentItem, productTagStatisticsItem  

import json
import scrapy
import time
import datetime

class tbSpider(BaseSpider):
    name = "taobaoSpider"
    #allowed_domains = ["s.taobao.com", "detail.tmall.com", "login.taobao.com", "pass.tmall.com", ""]
    start_key = ['python']
    start_urls = []
    key = ""
    dic_cookie = {}
    source = "苹果"
    
    def __init__(self):
        self.key = 'iphone6'
        #url = "https://s.taobao.com/search?q=%s&imgfile=&ie=utf8"%(self.key)
        url = "https://s.taobao.com/search?q=%s&imgfile=&ie=utf8&app=detailproduct&through=1"%(self.key)
        self.start_urls.append(url)
    
    def parse(self, response):                                                                                    
        htmlCode = response.body
        strJson = StringUtils.get_json_string(htmlCode, "g_page_config = {", "};")
        #strJson = strJson.decode('gb2312', 'ignore').encode('utf-8', 'ignore')
        strJson = "{" + strJson + "}"
        strJson = strJson.replace("\r", "").replace("\n", "")
        jsonRoot = json.loads(strJson)

        product_data = jsonRoot["mods"]["spuhead"]["data"]
        product_item_list = jsonRoot["mods"]["itemlist"]
        
        product_spu_id = product_data["spuId"]
        product_title = product_data["spuTitle"]
        product_price = product_data["month_sales"]
        product_tag_info = product_data["tag_info"]
        product_params = product_data["params"]
        
        product_auctions = product_item_list["data"]["auctions"]
        
        self.dic_cookie = {}
        
        for auction in product_auctions:
            #print auction
            product_id = auction["nid"]
            product_title = auction["raw_title"]
            product_detail_url = auction["detail_url"]
            product_price = auction["view_price"]
            product_comment_count = auction["comment_count"]
            
            link = urllib.unquote(str(product_detail_url)).decode('utf8')
            if(link.find("http:")<0):
                link = "http:" + link
                
            if not self.dic_cookie:
                self.dic_cookie = self.get_cookie(self.start_urls[0], link)
                #print self.dic_cookie 
    
            request = Request(url=link, cookies=self.dic_cookie, callback=self.parse_product_topic)
            yield request
            
            #break

    def parse_product_topic(self, response):
        print "********** parse_product_topic **********"
        #print response.body.decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        sel = Selector(response)
        product_title = sel.xpath('//div[@class="tb-detail-hd"]/h1/a/text()').extract_first()
        product_scheduler_id = 0
        product_keyword = self.key
        product_attr_content = sel.xpath('//div[@class="attributes-list"]').extract_first()
        
        #print "product_attr_content:", product_attr_content.decode('utf-8', 'ignore').encode('gb2312', 'ignore')

        product_name = ""
        product_attr1 = ""
        product_attr2 = ""
        product_attr3 = ""
        try:
            product_name = sel.xpath('//ul[@id="J_AttrUL"]/li[4]/text()').extract_first()
            if product_name.find("：")>0:
                product_name = product_name.split("：")[1]
                
            product_attr1 = sel.xpath('//ul[@id="J_AttrUL"]/li[3]/text()').extract_first()
            if product_attr1.find("：")>0:
                product_attr1 = product_attr1.split("：")[1]
               
            product_attr2 = sel.xpath('//ul[@id="J_AttrUL"]/li[6]/text()').extract_first()
            if product_attr2.find(":")>0:
                product_attr2 = product_attr2.split(":")[1]

            product_attr3 = sel.xpath('//ul[@id="J_AttrUL"]/li[8]/text()').extract_first()
            if product_attr3.find(":")>0:
                product_attr3 = product_attr3.split(":")[1]
            
        except:
            pass
        

        htmlCode = response.body
        strJson = StringUtils.get_json_string(htmlCode, "TShop.Setup(", ");")
        strJson = strJson.decode('gb2312', 'ignore').encode('utf-8', 'ignore')
        strJson = strJson.replace("\r", "").replace("\n", "")
        #print strJson.decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        jsonRoot = json.loads(strJson)
        brand = jsonRoot["itemDO"]["brand"]
        parser = HTMLParser.HTMLParser()

        product_brand = parser.unescape(brand)
        product_title = jsonRoot["itemDO"]["title"]
        product_spuid = jsonRoot["itemDO"]["spuId"]
        product_addr = jsonRoot["itemDO"]["prov"]
        product_item_id = jsonRoot["rateConfig"]["itemId"]
        product_seller_id = jsonRoot["rateConfig"]["sellerId"]
        product_code = self.name + "_" + str(product_item_id)
        
        print "product_item_id:", product_item_id
        print "product_spuid:", product_spuid
        print "product_name:", product_name
        print "product_brand:", product_brand
        print "product_title:", product_title
        print "product_addr:", product_addr
        print "product_attr1:", product_attr1.decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        print "product_attr2:", product_attr2.decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        print "product_attr3:", product_attr3.decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        

        item_topic = productTopicItem()
        item_topic["product_code"] = product_code
        item_topic["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        
        # topic
        InfoProductTopic = ItemLoader(item=productTopicItem(), response=response)
        InfoProductTopic.add_value('name', "productTopicItem")
        InfoProductTopic.add_value('scheduler_id', 0)
        InfoProductTopic.add_value('keyword', self.key)
        InfoProductTopic.add_value('product_title', product_title)
        InfoProductTopic.add_value('product_code', product_code)
        InfoProductTopic.add_value('product_name', product_name)
        InfoProductTopic.add_value('product_brand', product_brand)
        InfoProductTopic.add_value('product_attr1', product_attr1)
        InfoProductTopic.add_value('product_attr2', product_attr2)
        InfoProductTopic.add_value('product_attr3', product_attr3)
        InfoProductTopic.add_value('product_keyword', self.key)
        InfoProductTopic.add_value('product_addr', product_addr)
        InfoProductTopic.add_value('good_count', 0)
        InfoProductTopic.add_value('general_count', 0)
        InfoProductTopic.add_value('poor_count', 0)
        InfoProductTopic.add_value('comment_url', response.url)
        InfoProductTopic.add_value('comment_count', 0)
        InfoProductTopic.add_value('crawl_time', item_topic["crawl_time"])
        InfoProductTopic.add_value('product_from', self.source)
        
        yield InfoProductTopic.load_item()
        
        #return
        # tags
        link = "https://rate.tmall.com/listTagClouds.htm?itemId=%s&isAll=true&isInner=true"%(product_item_id)
        request = Request(url=link, cookies=self.dic_cookie, callback=self.parse_product_tags)
        request.meta['item_topic'] = item_topic
        yield request
        
        
        # comment
        for page in range(1,20):
            link = "https://rate.tmall.com/list_detail_rate.htm?itemId=%s&spuId=%s&sellerId=%s&currentPage=%d"%(product_item_id, product_spuid, product_seller_id, page)
            request = Request(url=link, cookies=self.dic_cookie, callback=self.parse_product_comment)
            request.meta['item_topic'] = item_topic
            yield request
            
            
    def get_cookie(self, auth_url, url):
        data={}
        post_data=urllib.urlencode(data)
        headers ={}
        
        cookieJar=cookielib.CookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        req=urllib2.Request(auth_url,post_data,headers)
        result = opener.open(req)
        result = opener.open(url)
        
        if result.code == 200:
            c = ''
            dic = {}
            for item in cookieJar:
                key = str(item.name)
                value = str(item.value)
                dic[key]=value

        return dic
    
    def parse_product_tags(self, response):
        print "********** parse_product_tags **********"
        
        strJson = response.body.decode('gb2312', 'ignore').encode('utf-8', 'ignore')
        strJson = "{" + strJson + "}"
        strJson = strJson.replace("\n", "").replace("\r", "")
        jsonRoot = json.loads(strJson)
        rateSum = jsonRoot["tags"]["rateSum"]
        
        #print "rateSum:", rateSum
        item_topic = response.meta['item_topic']
        product_code = str(item_topic["product_code"])
        for tag in jsonRoot["tags"]["tagClouds"]:
            print "*"*50
            print tag["id"]
            print tag["count"]
            print tag["tag"]
            
            InfoProductTags = ItemLoader(item=productTagStatisticsItem(), response=response)
            InfoProductTags.add_value('name', "productTagStatisticsItem")
            InfoProductTags.add_value('product_code', product_code)
            InfoProductTags.add_value('code', tag["id"])
            InfoProductTags.add_value('tag', tag["tag"])
            InfoProductTags.add_value('count', tag["count"])
            InfoProductTags.add_value('crawl_time', item_topic["crawl_time"])
            
            yield InfoProductTags.load_item()

             
    def parse_product_comment(self, response):
        print "********** parse_product_comment **********"

        #print response.body.decode('utf-8', 'ignore').encode('gb2312', 'ignore')
        item_topic = response.meta['item_topic']
        strJson = response.body.decode('gb2312', 'ignore').encode('utf-8', 'ignore')
        strJson = "{" + strJson + "}"
        strJson = strJson.replace("\n", "").replace("\r", "")
        jsonRoot = json.loads(strJson)
        rateList = jsonRoot["rateDetail"]["rateList"]
        product_code = str(item_topic["product_code"])

        for comment in rateList:
            print "*"*50
            print product_code
            print comment["id"]
            print comment["rateContent"]
            print comment["rateDate"]
            print comment["displayUserNick"]
            
            InfoProductComment = ItemLoader(item=productCommentItem(), response=response)
            InfoProductComment.add_value('name', "productCommentItem")
            InfoProductComment.add_value('code', comment["id"])
            InfoProductComment.add_value('product_code', product_code)
            InfoProductComment.add_value('guid', comment["displayUserNick"])
            InfoProductComment.add_value('comment_content', comment["rateContent"])
            InfoProductComment.add_value('comment_stars', 0)
            InfoProductComment.add_value('comment_praise', 0)
            InfoProductComment.add_value('comment_time', comment["rateDate"])
            InfoProductComment.add_value('crawl_time', item_topic["crawl_time"])
            
            yield InfoProductComment.load_item()
            
            

            
        
    
             