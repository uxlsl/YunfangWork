# -*- coding: utf-8 -*-

import random
import base64
import time,urllib,json
from redis import Redis
#from settings import PROXIES


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
    r = Redis(host='192.168.6.4',port=6379)
    proxy = r.srandmember("GZYF_Test:Proxy_Pool",1)[0]
    #print "**************ProxyMiddleware no pass************   %s"%(proxy)
    request.meta['proxy'] = "http://%s" % (proxy)
