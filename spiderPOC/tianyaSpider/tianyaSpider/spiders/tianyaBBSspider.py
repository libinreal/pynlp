#coding=utf-8

from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from tianyaSpider.items import articleTopicItem, articleCommentItem
import scrapy
import lxml.html as lh
from tianyaSpider.tianyaSpiderUtil import spiderutil as sp
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


class tianyaBBSspider(CrawlSpider):
    # 爬虫名称，非常关键，唯一标示
    name = "tianyaSpider"

    # 域名限定
    allowed_domains = ["bbs.tianya.cn"]
    #allowed_domains = ["weixin.sogou.com", "mp.weixin.qq.com"]

    key = "天涯论坛热帖榜"

    # 爬虫的爬取得起始url
    start_urls = [

        # 天涯论坛热帖榜  可以写多个用，分隔

        "http://bbs.tianya.cn/hotArticle.jsp",
        #"http://weixin.sogou.com/weixin?type=2&query=信用卡&ie=utf8&_sug_=n&_sug_type_=page=1"
    ]
    baseurl = 'http://bbs.tianya.cn'

    def parse(self, response):
        # 选择器
        sel = Selector(response)
        item = articleTopicItem()
        # 文章url列表
        article_url = sel.xpath('//div[@class="mt5"]/table[@class="tab-bbs-list tab-bbs-list-2"]//tr[@class="bg"]/td[1]/a/@href').extract()
        # 下一页地址
        next_page_url = sel.xpath('//div[@class="long-pages"]/a[last()]/@href').extract()

        for url in article_url:
            # 拼接url
            urll = urljoin(self.baseurl, url)
            # 调用parse_item解析文章内容
            request = scrapy.Request(urll, callback = self.parse_item)
            request.meta['item'] = item
            item["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            yield request
            #return
        
    
        if next_page_url[0]:
            # 调用自身进行迭代
            request = scrapy.Request(urljoin(self.baseurl, next_page_url[0]), callback=self.parse)
            yield request

    def parse_item(self, response):
        
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        Info = ItemLoader(item = articleTopicItem(), response = response)

        article_url = str(response.url)

        today_timestamp = sp.get_tody_timestamp()
        article_id = sp.hashForUrl(article_url)
        article_name = sel.xpath('//div[@id="post_head"]/h1/span/span/text()').extract()
        article_time = sel.xpath('//div[@class="atl-info"]/span[2]/text()').extract()
        article_content = sel.xpath('//div[@class="atl-main"]//div/div[@class="atl-content"]/div[2]/div[1]/text()').extract()
        article_author = sel.xpath('//div[@class="atl-info"]/span[1]/a/text()').extract()
        article_clik_num = sel.xpath('//div[@class="atl-info"]/span[3]/text()').extract()
        article_reply_num = sel.xpath('//div[@class="atl-info"]/span[4]/text()').extract()
        article_code = self.name + "_" + article_id
    
        article_comment_items = sel.xpath('//div[@class="atl-main"]/div[@class="atl-item"]').extract()
        for item_comment in article_comment_items:
            sel_item = Selector(text=item_comment)
            comment_item = articleCommentItem()
            comment_item["name"] = "articleCommentItem"
            comment_item["article_id"] = article_id
            comment_item["article_code"] = article_code
            comment_item["guid"] = sel_item.xpath('//div[@class="atl-item"]/@js_username').extract_first()
            comment_item["comment_content"] = sel_item.xpath('//div[@class="bbs-content"]/text()').extract_first()
            comment_item["comment_content"] = comment_item["comment_content"].replace("\r", "").replace("\n", "").replace(" ", "")
            comment_item["comment_content"] = comment_item["comment_content"].lstrip()
            comment_item["comment_content"] = comment_item["comment_content"].rstrip()
            comment_item["comment_stars"] = "0"
            comment_item["comment_praise"] = "0"
            comment_item["comment_time"] = sel_item.xpath('//div[@class="atl-item"]/@js_restime').extract_first()
            comment_item["current_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            comment_item["crawl_time"] = item["crawl_time"]
            
            print "*"*100
            print article_name[0]
            print comment_item["article_code"]
            print comment_item["comment_time"]
            print comment_item["crawl_time"]
            print comment_item["current_time"]
            print comment_item["guid"]
            print comment_item["comment_content"]
            
            CommentInfo = ItemLoader(item = articleCommentItem(), response = response)
            CommentInfo.add_value('name', "articleCommentItem")
            CommentInfo.add_value('article_code', comment_item["article_code"])
            CommentInfo.add_value('comment_time', comment_item["comment_time"])
            CommentInfo.add_value('current_time', comment_item["current_time"])
            CommentInfo.add_value('guid', comment_item["guid"])
            CommentInfo.add_value('comment_content', comment_item["comment_content"])
            yield CommentInfo.load_item()
            #print item.decode("utf-8", "ignore").encode("gb2312", "ignore")
            #break 
            
        #return
        

        # 文章内容拼起来
        for i in article_content:
            content = content + i

        article_id = article_id.encode('utf-8')
        article_name = article_name[0].encode('utf-8')
        #article_name = article_name[0]
        content = content.encode('utf-8')
        #article_time = article_time[0].encode('utf-8')[9::]
        article_time = article_time[0]
        crawl_time = today_timestamp.encode('utf-8')
        article_url = article_url.encode('utf-8')
        #article_author = article_author[0].encode('utf-8')
        article_author = article_author[0]
        click_num = article_clik_num[0].encode('utf-8')[9::]
        reply_num = article_reply_num[0].encode('utf-8')[9::]
        
        if(article_time.find("：")>0):
            article_time = article_time.split("：")[1]
            
        article_id = self.name + "_" + article_id

        article_from = "天涯论坛"        
        print "\r\n"
        print "article_name:", article_name
        print "article_from", article_from
        print "article_id:", article_id
        #print "article_content:", article_content
        print "crawl_time:", crawl_time
        print "article_time:", article_time
        print "reply_num:", reply_num
        print "click_num:", click_num
        print "article_author:", article_author

        #article_name = article_name.decode("utf-8", "ignore").encode("gb2312", "ignore")
        #article_author  = article_name.decode("utf-8", "ignore").encode("gb2312", "ignore")
        Info.add_value('name', "articleTopicItem")
        Info.add_value('article_name', article_name)
        Info.add_value('article_id', article_id)
        Info.add_value('article_content', content)
        Info.add_value('article_key', self.key)
        Info.add_value('crawl_time', crawl_time)
        Info.add_value('article_time', article_time)
        Info.add_value('article_url', article_url)
        Info.add_value('reply_num', reply_num)
        Info.add_value('click_num', click_num)
        Info.add_value('article_author', article_author)
        Info.add_value('article_from', article_from)
        
        
        yield Info.load_item()
