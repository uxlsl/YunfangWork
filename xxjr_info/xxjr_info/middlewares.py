# -*- coding: utf-8 -*-

import random
import base64
import time,urllib,json
#from settings import PROXIES
url_respon = urllib.urlopen('http://dynamic.goubanjia.com/dynamic/get/58fdfaac3262b71dd8a4ca2083ce25f5.html').read().replace("\n","")
PROXIES = [url_respon,]
up_time = time.time()
time_ch = 0


class RandomUserAgent(object):
  """Randomly rotate user agents based on a list of predefined ones"""


  def __init__(self, agents):
    self.agents = agents
  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings.getlist('USER_AGENTS'))
  def process_request(self, request, spider):
    #print "**************************" + random.choice(self.agents)
    request.headers.setdefault('User-Agent', random.choice(self.agents))

    
class ProxyMiddleware(object):
  def process_request(self, request, spider):
    global up_time
    global PROXIES
    global url_respon
    global time_ch
    low_time = time.time()
    time_ch = low_time-up_time
    print time_ch,low_time,up_time
    try:
      if (low_time-up_time)>random.randint(15,25):
        time_ch = 0
        up_time = time.time()
        url_respon = urllib.urlopen('http://dynamic.goubanjia.com/dynamic/get/58fdfaac3262b71dd8a4ca2083ce25f5.html').read().replace("\n","")
        PROXIES.append(url_respon)
        if len(PROXIES)>3:
          del PROXIES[0]
        print up_time,low_time
    except Exception,e:  
      print Exception,":",e 
      time_ch = 0
      up_time = time.time()

    proxy = random.choice(PROXIES)
    print "**************ProxyMiddleware no pass************   %s"%(proxy)
    request.meta['proxy'] = "http://%s" % (proxy)
