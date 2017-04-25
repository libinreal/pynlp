#coding=utf-8

import urllib
import urllib2
import cookielib 


from scrapy.contrib.loader import ItemLoader
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import scrapy
import lxml.html as lh
import sys
import time
import os
from urlparse import urljoin
from xml.dom.minidom import parse
import xml.dom.minidom

reload(sys)
sys.setdefaultencoding('utf8')

import datetime

import json



headers_settings = {
    "Host": "s.weibo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Cookie": "SINAGLOBAL=595181393488.4609.1491986628721; ULV=1492396639065:4:4:1:3668409379106.0034.1492396639061:1492141427480; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWE9ri20yPalgno4V-BjYGr5JpX5KMhUgL.Foq7SKB0SK2feKn2dJLoIp7LxKqLBo-LBoMLxKqLBo-LB-2ceh-Xe0-pSK2R; SCF=Au8oIqYFo3vHpz28h-dWaO-gxd7YcXGqmEM5rGwdjdouynFtudrwYYPyEex162kV-O6TvqdkD48Fh4ZqYWr3Aog.; SUHB=0JvgKzgiofcNyj; ALF=1523932736; un=18221065710; wvr=6; UOR=,,login.sina.com.cn; SWB=usrmdinst_8; SUB=_2A2518FqRDeRhGeBO7lYS9S_JyjSIHXVWhMtZrDV8PUNbmtBeLW6mkW9p3zFs3YF5siOk0pe6K7olcUEtkw..; SSOLoginState=1492396737; _s_tentry=login.sina.com.cn; Apache=3668409379106.0034.1492396639061",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0, no-cache",
    "Pragma": "no-cache"}
    
'''

#第一步：登陆知乎

#拿到一个cookie实例，用来保留cookie，具体怎么保留这个不用操心，一切给http handler(这里就是HTTPCookieProcessor)处理
cookie = cookiellib.CookieJar()
#整一个opener出来，实际上不这么整的话，就像最普通的urllib2.urlopen(url)这样，实际上也是用了一个默认的openrer，只不过今天在这里是明确指定了opener，因为要搞cookie么
#build_opener里面加了一个http handler用来处理所有http请求相关的东西，包括cookie的操作，这里为了搞cookie，所以用了这个cookieprocessor，里面放刚才的cookie实例
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
data = {"email":"xxx","password":"xxx"}
data=urllib.urlencode(data)
request = urllib2.Request("http://www.zhihu.com/login", data)
response = opener.open(request)
#这个时候cookie已经被保存好了
print cookie


#第二步：进入个人中心编辑页面
#注意上面cookie已经保存好了，而且注意是用这个cookie创建了httpcookieprocessor，又用这个httphandler创建了opener，所以这个opener就跟cookie关联上了，那么接下来进入个人中心就直接用这个opener就可以了
response2 = opener.open("http://www.zhihu.com/people/edit")

'''



data={"email":"","password":""} 
post_data=urllib.urlencode(data)  
cj=cookielib.CookieJar()   #获取cookiejar实例
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
website = "http://s.weibo.com/ajax/comment/small?act=list&mid=4097906900899202&uid=6054351518&smartFlag=false&smartCardComment=&isMain=true&suda-data=key%253Dtblog_search_weibo%2526value%253Dweibo_h_1_p_p&pageid=weibo&_t=0&__rnd=1492503865654"
req=urllib2.Request(website,post_data,headers)
content=opener.open(req)
print content.read()   

