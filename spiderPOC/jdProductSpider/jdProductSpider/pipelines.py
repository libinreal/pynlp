# -*- coding: utf-8 -*-

from scrapy import log
from twisted.enterprise import adbapi

from scrapy.conf import settings
import os
import urllib
import pymongo
import MySQLdb
import MySQLdb.cursors

import datetime
import time

class JdproductspiderPipeline(object):
    def process_item(self, item, spider):
        return item


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
        if item["name"][0] == "productTopicItem":
            query = self.dbpool.runInteraction(self._product_comment_topic_insert, item)
            return item
        elif item["name"][0] == "productTagStatisticsItem":
            query = self.dbpool.runInteraction(self._product_comment_tag_insert, item)
            return item
        elif item["name"][0] == "productCommentItem":
            query = self.dbpool.runInteraction(self._product_comment_content_insert, item)
            return item
        else:
            return item

                
    def _product_comment_topic_insert(self, tx, item):
        print "\n", "="*20, " comment topic ", "="*20, "\n"
        for i in range(len(item['name'])):
            record_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print record_time
            
            insert_sql = "insert into ws_data_product_comment_topic(scheduler_id,keyword,product_name,"\
                         + "product_brand,product_code,product_title,product_cate1,product_cate2,"\
                         + "product_cate3,product_attr1,product_attr2,product_attr3,"\
                         + "product_addr,comment_url,comment_count,good_count,general_count,poor_count,"\
                         + "crawl_time,record_time, site_name"\
                         + ")"\
                         + " values (%d,'%s','%s',"\
                         + "'%s','%s','%s','%s','%s',"\
                         + "'%s','%s','%s','%s',"\
                         + "'%s','%s',%d,%d,%d,%d,"\
                         + "'%s','%s', '%s'"\
                         + ")"
                        
            insert_sql = insert_sql%(item['scheduler_id'][i],item['keyword'][i],item['product_name'][i],\
                                item['product_brand'][i],item['product_code'][i],item['product_title'][i],'','',\
                                '',item['product_attr1'][i],item['product_attr2'][i],item['product_attr3'][i],\
                                item['product_addr'][i],item['comment_url'][i],item['comment_count'][i],item['good_count'][i],item['general_count'][i],item['poor_count'][i],\
                                item['crawl_time'][i],record_time, item['product_from'][i])
                                
            try:
                print insert_sql.decode('utf-8', 'ignore').encode('gb2312', 'ignore')
                tx.execute(insert_sql)
                print "OK: MYSQL, insert data, comment_topic"
            except:
                print "ERROR: MYSQL, insert data, comment_topic"
                pass
                            
 
    def _product_comment_tag_insert(self, tx, item):
        print "\n", "="*20, " comment tags ", "="*20, "\n"
        for i in range(len(item['name'])):
            record_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print record_time
            
            # find topic id
            topic_id = 0
            tx.execute("select id from ws_data_product_comment_topic where product_code = %s", (item['product_code'][i]))
            result = tx.fetchone()
            topic_id = result["id"]
            if topic_id == 0 or topic_id == None:
                print "ERROR: MYSQL, insert data, comment tags, can't find topic_id"
                continue

            insert_sql = "insert into ws_data_product_comment_tags_statistics(topic_id,tag,count,crawl_time,record_time)"\
                         + " values (%d,'%s',%d,'%s','%s')"
            insert_sql = insert_sql%(topic_id, item['tag'][i],item['count'][i],\
                                    item['crawl_time'][i],record_time)
                                    
            try:
                print insert_sql
                tx.execute(insert_sql)
                print "OK: MYSQL, insert data, comment_tag"
            except:
                print "ERROR: MYSQL, insert data, comment_tag"
                pass
            
                                    
    def _product_comment_content_insert(self, tx, item):
        print "\n", "="*20, " comment content ", "="*20, "\n"
        for i in range(len(item['name'])):
            record_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print record_time
            
            # find topic id
            topic_id = 0
            tx.execute("select id from ws_data_product_comment_topic where product_code = %s", (item['product_code'][i]))
            result = tx.fetchone()
            topic_id = result["id"]
            if topic_id == 0 or topic_id == None:
                print "ERROR: MYSQL, insert data, comment content, can't find topic_id"
                continue
        
            insert_sql = "insert into ws_data_product_comment_content("\
                         +" topic_id,guid,comment_content,comment_stars,"\
                         + "comment_praise,comment_time,crawl_time,record_time)"\
                         + " values (%d,'%s','%s',%d,%d,'%s','%s','%s')"
     
            insert_sql = insert_sql%(topic_id, item['guid'][i],item['comment_content'][i],item['comment_stars'][i],\
                                    item['comment_praise'][i],item['comment_time'][i],item['crawl_time'][i],record_time)
                                    
            try:
                print insert_sql
                tx.execute(insert_sql)
                print "OK: MYSQL, insert data, comment_content"
            except:
                print "ERROR: MYSQL, insert data, comment_content"
                pass



        
        

