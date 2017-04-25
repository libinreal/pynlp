#coding=utf-8

from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from sinaWeiboSpider.items import articleTopicItem, articleCommentItem
import scrapy
import lxml.html as lh
import sinaWeiboSpider.spiderUtil.StringUtils as sp
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

class sinaWeiboSpider(CrawlSpider):
    name = "sinaWeiboSpider"
    #allowed_domains = ["weixin.sogou.com", "mp.weixin.qq.com"]

    key = "iphone"
    source = "新浪微博"
    dic_cookie = {}
    str_cookie = ""
    headers_settings = {}
    start_urls = []

    def __init__(self):
        self.str_cookie = "SINAGLOBAL=1792963076449.764.1492503752614; ULV=1492587651527:3:3:3:5346633782024.6875.1492587651514:1492507646181; SCF=AtMzSXKmCXBMBB9n3qdsP-EJYPiTMiUL_O13JPggdA77GjwhprNOLEkejO52cSGcot2MMXJt4j6F4PbSa2R4G1Y.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWE9ri20yPalgno4V-BjYGr5JpX5KMhUgL.Foq7SKB0SK2feKn2dJLoIp7LxKqLBo-LBoMLxKqLBo-LB-2ceh-Xe0-pSK2R; SUHB=079jxaOzE-O1F7; ALF=1524104965; un=18221065710; wvr=6; SUB=_2A2518rvVDeRhGeBO7lYS9S_JyjSIHXVWiaodrDV8PUNbmtBeLUrQkW8pz43WqCoL5ugyxeE8gVRBdgFQOg..; SSOLoginState=1492568965; SWB=usrmdinst_6; _s_tentry=-; Apache=5346633782024.6875.1492587651514"
        self.headers_settings = {
            "Host": "s.weibo.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "max-age=0, no-cache"}
         
        self.headers_settings_comment = {
             "Host": "weibo.com",
             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
             "Accept": "*/*",
             "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
             "Accept-Encoding": "gzip, deflate",
             "Connection": "keep-alive",
             "Upgrade-Insecure-Requests": "1",
             "Content-Type": "application/x-www-form-urlencoded",
             "X-Requested-With": "XMLHttpRequest",
             "Cache-Control": "max-age=0, no-cache"}  
            
        self.dic_cookie = dict((line.split('=') for line in self.str_cookie.strip().split(";")))
        
        print self.dic_cookie
        
        url = "http://s.weibo.com/"
        self.start_urls.append(url)
        #for page in range(1,20):
        #    url = "http://s.weibo.com/weibo/%s&typeall=1&suball=1&Refer=g&page=%d"%(self.key, page)
        #    self.start_urls.append(url)

    def parse(self, response):
        for page in range(1,10):
            url = "http://s.weibo.com/weibo/%s&typeall=1&suball=1&page=%d"%(self.key, page)
            request = scrapy.Request(url, headers=self.headers_settings, cookies=self.dic_cookie, callback=self.parse_search)
            yield request
        
        
    def parse_search(self, response):
        print "*"*100
        sel = Selector(response)
        pn = 0
        htmlcode = ""
        script_items = sel.xpath('//script/text()').extract()
        for item in script_items:
            if item.find("STK.pageletM.view({\"pid\":\"pl_weibo_direct\"")>-1:
                print "="*100
                #print "feed_list_item:", item
                arrJs = item.split("STK.pageletM.view")
                js = arrJs[1]
                lenJs = len(js)
                js_new = js[1:lenJs-1]
                #print js_new
                
                jsonRoot = json.loads(js_new)
                htmlcode = jsonRoot["html"]
                
        if len(htmlcode) == 0:
            print "ERROR: HTML CODE IS EMPTY!"
          
        act = articleTopicItem()
        sel2 = Selector(text=htmlcode)
        
        mid = sel2.xpath('//div[@action-type="feed_list_item"]/@mid').extract_first()
        feed_list_items = sel2.xpath('//div[@action-type="feed_list_item"]').extract()
        for feed_list_item in feed_list_items:
            print "\n\n\n\n"
            print "*"*100,"-"
            #print feed_list_item.decode("utf-8", "ignore").encode("gb2312", "ignore")

            sel_content = Selector(text=feed_list_item)
            
            article_comment_data = sel_content.xpath('//ul[@class="feed_action_info feed_action_row4"]').extract_first()
            reply_num = sel_content.xpath('//a[@suda-data="key=tblog_search_weibo&value=weibo_ss_1_p"]/span[@class="line S_line1"]/em/text()').extract_first()
            click_num = sel_content.xpath('//a[@suda-data="key=tblog_search_weibo&value=weibo_ss_1_zan"]/span[@class="line S_line1"]/em/text()').extract_first()

            try:
                reply_num = int(reply_num)
            except:
                reply_num = 0
                pass
            
            try:
                click_num = int(click_num)
            except:
                click_num = 0
                pass
            
            
            print "mid:", mid
            print "reply_num:", reply_num
            #print "click_num:", click_num
            
            
            article_names = sel_content.xpath('//p[@class="comment_txt"]/text()').extract()
            act["article_author"] = sel_content.xpath('//p[@class="comment_txt"]/@nick-name').extract_first()
            
            article_url = sel_content.xpath('//div[@class="feed_content wbcon"]/a/@href').extract_first()
            #print "article_url:::", article_url
            
            article_id = sp.hashForUrl(article_url)
            article_id = self.name + "_" + article_id
            
            content = ""
            for article_name in article_names:
                content = content + article_name.replace("\n", "").replace("\r", "").strip()
            author = act["article_author"].replace("\n", "").replace("\r", "").lstrip()
            
            act["article_name"] = content
            act["article_author"] = author
            act["article_from"] = self.source
            act["article_key"] = self.key
            act["article_time"] = sel_content.xpath('//div[@class="feed_from W_textb"]/a/@title').extract_first()
            act["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            act["article_url"] = article_url
            act["article_id"] = article_id
            
            print "article_id:", act["article_id"]
            print "article_url:", act["article_url"]
            print "crawl_time:", act["crawl_time"]
            print "article_name:", act["article_name"].decode("utf-8", "ignore").encode("gb2312", "ignore")
            print "article_author:", act["article_author"].decode("utf-8", "ignore").encode("gb2312", "ignore")
            print "article_time:", act["article_time"]
            print "article_from:", act["article_from"].decode("utf-8", "ignore").encode("gb2312", "ignore")
            print "article_key:", act["article_key"].decode("utf-8", "ignore").encode("gb2312", "ignore")
                        
                        
            Info = ItemLoader(item = articleTopicItem(), response = response)
            Info.add_value('name', "articleTopicItem")
            Info.add_value('article_name', act["article_name"].encode('utf-8'))
            Info.add_value('article_id', act["article_id"].encode('utf-8'))
            Info.add_value('article_content', article_name)
            Info.add_value('article_key', self.key)
            Info.add_value('crawl_time', act["crawl_time"].encode('utf-8'))
            Info.add_value('article_time', act["article_time"].encode('utf-8'))
            Info.add_value('article_url', act["article_url"].encode('utf-8'))
            Info.add_value('reply_num', reply_num)
            Info.add_value('click_num', click_num)
            Info.add_value('article_author', act["article_author"].encode('utf-8'))
            Info.add_value('article_from',  self.source.encode('utf-8'))
            Info.add_value('scheduler_id', 0)
            Info.add_value('area', 0)

            yield Info.load_item()
            
            item = articleTopicItem()
            item["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            item["article_id"] = article_id
            # small
            #url = "http://s.weibo.com/ajax/comment/small?act=list&mid=4097867158667788&uid=6054351518"
            
            #mid = "4086615179151916"
            
            if reply_num > 0:
                # big 
                pages = reply_num/20 + 1
                if pages>100:
                    pages = 100
                    
                for page in range(1,10):
                    url = "http://weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&page=%d&filter=hot"%(mid, page)
                    request = scrapy.Request(url, headers=self.headers_settings_comment, cookies=self.dic_cookie, callback=self.parse_article_comment)
                    request.meta['item'] = item
                    yield request
            
            #break
            
            
    def parse_article_comment(self, response):
        print "***************** parse_article_comment **********************"
        #print response.body.decode("utf-8", "ignore").encode("gb2312", "ignore")
        
        item = response.meta['item']

        # "data":{"html"
        #print "============================================"
        strJson = response.body
        jsonRoot = json.loads(strJson)
        comment_data = jsonRoot["data"]["html"]
        #print comment_data.decode("utf-8", "ignore").encode("gb2312", "ignore")
        #product_item_list = jsonRoot["mods"]["itemlist"]

        article_url = str(response.url)
        article_id = sp.hashForUrl(article_url)
        
        sel = Selector(text=comment_data)
        # list_li S_line1 clearfix
        comment_list_items = sel.xpath('//div[@class="list_li S_line1 clearfix"]').extract()
        for comment_item in comment_list_items:
            #print "::::::::::::\n\n"
            #print comment_item.decode("utf-8", "ignore").encode("gb2312", "ignore")
            comment_item = comment_item.replace("：", "").replace("\n", "").replace("\r", "")
            sel_content = Selector(text=comment_item)
            article_id = sel_content.xpath('//div/@comment_id').extract_first()
            comment_author = sel_content.xpath('//div[@class="WB_text"]/a/text()').extract_first()
            comment_contents = sel_content.xpath('//div[@class="WB_text"]/text()').extract()
            comment_time = sel_content.xpath('//div[@class="WB_from S_txt2"]/text()').extract_first()
            article_code = item["article_id"]
            current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            if comment_time.find("今天")>=0:
                comment_time = str(datetime.datetime.now().strftime("%Y-%m-%d"))

            comment_content = ""
            for comment in comment_contents:
                #print comment.decode("utf-8", "ignore").encode("gb2312", "ignore")
                if len(comment)>0:
                    comment_content = comment_content + comment

            comment_content = comment_content.replace("\r", "").replace("\n", "").replace(" ", "").lstrip().rstrip()
            
            print "comment_id:", article_id
            print "article_code:", article_code  
            print "comment_author:", comment_author.decode("utf-8", "ignore").encode("gb2312", "ignore")    
            print "comment_content:", comment_content.decode("utf-8", "ignore").encode("gb2312", "ignore")
            print "comment_time:", comment_time.decode("utf-8", "ignore").encode("gb2312", "ignore") 
            print "crawl_time:", item["crawl_time"]

            CommentInfo = ItemLoader(item = articleCommentItem(), response = response)
            CommentInfo.add_value('name', "articleCommentItem")
            CommentInfo.add_value('article_code', item["article_id"])
            CommentInfo.add_value('comment_time', comment_time)
            CommentInfo.add_value('current_time', item["crawl_time"])
            CommentInfo.add_value('guid', comment_author)
            CommentInfo.add_value('comment_content', comment_content)
            yield CommentInfo.load_item()
            
            
            