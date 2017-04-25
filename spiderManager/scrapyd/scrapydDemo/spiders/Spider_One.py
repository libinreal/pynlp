#coding=utf-8
'''
@author: nancheng
'''

#coding=utf-8
from BeautifulSoup import BeautifulSoup
import logging
import scrapy
from scrapydDemo.items import  *
class Spider_One(scrapy.Spider):
    name="Spider_One"
    allowed_domains = ["baidu.com"]
    start_urls = [
       "http://tieba.baidu.com/f?kw=嘉祥一中&ie=utf-8&tab=good&cid=7"
       ,"http://tieba.baidu.com/f?kw=%E5%98%89%E7%A5%A5%E4%B8%80%E4%B8%AD&ie=utf-8&tab=good&cid=2"
       ,"http://tieba.baidu.com/f?kw=%E5%98%89%E7%A5%A5%E4%B8%80%E4%B8%AD&ie=utf-8&tab=good&cid=6"
    ] 
    def parse(self,response):
        logging.info("==爬虫Spider_One 的 parse start!==")
        self.num=0
        self.wanted_num=5
        item=TieziItem()
        infos=response.xpath('//div[@class="threadlist_lz clearfix"]/div/a[@class="j_th_tit "]')
        for info in infos:
            item['title']=info.xpath("text()").extract()[0]
            item['url']="http://tieba.baidu.com"+info.xpath("@href").extract()[0]
            item['author']=info.xpath('..').xpath('..').xpath("div[@class='threadlist_author pull_right']/span/a/text()").extract()[0]
            self.num=self.num+1
            request = scrapy.Request(item['url'], callback=self.parseTieziDetail)
            request.meta['item'] = item
            yield request
            
    def shutdown(self):
        '''可能会数量太多,在这儿就拦截了'''
        if self.num>=self.wanted_num:
                return 
            

    def parseTieziDetail(self,response):
        ''' 这个还需要把帖子内容解析出来'''
        item = response.meta['item']
        infos=response.xpath("//cc/div/text()").extract()
        mStr='\n'.join(infos)
        item['content']=mStr
        return item
    
    def getRideOfHtmlMarker(self,mStr):
        '''去除html标记'''
        soup=BeautifulSoup(mStr)
        return ''.join(soup.findAll(text=True))
        
            

        

