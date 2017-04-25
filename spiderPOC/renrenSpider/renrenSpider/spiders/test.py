#coding=utf-8

import sys
import time
import os

reload(sys)
sys.setdefaultencoding('utf8')

url = "http://share.renren.com/share/226075584/18092342553?from=0104100202"

entryOwnerId = ""
entryId = ""


s = url.split('/')
entryOwnerId = s[len(s)-2]
entryId = s[len(s)-1]
arr = entryId.split("?")
if len(arr)>1:
    entryId = arr[0]
else:
    entryId = b

print "entryOwnerId:", entryOwnerId    
print "entryId:", entryId