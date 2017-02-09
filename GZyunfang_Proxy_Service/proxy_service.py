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


import random,urllib2,json,base64,time,lxml,os

from scrapy.exceptions import NotConfigured
from twisted.internet import task
from scrapy import signals
from redis import Redis
from twisted.internet import reactor
from configobj import ConfigObj


# get config from file ./proxy_service.cfg

service_config = ConfigObj(os.getcwd()+'/proxy_service.cfg')
proxy_api = service_config['proxy_ip_settings']['PROXY_API']
bind_api = service_config['proxy_ip_settings']['BIND_API']
api_timeout = int(service_config['proxy_ip_settings']['API_TIMEOUT'])
redis_host = service_config['proxy_ip_settings']['REDIS_HOST']
redis_port = service_config['proxy_ip_settings']['REDIS_PORT']
get_ip_delay = int(service_config['proxy_ip_settings']['GET_IP_DELAY'])
bind_ip_delay = int(service_config['proxy_ip_settings']['BIND_IP_DELAY'])



#reactor func to get proxy IPs

def _get_proxy():
    global hash_index,proxy,api_timeout,redis_port,redis_host
    try:
        r = Redis(host=redis_host, port=redis_port) 
        print get_curtime()," : ","get proxy ip from api\r\n"
        url_respon = (urllib2.urlopen(proxy_api,timeout = api_timeout).read().split("\r\n"))
        print get_curtime()," : ","add proxy ip %s to pool ,hash_index is %s \r\n"%(str(url_respon),hash_index)
        for offset_index in range(len(url_respon)):
            if ('<' in url_respon[offset_index]) or url_respon[offset_index] == '':
                print "pass %s"%(url_respon[offset_index])
                pass
            else:
                r.hset("Proxy_Test:Middle_Temp",hash_index,url_respon[offset_index])
                hash_index += 1
                if hash_index>249:
                    hash_index = 0
                    print get_curtime()," : ","reset hash_index :%s\r\n"%hash_index
        r.delete('Proxy_Test:Pool')
        for item in set(r.hvals('Proxy_Test:Middle_Temp')):
            r.sadd('Proxy_Test:Pool',item)
        print get_curtime()," : ","success \r\n"
    except Exception as e:
        print get_curtime()," : ", Exception,":",e




#reactor func to bind the host ip to the supplier service

def _bind_ip():
    global bind_api
    try:
        verify_result = ''
        while not (verify_result == 'ok'):
            print get_curtime()," : ","bind ip to proxy service verify\r\n"
            verify_result = urllib2.urlopen(bind_api,timeout = api_timeout).read()
            print get_curtime()," : ","verify result is %s \r\n"%verify_result
            print get_curtime()," : ","waiting for service verified......"
            time.sleep(20)
        print get_curtime()," : ","success \r\n"
    except Exception as e:
        print get_curtime()," : ", Exception,":",e




def get_curtime():

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())




#start the service with twisted reactor

if __name__ == '__main__':
    
    hash_index = 0
    task_bindIP_service = task.LoopingCall(_bind_ip)
    task_bindIP_service.start(bind_ip_delay)
    task_proxy_service = task.LoopingCall(_get_proxy)
    task_proxy_service.start(get_ip_delay)
    reactor.run()
