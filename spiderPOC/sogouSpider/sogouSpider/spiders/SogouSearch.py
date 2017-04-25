#coding=utf-8
import sys
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")
from scrapy.contrib.loader import ItemLoader
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from sogouSpider.items import WechartAccount
from sogouSpider.SpiderUtil import spiderutil as sp
import json
import scrapy

import urllib2
import urllib
import cookielib
import re
import HTMLParser


class SogouWechartSpider(BaseSpider):
    name = 'sogouSpider'
    allowed_domains = ["weixin.sogou.com", "mp.weixin.qq.com"]
    start_key = ['python']
    start_urls = []
    dic_cookie = {}
    key = "苹果"

    def __init__(self):
        """
        fileObj = open('F:/scrapy/it_key.json')
        str = fileObj.read()
        keys = json.loads(str)
        for key in keys:
            self.start_key.append(key['name'])
            for c in key['children']:
                self.start_key.append(c['name'])
        for key in self.start_key:
            for i in range(1, 10):
                url = 'http://weixin.sogou.com/weixin?type=2&query=%s&ie=utf8&_sug_=n&_sug_type_=page=%s' % (key, i)
                self.start_urls.append(url)
        """

        '''
        for i in range(2, 3):
            url = 'http://weixin.sogou.com/weixin?query=%s&_sug_type_=&_sug_=n&type=2&page=%s&ie=utf8'% (self.key, i)
            self.start_urls.append(url)
        '''
        url = "http://weixin.sogou.com/"
        self.start_urls.append(url)    
        

    def parse(self, response):
        #http://weixin.sogou.com/
        #self.dic_cookie = sp.get_cookie("http://weixin.sogou.com/", self.start_urls[0])

        headers_settings = {
            "Host": "weixin.sogou.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Cookie": "ABTEST=0|1490168081|v1; IPLOC=CN3101; SUID=AA4D4A7C1E24940A0000000058D22911; SUV=008F73507C4A4DAA58D22912BACA3905; SUIR=1490168090; SUID=AA4D4A7C2E08990A0000000058D2291B; SNUID=1FFBFFCAB5B0FEF9576F11EAB6DE507E; JSESSIONID=aaa6BQMT8grr2_utAF5Rv; weixinIndexVisited=1; ppinf=5|1490336863|1491546463|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlODglOUQlRTUlQkYlODN8Y3J0OjEwOjE0OTAzMzY4NjN8cmVmbmljazoxODolRTUlODglOUQlRTUlQkYlODN8dXNlcmlkOjQ0Om85dDJsdU5HTjF4Y0ZwaVh3U2pRVlotOG1mVkVAd2VpeGluLnNvaHUuY29tfA; pprdig=KW4UMYb9KRMc4KS-2HDJtAdvV177jTly22HVToDE-Ll7E-n4qX6sO2RwdgYIrAgztUL1SuFRAFz-L1cFAq1myNGAnJRvCGKHTiO4_U1YaXTlfMYOwhNM_wA8K_DxSczc8DkcDxmB6Bsvfp2mgbM2u_yQgmmdSK3zAMQ4x0719eU; sgid=; ppmdig=1490336863000000016210721bdf2bfd216dcf492cafd45f",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
            }
        
   
        for i in range(1, 100):
            url = 'http://weixin.sogou.com/weixin?query=%s&_sug_type_=&_sug_=n&type=2&page=%s&ie=utf8'% (self.key, i)
            #url = "http://weixin.sogou.com/weixin?type=2&quesry=iphone+6s&ie=utf8&s_from=input&_sug_=y&_sug_type_="
            request = scrapy.Request(url, headers=headers_settings, callback=self.parse_article)
            yield request
            
        
    def parse_article(self, response):
        #print "parse_article:"
        #print response.body.decode("utf-8", "ignore").encode("gb2312", "ignore")

        sel = Selector(response)
        item = WechartAccount()
        article_url = sel.xpath( '//div[@class="txt-box"]/h3/a/@href').extract()
        for l in article_url:
            urll = l
            #link = ''.join(l.xpath('div[2]/h4/a/@href').extract())
            request = scrapy.Request(urll, cookies=self.dic_cookie, callback=self.parse_article_content)
            request.meta['item'] = item
            yield request
            break
        
    def parse_article_content(self, response):
        #print response.body.decode("utf-8", "ignore").encode("gb2312", "ignore")
        #return
        
        content = ''
        sel = Selector(response)
        item = response.meta['item']
        
        article_url = str(response.url)

        today_timestamp = sp.get_tody_timestamp()
        article_id = sp.hashForUrl(article_url)
        article_name = sel.xpath('//title/text()').extract()
        article_time = sel.xpath('//div[@class="rich_media_meta_list"]/em[@id="post-date"]/text()').extract()
        article_author = sel.xpath('//div[@class="rich_media_meta_list"]/a[@id="post-user"]/text()').extract()
        article_content = sel.xpath('//div[@id="js_content"]/p/span[1]/text()').extract()
        image_urls = sel.xpath('//div[@id="js_content"]/p/img/@data-src').extract()

        for i in article_content:
            content = content + i

        article_id = article_id.encode('utf-8')
        article_name = article_name[0].encode('utf-8')
        content = content.encode('utf-8')
        article_time = article_time[0]
        crawl_time = today_timestamp.encode('utf-8')
        article_url = article_url.encode('utf-8')
        article_author = article_author[0]
        article_id = self.name + "_" + article_id
        article_key = self.key
        article_from = "搜狗微信" 
        
        item = WechartAccount() 
        item["article_id"] = article_id
        item["article_key"] = article_key
        item["article_name"] = article_name
        item["article_url"] = article_url
        item["article_content"] = content
        item["article_time"] = article_time
        item["article_from"] = article_from
        item["crawl_time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        item["click_num"] = "0"
        item["reply_num"] = "0"
        item["praise_num"] = "0"
        item["article_author"] = article_author
        item["image_urls"] = image_urls
        
        url = response.url.replace("/s?", "/mp/getcomment?")
        request = scrapy.Request(url, callback=self.parse_article_comment)
        request.meta['item'] = item
        yield request

        
    def parse_article_comment(self, response):
        item = response.meta['item']
        jsonRoot = json.loads(response.body)
        
        try:
            item["reply_num"] = jsonRoot["read_num"]
            item["click_num"] = jsonRoot["like_num"]
            item["praise_num"] = jsonRoot["like_num"]
        except:
            pass
            
        if item["reply_num"] == "": 
            item["reply_num"] = "0"
        
        if item["click_num"] == "":
            item["click_num"] = "0"

        print "\r\n"
        print "article_name:", item["article_name"]
        print "article_from", item["article_from"]
        print "article_id:", item["article_id"]
        #print "article_content:", article_content
        print "crawl_time:", item["crawl_time"]
        print "article_time:", item["article_time"]
        print "reply_num:", item["reply_num"]
        print "click_num:", item["click_num"]
        print "article_author:", item["article_author"]
        
        Info = ItemLoader(item=WechartAccount(), response=response)
        Info.add_value('article_key', self.key)
        Info.add_value('article_id', item["article_id"])
        Info.add_value('article_from', item["article_from"])
        Info.add_value('article_name', item["article_name"])
        Info.add_value('article_content', item["article_content"])
        Info.add_value('crawl_time', item["crawl_time"])
        Info.add_value('article_time', item["article_time"])
        Info.add_value('article_url', item["article_url"])
        Info.add_value('reply_num', item["reply_num"])
        Info.add_value('click_num', item["click_num"])
        Info.add_value('article_author', item["article_author"])
        Info.add_value('image_urls', item["image_urls"])
        Info.add_value('scheduler_id', 0)
        Info.add_value('area', 0)
        
        yield Info.load_item()
        
    
      
        
        



