#coding=utf-8

from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from renrenSpider.items import articleTopicItem, articleCommentItem
import scrapy
import lxml.html as lh
import renrenSpider.spiderUtil.StringUtils as sp
import sys
import time
import os
from scrapy.contrib.spiders import CrawlSpider, Rule
from urlparse import urljoin
from xml.dom.minidom import parse
import xml.dom.minidom

reload(sys)
sys.setdefaultencoding('utf8')

import datetime

import json

class renrenSpider(CrawlSpider):
    name = "renrenSpider"
    #allowed_domains = ["weixin.sogou.com", "mp.weixin.qq.com"]

    key = "iphone"
    source = "人人网"
    dic_cookie = {}
    str_cookie = ""
    headers_settings = {}
    start_urls = []

    def __init__(self):
        self.str_cookie = "SINAGLOBAL=1792963076449.764.1492503752614; ULV=1492587651527:3:3:3:5346633782024.6875.1492587651514:1492507646181; SCF=AtMzSXKmCXBMBB9n3qdsP-EJYPiTMiUL_O13JPggdA77GjwhprNOLEkejO52cSGcot2MMXJt4j6F4PbSa2R4G1Y.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWE9ri20yPalgno4V-BjYGr5JpX5KMhUgL.Foq7SKB0SK2feKn2dJLoIp7LxKqLBo-LBoMLxKqLBo-LB-2ceh-Xe0-pSK2R; SUHB=079jxaOzE-O1F7; ALF=1524104965; un=18221065710; wvr=6; SUB=_2A2518rvVDeRhGeBO7lYS9S_JyjSIHXVWiaodrDV8PUNbmtBeLUrQkW8pz43WqCoL5ugyxeE8gVRBdgFQOg..; SSOLoginState=1492568965; SWB=usrmdinst_6; _s_tentry=-; Apache=5346633782024.6875.1492587651514"
        self.dic_cookie = dict((line.split('=') for line in self.str_cookie.strip().split(";")))
        #print self.dic_cookie
        
        for page in range(0,10):
            offset = page*10
            
            print "offset:::::::::::::::::::::::", offset
            
            # http://browse.renren.com/s/content?q=iphone6&p=&limit=10&sort=0&offset=20&range=0&t=0
            url = "http://browse.renren.com/s/content?q=iphone6&p=&limit=10&sort=0&offset=%d&range=0&t=0"%(offset)
            print url
            #continue
            self.start_urls.append(url)
            


    def parse(self, response):
        #print response.body.decode("utf-8", "ignore").encode("gb2312", "ignore")
        
        sel = Selector(response)
        pn = 0
        htmlcode = ""

        
        list_nodes = sel.xpath('//div[@class="search_log"]/div[@class="list_node"]').extract()
        for node in list_nodes:
            # div class="node_title">
            sel_node = Selector(text=node)
            
            article_url = sel_node.xpath('//div[@class="node_title"]/a/@href').extract_first()
            article_name = sel_node.xpath('//div[@class="node_title"]/a/text()').extract_first()
            article_time = sel_node.xpath('//div[@class="node_content"]/div[@class="node_content_info"]/p[@class="action"]/font/text()').extract_first()
            article_author = sel_node.xpath('//div[@class="node_content"]/div[@class="node_content_info"]/p[@class="action"]/a/text()').extract_first()
            article_time = article_time.replace("来自", "")
            article_from = self.source
            article_key = self.key
           
            article_id = sp.hashForUrl(article_url)
            article_id = self.name + "_" + article_id
             
            print "\n\n\n"
            print "*"*100
            print "article_id:", article_id
            print "article_name:", article_name
            print "article_time:", article_time
            print "article_author:", article_author
            print "article_from:", article_from
            print "article_key:", article_key
            print "article_url:", article_url
            
            s = article_url.split('/')
            entryOwnerId = s[len(s)-2]
            entryId = s[len(s)-1]
            arr = entryId.split("?")
            if len(arr)>1:
                entryId = arr[0]
            else:
                entryId = b
             
            print "entryOwnerId:", entryOwnerId    
            print "entryId:", entryId
             
            
            url = "http://comment.renren.com/comment/xoa2/global?limit=20&desc=true&offset=0&replaceUBBLarge=true&type=share&entryId=%s&entryOwnerId=%s&"%(entryId, entryOwnerId)
            print "url:commentL", url
            
            item = articleTopicItem()
            item["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            item["article_id"] = article_id
            
            # save topic
            Info = ItemLoader(item = articleTopicItem(), response = response)
            Info.add_value('name', "articleTopicItem")
            Info.add_value('article_name', article_name.encode('utf-8'))
            Info.add_value('article_id', article_id.encode('utf-8'))
            Info.add_value('article_content', article_name)
            Info.add_value('article_key', self.key)
            Info.add_value('crawl_time', item["crawl_time"].encode('utf-8'))
            Info.add_value('article_time', article_time.encode('utf-8'))
            Info.add_value('article_url', url.encode('utf-8'))
            Info.add_value('reply_num', 0)
            Info.add_value('click_num', 0)
            Info.add_value('article_author', article_author.encode('utf-8'))
            Info.add_value('article_from',  self.source.encode('utf-8'))
            Info.add_value('scheduler_id', 0)
            Info.add_value('area', 0)
            
            yield Info.load_item()
            
            
            # request 
            request = scrapy.Request(url, headers=self.headers_settings, cookies=self.dic_cookie, callback=self.parse_article_comment)
            request.meta['item'] = item
            yield request
             
        list_nodes = sel.xpath('//div[@class="search_log"]/div[@class="list_img"]').extract()
        for node in list_nodes:
            # div class="node_title">
            sel_node = Selector(text=node)
            
            article_url = sel_node.xpath('//div[@class="img_title"]/a/@href').extract_first()
            titles = sel_node.xpath('//div[@class="img_title"]/a/text()').extract()
            article_name = ""
            for title in titles:
                article_name = article_name + title
            article_name = article_name.replace("\n", "").replace("\r", "").strip() 
            
            article_time = sel_node.xpath('//div[@class="img_content"]/div[@class="img_content_info"]/p[@class="action"]/font/text()').extract_first()
            article_author = sel_node.xpath('//div[@class="img_content"]/div[@class="img_content_info"]/p[@class="action"]/a/text()').extract_first()
            article_time = article_time.replace("来自", "")
            article_from = self.source
            article_key = self.key
           
            article_id = sp.hashForUrl(article_url)
            article_id = self.name + "_" + article_id
             
            print "\n\n\n"
            print "="*100
            print "article_id:", article_id
            print "article_name:", article_name
            print "article_time:", article_time
            print "article_author:", article_author
            print "article_from:", article_from
            print "article_key:", article_key
            print "article_url:", article_url
            
            s = article_url.split('/')
            entryOwnerId = s[len(s)-2]
            entryId = s[len(s)-1]
            arr = entryId.split("?")
            if len(arr)>1:
                entryId = arr[0]
             
            print "entryOwnerId:", entryOwnerId    
            print "entryId:", entryId
             
            
            url = "http://comment.renren.com/comment/xoa2/global?limit=20&desc=true&offset=0&replaceUBBLarge=true&type=share&entryId=%s&entryOwnerId=%s&"%(entryId, entryOwnerId)
            print "url:commentL", url

            item = articleTopicItem()
            item["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            item["article_id"] = article_id

            # save topic
            Info = ItemLoader(item = articleTopicItem(), response = response)
            Info.add_value('name', "articleTopicItem")
            Info.add_value('article_name', article_name.encode('utf-8'))
            Info.add_value('article_id', article_id.encode('utf-8'))
            Info.add_value('article_content', article_name)
            Info.add_value('article_key', self.key)
            Info.add_value('crawl_time', item["crawl_time"].encode('utf-8'))
            Info.add_value('article_time', article_time.encode('utf-8'))
            Info.add_value('article_url', url.encode('utf-8'))
            Info.add_value('reply_num', 0)
            Info.add_value('click_num', 0)
            Info.add_value('article_author', article_author.encode('utf-8'))
            Info.add_value('article_from',  self.source.encode('utf-8'))
            Info.add_value('scheduler_id', 0)
            Info.add_value('area', 0)
            
            yield Info.load_item()
            
            request = scrapy.Request(url, headers=self.headers_settings, cookies=self.dic_cookie, callback=self.parse_article_comment)
            request.meta['item'] = item
            yield request
            

    def parse_article_comment(self, response):
        print "***************** parse_article_comment **********************"
        print response.body.decode("utf-8", "ignore").encode("gb2312", "ignore")
       
        item = response.meta['item']

        strJson = response.body
        jsonRoot = json.loads(strJson)
        comments = jsonRoot["comments"]
        for comment in comments:
            if len(comment)<10:
                continue
            
            print "\n\n\n"
            print comment
            print "-"*100
            print "article_id:", item["article_id"] 
            #print "commentId:", comment["commentId"]
            print "time:", comment["time"]
            print "authorName:", comment["authorName"].decode("utf-8", "ignore").encode("gb2312", "ignore")
            print "content:", comment["content"].decode("utf-8", "ignore").encode("gb2312", "ignore")
            print "crawl_time:", item["crawl_time"] 

            CommentInfo = ItemLoader(item = articleCommentItem(), response = response)
            CommentInfo.add_value('name', "articleCommentItem")
            CommentInfo.add_value('article_code', item["article_id"])
            CommentInfo.add_value('comment_time', comment["time"])
            CommentInfo.add_value('current_time', item["crawl_time"])
            CommentInfo.add_value('guid', comment["authorName"])
            CommentInfo.add_value('comment_content', comment["content"])
            yield CommentInfo.load_item()
            
