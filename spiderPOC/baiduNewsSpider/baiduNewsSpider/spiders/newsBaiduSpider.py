#coding=utf-8

from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from baiduNewsSpider.items import articleTopicItem
import scrapy
import lxml.html as lh
import baiduNewsSpider.SpiderUtil.StringUtils as sp
import sys
import time
import os
from scrapy.contrib.spiders import CrawlSpider, Rule
from urlparse import urljoin
from xml.dom.minidom import parse
import xml.dom.minidom

import json

reload(sys)
sys.setdefaultencoding('utf8')

import datetime


class newsBaiduSpider(CrawlSpider):
    name = "baiduNewsSpider"
    #allowed_domains = ["weixin.sogou.com", "mp.weixin.qq.com"]

    key = "m2017"
    source = "百度新闻"
    start_urls = []
    dic_cookie = {}
    headers_settings = {}
    
    def __init__(self):
        self.headers_settings = {
                     "Host": "news.baidu.com",
                     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                     "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                     "Accept-Encoding": "gzip, deflate",
                     "Cookie": "BAIDUID=F05FC020A1B80FA4D0F5CC9563167A81:FG=1; BIDUPSID=F05FC020A1B80FA4D0F5CC9563167A81; PSTM=1490169240; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=; LOCALGX=%u4E0A%u6D77%7C%32%33%35%34%7C%u4E0A%u6D77%7C%32%33%35%34; Hm_lvt_e9e114d958ea263de46e080563e254c4=1490751393,1490751918; Hm_lpvt_e9e114d958ea263de46e080563e254c4=1490751918; BD_CK_SAM=1; BDSVRTM=285; PSINO=2; BDRCVFR[C0p6oIjvx-c]=mbxnW11j9Dfmh7GuZR8mvqV",
                     "Connection": "keep-alive",
                     "Upgrade-Insecure-Requests": "1"}


        #url = "https://s.taobao.com/search?q=%s&imgfile=&ie=utf8"%(self.key)
        url = "http://news.baidu.com/ns?word=%s&tn=news&from=news&cl=2&rn=20&ct=1"%(self.key)
        self.start_urls.append(url)
        
    def parse(self, response):
        print response.body.decode("utf-8", "ignore").encode("gb2312", "ignore")

        sel = Selector(response)
        pn = 0
        for i in range(0, 5):
            #url = "http://news.baidu.com/ns?word=iphone7&tn=news&from=news&cl=2&rn=20&ct=1"
            pn = i*20
            url = "http://news.baidu.com/ns?word=%s&tn=news&from=news&cl=2&rn=20&ct=1&pn=%d"%(self.key, pn)
            request = scrapy.Request(url, headers=self.headers_settings, callback=self.parse_article_list)
            yield request

    
    def parse_article_list(self, response):
        sel = Selector(response)

        article_url_links = sel.xpath('//div[@class="result"]').extract()
        for link in article_url_links:
            sel = Selector(text=link)
            
            item_topic = articleTopicItem()
            
            article_titles = sel.xpath('//h3[@class="c-title"]/a/text()').extract()
            item_topic["article_url"] = sel.xpath('//h3[@class="c-title"]/a/@href').extract_first()
            item_topic["article_id"] = sp.get_md5_value(item_topic["article_url"])
            
            item_topic["article_id"] = self.name + "_" + item_topic["article_id"]
            
            article_title = ""
            for txt in article_titles:
                article_title = article_title + txt
            item_topic["article_name"] = article_title
            
            article_author_time = sel.xpath('//p[@class="c-author"]/text()').extract_first()
            pos = sp.get_first_num_pos(article_author_time)
            item_topic["article_author"] = article_author_time[0:pos]
            item_topic["article_time"] = article_author_time[pos:len(article_author_time)]
            item_topic["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            request = scrapy.Request(item_topic["article_url"], callback=self.parse_article_content)
            request.meta['item_topic'] = item_topic
            yield request      
        
       
        #next_page_url = sel.xpath('//div[@class="long-pages"]/a[last()]/@href').extract()
        

    def parse_article_content(self, response):
        print "***********", "parse_article_content" , "**************"
        #print response.body.decode("utf-8", "ignore").encode("gb2312", "ignore")
        item_topic = response.meta['item_topic']

        sel = Selector(response)
        article_title = sel.xpath('//html/head/title/text()').extract_first()

        pTags = sel.xpath('//div/p/text()').extract()
        article_content = ""
        
        for pTag in pTags:
            pTag = pTag.strip()
            pTag = pTag.replace(" ", "").replace("\r", "").replace("\n", "")
            if len(pTag)>1:
                article_content = article_content + " " + pTag
                
        if article_title == None or article_title == "":
            article_title = sel.xpath('//html/head/title/text()').extract_first()
        
        if article_title == None or article_title == "":
            # <meta name="description" content=
            article_title = sel.xpath('//html/head/meta[@name="description"]/@content').extract_first()  
            
        if article_title == None or article_title == "":
            # <meta name="keywords" content=
            article_title = sel.xpath('//html/head/meta[@name="keywords"]/@content').extract_first() 
            
        item_topic["article_content"] = article_content
        
        print "\r\n"
        print "article_id:", item_topic["article_id"]
        print "article_url:", item_topic["article_url"]
        print "article_title:", item_topic["article_name"]
        print "article_author:", item_topic["article_author"].decode("utf-8", "ignore").encode("gb2312", "ignore")
        print "article_time:", item_topic["article_time"].decode("utf-8", "ignore").encode("gb2312", "ignore")
        print "article_content:", item_topic["article_content"].decode("utf-8", "ignore").encode("gb2312", "ignore")
        print "crawl_time:", item_topic["crawl_time"]   
        

        Info = ItemLoader(item = articleTopicItem(), response = response)
        Info.add_value('name', "articleTopicItem")
        Info.add_value('article_name', item_topic["article_name"].encode('utf-8'))
        Info.add_value('article_id', item_topic["article_id"].encode('utf-8'))
        Info.add_value('article_content', item_topic["article_content"].encode('utf-8'))
        Info.add_value('article_key', self.key)
        Info.add_value('crawl_time', item_topic["crawl_time"].encode('utf-8'))
        Info.add_value('article_time', item_topic["article_time"].encode('utf-8'))
        Info.add_value('article_url', item_topic["article_url"].encode('utf-8'))
        Info.add_value('reply_num', 0)
        Info.add_value('click_num', 0)
        Info.add_value('article_author', item_topic["article_author"].encode('utf-8'))
        Info.add_value('article_from',  self.source.encode('utf-8'))
        Info.add_value('image_urls', "")
        Info.add_value('scheduler_id', 0)
        Info.add_value('area', 0)
         
        yield Info.load_item()