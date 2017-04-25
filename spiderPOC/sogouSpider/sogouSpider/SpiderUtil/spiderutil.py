#coding=utf8 
###################################################
#
#用途:爬虫的工具类
#version:1.0
#
#
###################################################
import time
import os
import hashlib
from hashlib import md5

import urllib2
import urllib
import cookielib
import re
import HTMLParser


 #时间 20151102
def get_tody_time():
    t = time.time()
    lt = time.localtime(t)
    format_str = '%Y-%m-%d'
    todytime = time.strftime(format_str,lt)
    return todytime
#计算url的hash值,采用md5hash算法，生成32位的unicode
def hashForUrl(url):

    m = md5() #hash对象
    m.update(url) #得到hash之后的byte
    return m.hexdigest() #返回unicodei
    #时间年月日时分秒 20151102
def get_tody_timestamp():
    t = time.time()
    lt = time.localtime(t)
    format_str = '%Y-%m-%d %H:%M:%S'
    todytimestamp = time.strftime(format_str,lt)
    return todytimestamp
def isContains(title):
    path = "/sogouWechart/keywords.txt"
    xmlpath = os.getcwd()+path
    file = open(xmlpath)
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            list = line.split('+')
        for keyword in list:
            if title.find(keyword) != -1:
                print keyword
                return 1
    return -1

def get_cookie(auth_url, url):
    data={}
    post_data=urllib.urlencode(data)
    headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    
    cookieJar=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    req=urllib2.Request(auth_url,post_data,headers)
    #result = opener.open(req)
    result = opener.open(url)
        
    if result.code == 200:
        c = ''
        dic = {}
        for item in cookieJar:
            key = str(item.name)
            value = str(item.value)
            dic[key]=value

    return dic

