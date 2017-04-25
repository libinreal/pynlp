#coding=utf-8
#这个是用来运行云端服务的
import urllib
import urllib2
dmoz_data={'project':'scrapydDemo','spider':'dmoz'}
dmoz_data_urlencode=urllib.urlencode(dmoz_data)
requesurl="http://localhost:6800/schedule.json"
req=urllib2.Request(url=requesurl,data=dmoz_data_urlencode)
print req

res_data=urllib2.urlopen(req)
res=res_data.read()
print res

t=raw_input()
if(t=='q'):
    print "退出"
else:
     raw_input()
