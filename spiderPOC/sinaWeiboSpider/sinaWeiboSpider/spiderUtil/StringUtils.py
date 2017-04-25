#coding=utf8 
###################################################
#
#用途:爬虫的工具类
#作者:chaosju
#version:1.0
#
#
###################################################
import time
import os
import hashlib
from hashlib import md5
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
    path = "/CpsecSpiders/keywords.txt"
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


