#!/usr/bin/python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------
# 
#                                  _oo8oo_
#                                 o8888888o
#                                 88" . "88
#                                 (| -_- |)
#                                 0\  =  /0
#                               ___/'==='\___
#                             .' \\|     |// '.
#                            / \\|||  :  |||// \
#                           / _||||| -:- |||||_ \
#                          |   | \\\  -  /// |   |
#                          | \_|  ''\---/''  |_/ |
#                          \  .-\__  '-'  __/-.  /
#                        ___'. .'  /--.--\  '. .'___
#                     ."" '<  '.___\_<|>_/___.'  >' "".
#                    | | :  `- \`.:`\ _ /`:.`/ -`  : | |
#                   \  \ `-.   \_ __\ /__ _/   .-` /  /
#                =====`-.____`.___ \_____/ ___.`____.-`=====
#                                  `=---=`
# 
# 
#               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                       佛祖保佑         永不宕机/永无bug
#
#
#-----------------------------------------------------------------


import random,urllib2,json,base64,time

from scrapy.exceptions import NotConfigured
from twisted.internet import task
from scrapy import signals
from redis import Redis
from twisted.internet import reactor

proxy_api = 'http://api.goubanjia.com/api/get.shtml?order=58fdfaac3262b71dd8a4ca2083ce25f5&num=100&carrier=0&protocol=0&an1=1&an2=2&an3=3&sp1=1&sp2=2&sort=1&system=1&distinct=0&rettype=1&seprator=%0D%0A'
api_timeout = 4
redis_host = '192.168.10.48'
redis_port = 6379

def log():
    global hash_index,proxy,api_timeout,redis_port,redis_host
    try:
        r = Redis(host=redis_host, port=redis_port) 
        print get_curtime()," : ","get proxy ip from api\r\n"
        url_respon = (urllib2.urlopen(proxy_api,timeout = api_timeout).read().split("\r\n"))
        print get_curtime()," : ","add proxy ip %s to pool ,hash_index is %s \r\n"%(str(url_respon),hash_index)
        for offset_index in range(len(url_respon)):
            if ('<' in url_respon[offset_index]) or url_respon[offset_index] == '':
                print "pass %s"%url_respon[offset_index]
                pass
            else:
                r.hset("anjuke_test:proxy_pool",hash_index,url_respon[offset_index])
                hash_index += 1
                if hash_index>249:
                    hash_index = 0
                    print get_curtime()," : ","reset hash_index :%s\r\n"%hash_index
        print get_curtime()," : ","success \r\n"
    except Exception as e:
        print get_curtime()," : ", Exception,":",e

def get_curtime():

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


if __name__ == '__main__':
    
    r = Redis(host=redis_host, port=redis_port) 
    print get_curtime()," : ","start service \r\nget proxy ip from api\r\n"
    url_respon = (urllib2.urlopen(proxy_api,timeout = api_timeout).read().split("\r\n"))
    hash_index = 0
    print get_curtime()," : ","add proxy ip %s to pool ,hash_index is %s \r\n"%(str(url_respon),hash_index)
    for offset_index in range(len(url_respon)):
        if ('<' in url_respon[offset_index]) or url_respon[offset_index] == '':
            print "pass %s"%url_respon[offset_index]
            pass
        else:
            r.hset("anjuke_test:proxy_pool",hash_index,url_respon[offset_index])
            hash_index += 1
    print get_curtime()," : ","success \r\n"
    task1 = task.LoopingCall(log)
    task1.start(6)
    reactor.run()