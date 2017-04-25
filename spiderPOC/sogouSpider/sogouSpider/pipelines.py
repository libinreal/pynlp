# -*- coding: utf-8 -*-

from scrapy import log
from twisted.enterprise import adbapi

from scrapy.conf import settings
import os
import urllib
import pymongo
import MySQLdb
import MySQLdb.cursors


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
        for i in range(len(item['article_name'])):
            tx.execute("select * from ws_data_article_topic as t where t.article_code = %s", (item['article_id'][i]))
            result = tx.fetchone()
            
            article_from = item['article_from'][i].decode("gb2312", "ignore").encode("utf-8", "ignore")
            article_key = item['article_key'][i].decode("gb2312", "ignore").encode("utf-8", "ignore")    
            print "article_from", article_from
            if not result:
                #insert_sql = 'insert into article_info(id,article_name,article_time,article_url,crawl_time,praise_num,comment_num,article_from,article_author) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(item['article_id'][i],item['article_name'][i],item['article_time'][i],item['article_url'][i],item['crawl_time'][i],item['click_num'][i],item['reply_num'][i],item['article_from'][i],item['article_author'][i])
                insert_sql = "insert into ws_data_article_topic(article_code,title,createtime,"\
                             +"url,crawl_time,"\
                             +"praise_num,comment_num,site_name,author,keyword,scheduler_id,area)"\
                             +" values ('%s','%s','%s','%s','%s',%d,%d,'%s','%s','%s',%d, '%s')"\
                             % (item['article_id'][i],item['article_name'][i],item['article_time'][i],\
                            item['article_url'][i],item['crawl_time'][i],\
                            int(item['click_num'][i]),int(item['reply_num'][i]),item['article_from'][i],\
                            item['article_author'][i],item['article_key'][i], item['scheduler_id'][i],item['area'][i])
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
        '''
        print "MongoDBPipeline.................process_item..."
        content = {}
        for i in range(len(item['article_name'])):
            contentid = item['article_id'][i]
            contentlist = item['article_content'][i].splitlines()  # 分行
            for subcontent in contentlist:
                 subcontent = subcontent.replace('\t', '')
                 subcontent = subcontent.replace('　', '')  # 去掉汉子空格
                 if subcontent != '':
                     subcontent = subcontent.lstrip()
                     subcontent = subcontent.rstrip()
                     content['article_id'] = contentid
                     content['article_content'] = subcontent
                     self.collection.insert(dict(content))
        '''
                    
        
                    
        print "\n", "="*20, " comment content(mongodb) ", "="*20, "\n"
        comment = {}
        for i in range(len(item['article_id'])):
            comment_code = item['article_id'][i]
            comment_time = item['article_time'][i]
            comment_content = item['article_content'][i] # 分行
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


class ImagePipeline(object):
    def process_item(self, item, spider):
        '''
        if item['image_urls'][0]:
            dir_path = '%s/scrapy/%s' % (settings['IMAGES_STORE'], spider.name)  # 存储路径
            print 'dir_path', dir_path
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['image_urls']:
                list_name = image_url.split('/')
                #file_name = list_name[len(list_name) - 1]+'.jpg'  # 图片名称
                file_name = list_name[4]+'.jpg'  # 图片名称
                # print 'filename',file_name
                file_path = '%s/%s' % (dir_path, file_name)
                # print 'file_path',file_path
                if os.path.exists(file_name):
                    continue
                with open(file_path, 'wb') as file_writer:
                    conn = urllib.urlopen(image_url)  # 下载图片
                    file_writer.write(conn.read())
                file_writer.close()
        '''
        return item