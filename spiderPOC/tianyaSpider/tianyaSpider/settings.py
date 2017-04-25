# -*- coding: utf-8 -*-

# Scrapy settings for CpesecSpiers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tianyaSpider'

SPIDER_MODULES = ['tianyaSpider.spiders']
NEWSPIDER_MODULE = 'tianyaSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CpesecSpiers (+http://www.yourdomain.com)'
#减慢爬取速度 为1s  
download_delay = 2
#爬取网站深度
DEPTH_LIMIT = 20
#禁止cookies,防止被ban  
COOKIES_ENABLED = False


# ----- 配置MongoDB
MONGODB_SERVER = '192.168.2.187'
MONGODB_PORT = 27017
MONGODB_DB = 'comment' #数据库名
MONGODB_COLLECTION = 'article'  #表名


# -----
ITEM_PIPELINES = {
        'tianyaSpider.pipelines.MySQLPipeline':300,
        'tianyaSpider.pipelines.MongoDBPipeline': 400

}
"""
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'cpsec_spider.spiders.rotate_useragent.RotateUserAgentMiddleware' :500,
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware' :110,
        'cpsec_spider.spiders.middlewares.ProxyMiddleware' : 100
    }
"""
"""
所谓的user agent，是指包含浏览器信息、操作系统信息等的一个字符串，也称之为一种特殊的网络协议。服务器通过它判断当前访问对象是浏览器、邮件客户端还
是网络爬虫。
UserAgent池
"""
USER_AGENTS = [
  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
  "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
  "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
  "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
  "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
  "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
  "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
"""
代理ip获取网址http://www.xici.net.co/
ip池
"""
PROXIES = [
  {'ip_port': '27.221.10.194:8081', 'user_pass': ''},
  {'ip_port': '147.143.2.221:9797', 'user_pass': ''},
  {'ip_port': '200.47.33.177:8000', 'user_pass': ''},
  {'ip_port': '182.239.127.140:80', 'user_pass': ''},
  {'ip_port': '183.250.177.17:55336', 'user_pass': ''},
  {'ip_port': '122.225.106.35:80', 'user_pass': ''},
  {'ip_port': '60.164.223.19:55336', 'user_pass': ''},
  {'ip_port': '183.207.228.11:86', 'user_pass': ''},
  {'ip_port': '218.89.170.114:8888', 'user_pass': ''},
  {'ip_port': '222.51.38.34:8118', 'user_pass': ''},
  {'ip_port': '106.58.63.63:55336', 'user_pass': ''},
  {'ip_port': '183.250.177.13:55336', 'user_pass': ''},
  {'ip_port': '218.61.39.55:55336', 'user_pass': ''},
  {'ip_port': '157.122.96.74:55336', 'user_pass': ''},
  {'ip_port': '67.195.42.72:80', 'user_pass': ''},
  {'ip_port': '190.183.62.232:3128', 'user_pass': ''},

]

