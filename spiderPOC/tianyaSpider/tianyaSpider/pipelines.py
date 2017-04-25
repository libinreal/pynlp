#coding=utf-8
##########################################################################
# author
#     chaosju
# description:
#     Define your item pipelines here
#     save or process  your spider's data 
# attention:
#     Don't forget to add your pipeline to the ITEM_PIPELINES setting in setting file
# help document:
#     See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
########################################################################
import re
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.conf import settings
from tianyaSpider.items import articleTopicItem
import pymongo
import MySQLdb
import MySQLdb.cursors
from scrapy.exceptions import DropItem
from tianyaSpider.tianyaSpiderUtil import  spiderutil as sp

class MySQLPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '192.168.2.187',
            db = 'webspider',
            user = 'root',
            passwd = '3ti123',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True)
            

    def process_item(self, item, spider):
        """
        if  spider.name == '360search' or spider.name == 'baidu' or spider.name == 'sogou':
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            return item
        elif  spider.name == 'ifengSpider':
            query = self.dbpool.runInteraction(self._conditional_insert_ifeng, item)
            return item
        elif spider.name == 'chinanews':
            query = self.dbipool.runInteraction(self._conditional_insert_chinanews, item)
            return item
        else:
        """    
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    def _conditional_insert(self, tx, item):
        if item["name"][0] == "articleTopicItem":
            print "********** articleTopicItem **********"
            for i in range(len(item['article_name'])):
                tx.execute("select * from ws_data_article_topic as t where t.article_code = %s", (item['article_id'][i]))
                result = tx.fetchone()
                #lens = sp.isContains(item['article_name'][i])
                #print lens
                #print item['article_name'][i]
                #if not result and lens != -1:
                    
                article_from = item['article_from'][i].decode("gb2312", "ignore").encode("utf-8", "ignore")
                keyword = item['article_key'][i] 
                print "article_from", article_from
                if not result:
                    #insert_sql = 'insert into article_info(id,article_name,article_time,article_url,crawl_time,praise_num,comment_num,article_from,article_author) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(item['article_id'][i],item['article_name'][i],item['article_time'][i],item['article_url'][i],item['crawl_time'][i],item['click_num'][i],item['reply_num'][i],item['article_from'][i],item['article_author'][i])
                    insert_sql = "insert into ws_data_article_topic(article_code,keyword,title,createtime,"\
                                 +"url,crawl_time,"\
                                 +"praise_num,comment_num,site_name,author)"\
                                 +" values ('%s','%s','%s','%s','%s','%s',%d,%d,'%s','%s')"\
                                 % (item['article_id'][i],keyword,item['article_name'][i],item['article_time'][i],\
                                item['article_url'][i],item['crawl_time'][i],\
                                int(item['click_num'][i]),int(item['reply_num'][i]),item['article_from'][i],item['article_author'][i])
                    try:
                        print insert_sql
                        tx.execute(insert_sql)
                        print "OK: MYSQL, insert data, article_topic"
                    except:
                        print "ERROR: MYSQL, insert data, article_topic"
                        pass
            
                
                

class MongoDBPipeline(object):
    def __init__(self):
        #connect to MongoDB
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if item["name"][0] == "articleCommentItem":
            print "********** articleCommentItem **********"
            comment = {}
            for i in range(len(item['name'])):
                comment_code = item['article_code'][i]
                comment_time = item['comment_time'][i]
                comment_content = item['comment_content'][i] # 分行
                comment_content = comment_content.replace('\t', '')
                comment_content = comment_content.replace('　', '')  # 去掉汉子空格
                if comment_content != '':
                    comment_content = comment_content.lstrip()
                    comment_content = comment_content.rstrip()
                    comment['code'] = comment_code
                    comment['content'] = comment_content
                    comment['time'] = comment_time
                    self.collection.insert(dict(comment))
                        
        return item
